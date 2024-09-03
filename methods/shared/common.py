import json
import allure

from assertpy import assert_that as assertpy_assert  # type: ignore
from pytest_nhsd_apim.identity_service import (
    AuthorizationCodeAuthenticator,
    AuthorizationCodeConfig,
    ClientCredentialsConfig,
    ClientCredentialsAuthenticator,
)

from features.environment import (
    CIS2_USERS,
    LOGIN_USERS,
    CLIENT_ID,
    CLIENT_SECRET,
    JWT_PRIVATE_KEY,
    JWT_KID,
)


def get_psu_authenticator(env, url):
    if CLIENT_ID is None or JWT_KID is None or JWT_PRIVATE_KEY is None:
        raise ValueError("You must provide CLIENT_ID, JWT_KID and JWT_PRIVATE_KEY")
    config = ClientCredentialsConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        client_id=CLIENT_ID,
        jwt_private_key=JWT_PRIVATE_KEY,
        jwt_kid=JWT_KID,
    )
    # 2. Pass the config to the Authenticator
    authenticator = ClientCredentialsAuthenticator(
        config=config  # pyright: ignore [reportArgumentType]
    )

    return authenticator


def get_eps_fhir_authenticator(user, env, url):
    scope = "nhs-cis2"
    login_form = {"username": CIS2_USERS[user]["user_id"]}
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise ValueError("You must provide BOTH CLIENT_ID and CLIENT_SECRET")
    config = AuthorizationCodeConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        callback_url="https://example.org/",  # pyright: ignore [reportArgumentType]
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=scope,
        login_form=login_form,
    )
    authenticator = AuthorizationCodeAuthenticator(
        config=config  # pyright: ignore [reportArgumentType]
    )
    return authenticator


def get_pfp_apigee_authenticator(env, url):
    scope = "nhs-login"
    login_form = {"username": LOGIN_USERS["user_id"]}
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise ValueError("You must provide BOTH CLIENT_ID and CLIENT_SECRET")
    config = AuthorizationCodeConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        callback_url="https://example.org/",  # pyright: ignore [reportArgumentType]
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=scope,
        login_form=login_form,
    )
    authenticator = AuthorizationCodeAuthenticator(
        config=config  # pyright: ignore [reportArgumentType]
    )
    return authenticator


def get_auth(env, product, user="prescriber"):
    authenticator = None
    if product != "EPS-FHIR" and product != "PFP-APIGEE" and product != "PSU":
        raise ValueError(f"Unknown product {product}")
    env = env.lower()
    url = f"https://{env}.api.service.nhs.uk/oauth2-mock"
    if product == "EPS-FHIR":
        authenticator = get_eps_fhir_authenticator(user, env, url)
    if product == "PFP-APIGEE":
        authenticator = get_pfp_apigee_authenticator(env, url)
    if product == "PSU":
        authenticator = get_psu_authenticator(env, url)
    if authenticator is not None:
        return get_token(authenticator)
    else:
        raise ValueError(
            "Authentication failed because authenticator was not generated"
        )


def get_token(authenticator):
    # 3. Get your token
    token_response = authenticator.get_token()
    assert "access_token" in token_response
    token = token_response["access_token"]
    return token


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
