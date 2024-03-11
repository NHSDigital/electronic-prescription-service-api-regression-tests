import base64
from datetime import datetime, time
import json
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate


# get ENV
url = os.environ["PACT_PROVIDER_URL"]

# all keys
private_key_path = os.environ["SIGNING_PRIVATE_KEY_PATH"]
x509_certificate_path = os.environ["SIGNING_CERT_PATH"]
dummy_signature = "DQo8U2lnbmF0dXJlIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjIj4NCiAgICA8U2lnbmVkSW5mbz48Q2Fub25pY2FsaXphdGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMTAveG1sLWV4Yy1jMTRuIyI"


def get_jwt(digest):
    # add headers
    header = {
        "alg": "RS512",
        "typ": "JWT",
        "kid": "test-1"
    }

    # add payload
    payload = {
        "payloads": [
            {
                "id": "1",
                "payload": digest
            }
        ],
        "algorithm": "RS1",
        "iat": int(time.time()) - 600,  # Issued 10 mins ago
        "exp": int(time.time()) + 600,  # Expires in 10 minutes
        "aud": f"{url}/oauth2/token",
        "iss": os.environ["API_CLIENT_ID"],
        "sub": os.environ["API_CLIENT_ID"]
    }
    
    # token - how to encode it?
    encoded_header = base64.urlsafe_b64encode(json.dumps(header)).decode()
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload)).decode()

    token = f"{encoded_header}.{encoded_payload}"
    return token

# get the signed signature
def get_signed_signature(digest, valid):
    # check if key and cert exist to assign signature
    private_key_exists = os.path.exists(private_key_path)
    x509_cert_exists = os.path.exists(x509_certificate_path)
    digest_placeholder = "{{digest}}"
    signature_placeholder = "{{signature}}"
    cert_placeholder = "{{cert}}"
    
    # assign signature dummy if key and cert doesnt exist
    if not private_key_exists and x509_cert_exists:
        return dummy_signature
    
    # get buffer - decode
    digest_buffer = base64.b64decode(digest, "utf-8").decode("utf-8")
    # get no namespace replace(`<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">`, `<SignedInfo>`)
    digest_without_namespace = digest_buffer.replace('<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">', '<SignedInfo>')
    
    # get private key to use for signature
    private_key = serialization.load_pem_private_key(
        get_path(private_key_path),
        password=None,
        backend=default_backend()
    )
    # get signed_signature
    signed_signature = private_key.sign(
        digest_buffer,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    # get certificate
    cert_data = get_path(x509_certificate_path)
    # x509?? - certificate
    cert = load_pem_x509_certificate(cert_data, default_backend())
    # check if cert has expired
    if cert.not_valid_after < datetime.now():
        # raise an Exception if it has
        raise ValueError("Signing certificate has expired")
    # get the raw value to certificate_value???
    certificate_value = base64.b64encode(cert_data).decode()
    # assign signData to template file 
    sign_data = get_path("./util/signature.txt") # change file path
    # get the signData for replace("{{digest}}", digestWithoutNamespace)
    sign_data = sign_data.replace(digest_placeholder, digest_without_namespace)
    # if valid signData = signData.replace("{{signature}}", signedSignature)
    if valid:
        sign_data = sign_data.replace(signature_placeholder, signed_signature)
    # else signData = signData.replace("{{signature}}", `${signedSignature}TVV3WERxSU0xV0w4ODdRRTZ3O`)
    else:
        sign_data = sign_data.replace(signature_placeholder, f"{signed_signature}TVV3WERxSU0xV0w4ODdRRTZ3O")
    # outside of else signData = signData.replace("{{cert}}", certificateValue)
    sign_data = sign_data.replace(cert_placeholder, certificate_value)
    
    #get signature - decode
    signature = base64.b64encode(sign_data, "utf-8").decode("utf-8")
    return signature
        
    
    
def get_path(path):
    with open(path, "rb") as f:
        doc = f.read()
    return doc
