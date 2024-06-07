import json
import allure
import requests

from assertpy import assert_that as assertpy_assert  # type: ignore
from pytest_nhsd_apim.identity_service import (
    AuthorizationCodeAuthenticator,
    AuthorizationCodeConfig,
)

from features.environment import CIS2_USERS, CLIENT_ID, CLIENT_SECRET


def get_auth(user, env):
    # 1. Set your app config
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise ValueError("You must provide BOTH CLIENT_ID and CLIENT_SECRET")
    env = env.lower()
    url = f"https://{env}.api.service.nhs.uk/oauth2-mock"
    config = AuthorizationCodeConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        callback_url="https://example.org/",  # pyright: ignore [reportArgumentType]
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope="nhs-cis2",
        login_form={"username": CIS2_USERS[user]["user_id"]},
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
    if env == "int":
        response = requests.get(
            "https://int.api.service.nhs.uk/mock-jwks/test-auth/nhs-cis2/aal3",
            headers=headers,
        )
        if response.status_code != 200:
            print(f"{response.status_code}\n{str(response.content)}")
            raise AssertionError()
        assert response.status_code == 200
    return token


def get_auth_internal_dev():
    url = "https://sxhjsbv4d7tvmt67av3jlboera0yzvgc.lambda-url.eu-west-2.on.aws/?env=internal-dev"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        if access_token:
            return access_token
        else:
            print("Access token not found in response")
            return None
    else:
        print(f"Failed to retrieve access token. Status code: {response.status_code}")
        return None


def assert_that(actual):
    allure.attach(
        body=str(actual), name="Actual", attachment_type=allure.attachment_type.TEXT
    )
    return assertpy_assert(val=actual)


def attach_api_information(context):
    allure.attach(
        json.dumps(dict(context.response.request.headers)),
        "REQUEST Headers",
        allure.attachment_type.JSON,
    )
    allure.attach(
        json.dumps(context.response.request.method),
        "REQUEST Method",
        allure.attachment_type.JSON,
    )
    allure.attach(
        json.dumps(context.response.request.url),
        "REQUEST URL",
        allure.attachment_type.JSON,
    )
    allure.attach(
        json.dumps(context.response.request.body),
        "REQUEST Body",
        allure.attachment_type.JSON,
    )
    allure.attach(
        str(context.response.status_code),
        "RESPONSE Status Code",
        allure.attachment_type.TEXT,
    )
    allure.attach(
        json.dumps(dict(context.response.headers)),
        "RESPONSE Headers",
        allure.attachment_type.JSON,
    )
    allure.attach(
        context.response.content,
        "RESPONSE Body",
        allure.attachment_type.JSON,
    )


def the_expected_response_code_is_returned(context, expected_response_code: int):
    actual_response_code = context.response.status_code
    assert_that(actual_response_code).is_equal_to(expected_response_code)


if __name__ == "__main__":
    print(get_auth("dispenser", "INTERNAL-DEV"))
