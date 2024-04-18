#####################################################################
# Translated from FHIR Facade API code                              #
# See:                                                              #
# https://github.com/NHSDigital/electronic-prescription-service-api #
# packages/e2e-tests/services/update-prescriptions.ts               #
# packages/bdd-tests/services/getJWT.ts                             #
#####################################################################

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import Encoding, load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate
from datetime import datetime, timezone
from os.path import exists

# PRIVATE_KEY_PATH = os.environ["SIGNING_PRIVATE_KEY_PATH"]
# X509_CERT_PATH = os.environ["SIGNING_CERT_PATH"]
PRIVATE_KEY_PATH = "./certs/cert.crt"
X509_CERT_PATH = "./certs/x506.pem"
DUMMY_SIGNATURE = """
DQo8U2lnbmF0dXJlIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLz\
A5L3htbGRzaWcjIj4NCiAgICA8U2lnbmVkSW5mbz48Q2Fub25pY2FsaXph\
dGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMD\
EvMTAveG1sLWV4Yy1jMTRuIyI
"""

PRIVATE_KEY_EXISTS = exists(PRIVATE_KEY_PATH)
X509_CERT_EXISTS = exists(X509_CERT_PATH)


def verify_certificate_valid_when_signed(signature_date, certificate):
    certificate_start_date = certificate.not_valid_before_utc
    certificate_end_date = certificate.not_valid_after_utc
    return certificate_start_date <= signature_date <= certificate_end_date


def get_signature(digest: str, valid: bool):
    with open(X509_CERT_PATH, "rb") as cert_file:
        cert_data = cert_file.read()
    certificate = load_pem_x509_certificate(cert_data, default_backend())

    # Get the current date (signature date)
    signature_date = datetime.now(timezone.utc)

    # Check if certificate has expired
    if verify_certificate_valid_when_signed(signature_date, certificate):
        print("Certificate is valid.")
    else:
        raise Exception("Certificate has expired. You may need to generate a new one.")

    if not PRIVATE_KEY_EXISTS and X509_CERT_EXISTS:
        return DUMMY_SIGNATURE
    # load x509 and check it hasn't expired
    cert_bytes = load_file(X509_CERT_PATH)
    x509_cert = load_pem_x509_certificate(cert_bytes)

    if x509_cert.not_valid_after_utc < datetime.now(timezone.utc):
        raise Exception("Signing certificate has expired")

    # load private key and generate signature
    key_bytes = load_file(PRIVATE_KEY_PATH)
    private_key = load_pem_private_key(key_bytes, password=None)

    digest = base64.b64decode(digest).decode("utf-8")
    # print(f"Digest: {digest}")

    signature_raw = private_key.sign(  # pyright: ignore [reportAttributeAccessIssue, reportCallIssue]
        digest.encode("utf-8"),
        padding.PKCS1v15(),  # pyright: ignore [reportAttributeAccessIssue, reportCallIssue]
        hashes.SHA1(),  # pyright: ignore [reportAttributeAccessIssue, reportCallIssue]
    )

    # align format of signature with equivalent ts code
    signature = base64.b64encode(signature_raw).decode("ASCII")
    # print(f"Signature: {signature}")

    # prepare values for insertion into xml signature
    digest_without_namespace = digest.replace(
        ' xmlns="http://www.w3.org/2000/09/xmldsig#"', ""
    )
    # print(f"digest_without_namespace: {digest_without_namespace}")
    cert_public_bytes = x509_cert.public_bytes(encoding=Encoding.DER)
    cert_string = base64.b64encode(cert_public_bytes).decode("utf-8")
    # print(f"Cert: {cert_string} ----")

    # load template and insert prepared values
    xml_d_sig = f"""<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
        {digest_without_namespace}
        <SignatureValue>{signature if valid else f'{signature}TVV3WERxSU0xV0w4ODdRRTZ3O'}</SignatureValue>
        <KeyInfo>
            <X509Data>
                <X509Certificate>{cert_string}</X509Certificate>
            </X509Data>
        </KeyInfo>
      </Signature>"""

    # match returned signature data with that from equivalent ts code
    signature_data = base64.b64encode(xml_d_sig.encode("utf-8")).decode("utf-8")
    return signature_data


def load_file(path, mode="rb"):
    with open(path, mode) as f:
        doc = f.read()
    return doc


if __name__ == "__main__":
    print(
        get_signature(
            "PFNpZ25lZEluZm8geG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyMiPjxDYW5vbmljYWxpemF0aW9uTWV0aG9kIE"
            "FsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8xMC94bWwtZXhjLWMxNG4jIj48L0Nhbm9uaWNhbGl6YXRpb25NZXRob2Q+PFNp"
            "Z25hdHVyZU1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNyc2Etc2hhMSI+PC9TaWduYXR1cm"
            "VNZXRob2Q+PFJlZmVyZW5jZT48VHJhbnNmb3Jtcz48VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8xMC94"
            "bWwtZXhjLWMxNG4jIj48L1RyYW5zZm9ybT48L1RyYW5zZm9ybXM+PERpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3"
            "JnLzIwMDAvMDkveG1sZHNpZyNzaGExIj48L0RpZ2VzdE1ldGhvZD48RGlnZXN0VmFsdWU+bGREelRDZ0JQbXcvTm9kbU1FQTVQdTM2Z2U0"
            "PTwvRGlnZXN0VmFsdWU+PC9SZWZlcmVuY2U+PC9TaWduZWRJbmZvPg==",
            True,
        )
    )
