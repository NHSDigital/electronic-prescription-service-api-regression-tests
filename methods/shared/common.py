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
    APIGEE_APPS,
    JWT_PRIVATE_KEY,
    JWT_KID,
)


def get_psu_authenticator(env, url):
    client_id = APIGEE_APPS["PSU"]["client_id"]
    if client_id is None or JWT_KID is None or JWT_PRIVATE_KEY is None:
        raise ValueError("You must provide CLIENT_ID, JWT_KID and JWT_PRIVATE_KEY")
    config = ClientCredentialsConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        client_id=client_id,
        jwt_private_key=JWT_PRIVATE_KEY,
        jwt_kid=JWT_KID,
    )
    # 2. Pass the config to the Authenticator
    authenticator = ClientCredentialsAuthenticator(
        config=config  # pyright: ignore [reportArgumentType]
    )

    return authenticator


def get_eps_fhir_authenticator(user, env, url, product):
    scope = "nhs-cis2"
    login_form = {"username": CIS2_USERS[user]["user_id"]}
    client_id = APIGEE_APPS[product]["client_id"]
    client_secret = APIGEE_APPS[product]["client_secret"]
    if client_id is None or client_secret is None:
        raise ValueError("You must provide BOTH CLIENT_ID and CLIENT_SECRET")
    config = AuthorizationCodeConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        callback_url="https://example.org/",  # pyright: ignore [reportArgumentType]
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        login_form=login_form,
    )
    authenticator = AuthorizationCodeAuthenticator(
        config=config, allure=allure  # pyright: ignore [reportArgumentType]
    )
    return authenticator


def get_pfp_apigee_authenticator(env, url):
    scope = "nhs-login"
    login_form = {"username": LOGIN_USERS["user_id"]}
    client_id = APIGEE_APPS["PFP-APIGEE"]["client_id"]
    client_secret = APIGEE_APPS["PFP-APIGEE"]["client_secret"]
    if client_id is None or client_secret is None:
        raise ValueError("You must provide BOTH CLIENT_ID and CLIENT_SECRET")
    config = AuthorizationCodeConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        callback_url="https://example.org/",  # pyright: ignore [reportArgumentType]
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        login_form=login_form,
    )
    authenticator = AuthorizationCodeAuthenticator(
        config=config, allure=allure  # pyright: ignore [reportArgumentType]
    )
    return authenticator


def get_auth(env, product, user="prescriber"):
    authenticator = None
    if product not in [
        "CPTS-FHIR",
        "EPS-FHIR",
        "EPS-FHIR-SHA1",
        "EPS-FHIR-PRESCRIBING",
        "EPS-FHIR-PRESCRIBING-SHA1",
        "EPS-FHIR-DISPENSING",
        "PFP-APIGEE",
        "PSU",
    ]:
        raise ValueError(f"Unknown product {product}")
    env = env.lower()
    url = f"https://{env}.api.service.nhs.uk/oauth2-mock"
    if product in [
        "CPTS-FHIR",
        "EPS-FHIR",
        "EPS-FHIR-DISPENSING",
        "EPS-FHIR-PRESCRIBING",
        "EPS-FHIR-SHA1",
        "EPS-FHIR-PRESCRIBING-SHA1",
    ]:
        authenticator = get_eps_fhir_authenticator(user, env, url, product)
    if product == "PFP-APIGEE":
        authenticator = get_pfp_apigee_authenticator(env, url)
    if product == "PSU":
        authenticator = get_psu_authenticator(env, url)
    if authenticator is not None:
        with allure.step("calling get token"):
            return get_token(authenticator)
    else:
        raise ValueError(
            "Authentication failed because authenticator was not generated"
        )


def get_token(authenticator):
    # 3. Get your token
    with allure.step("calling authenticator.get token"):
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


def convert_to_uri(page_name):
    if page_name == "search by prescription":
        return "search-by-prescription-id"
    if page_name == "search by basic details":
        return "search-by-basic-details"
    return page_name
