import requests
from pytest_nhsd_apim.identity_service import (
    AuthorizationCodeConfig,
    AuthorizationCodeAuthenticator,
)


def get_auth():
    # 1. Set your app config
    config = AuthorizationCodeConfig(
        environment="int",
        identity_service_base_url="https://int.api.service.nhs.uk/oauth2-mock",  # pyright: ignore [reportArgumentType]
        callback_url="https://example.org/",  # pyright: ignore [reportArgumentType]
        client_id="4foToJR1dlX2Vs90pxRD1D48SaZMAwAY",  # INT
        client_secret="2NeQe6P6ObWPfILl",  # INT
        # client_id="tU1NHdDCHGrOi94pXdjCsXJOuZkOH8XA", # INTERNAL-DEV
        # client_secret="OLeZoP6Fb0BKbeYN", # INTERNAL-DEV
        scope="nhs-cis2",
        login_form={"username": "656005750104"},
    )

    # 2. Pass the config to the Authenticator
    authenticator = AuthorizationCodeAuthenticator(
        config=config  # pyright: ignore [reportArgumentType]
    )

    # 3. Get your token
    token_response = authenticator.get_token()
    assert "access_token" in token_response
    token = token_response["access_token"]

    # 4. Use the token and confirm is valid
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(
        f"https://int.api.service.nhs.uk/mock-jwks/test-auth/nhs-cis2/aal3",
        headers=headers,
    )
    assert resp.status_code == 200
    print("Successfully Authenticated")
    return token


if __name__ == "__main__":
    get_auth()
