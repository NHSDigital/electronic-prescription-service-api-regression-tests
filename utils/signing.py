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

from features.environment import PRIVATE_KEY, CERTIFICATE

DUMMY_SIGNATURE = """
DQo8U2lnbmF0dXJlIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLz\
A5L3htbGRzaWcjIj4NCiAgICA8U2lnbmVkSW5mbz48Q2Fub25pY2FsaXph\
dGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMD\
EvMTAveG1sLWV4Yy1jMTRuIyI
"""


def verify_certificate_valid_when_signed(signature_date, certificate):
    certificate_start_date = certificate.not_valid_before_utc
    certificate_end_date = certificate.not_valid_after_utc
    return certificate_start_date <= signature_date <= certificate_end_date


def get_signature(digest: str, algorithm: str):
    # Load X.509 certificate
    x509_cert = load_pem_x509_certificate(
        CERTIFICATE.encode("utf-8"),  # pyright: ignore [reportOptionalMemberAccess]
        default_backend(),
    )

    # Load private key
    private_key = load_pem_private_key(
        PRIVATE_KEY.encode("utf-8"),  # pyright: ignore [reportOptionalMemberAccess]
        password=None,
        backend=default_backend(),
    )

    # Get the current date (signature date)
    signature_date = datetime.now(timezone.utc)

    # Check if the certificate has expired
    if not verify_certificate_valid_when_signed(signature_date, x509_cert):
        raise RuntimeError(
            "Certificate has expired. You may need to generate a new one."
        )

    # check if X.509 certificate has expired
    if x509_cert.not_valid_after_utc < datetime.now(timezone.utc):
        raise RuntimeError("Signing certificate has expired")

    # Decode digest
    digest = base64.b64decode(digest).decode("utf-8")

    # Set signing algorithm from prepare response
    signing_algorithm = None

    if algorithm == "RS256":
        signing_algorithm = hashes.SHA256()
    elif algorithm == "RS1":
        signing_algorithm = hashes.SHA1()
    else:
        raise ValueError("Unsupported algorithm {}".format(algorithm))

    # Generate signature
    signature_raw = private_key.sign(  # pyright: ignore [reportAttributeAccessIssue]
        digest.encode("utf-8"),
        padding.PKCS1v15(),  # pyright: ignore [reportCallIssue]
        signing_algorithm,  # pyright: ignore [reportCallIssue]
    )
    # Align format of signature with equivalent TypeScript code
    signature = base64.b64encode(signature_raw).decode("ASCII")
    # Prepare values for insertion into XML signature
    digest_without_namespace = digest.replace(
        'xmlns="http://www.w3.org/2000/09/xmldsig#"', ""
    )
    cert_public_bytes = x509_cert.public_bytes(encoding=Encoding.DER)
    cert_string = base64.b64encode(cert_public_bytes).decode("utf-8")

    # Load template and insert prepared values
    xml_d_sig = f"""<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">{digest_without_namespace}\
    <SignatureValue>{signature}</SignatureValue><KeyInfo><X509Data><X509Certificate>{cert_string}\
    </X509Certificate></X509Data></KeyInfo></Signature>"""

    # Match returned signature data with that from equivalent TypeScript code
    signature_data = base64.b64encode(xml_d_sig.encode("utf-8")).decode("utf-8")
    return signature_data
