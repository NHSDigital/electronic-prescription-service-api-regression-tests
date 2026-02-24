import json
from os import environ
import urllib.request
from urllib.error import HTTPError
import allure
import boto3
from botocore.exceptions import BotoCoreError, ClientError

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
    EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY,
    EPS_FHIR_DISPENSING_JWT_KID,
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
    # fmt: off
    authenticator = ClientCredentialsAuthenticator(config=config)  # pyright: ignore [reportArgumentType]
    # fmt: on
    return authenticator


def get_eps_fhir_dispensing_jwt_authenticator(env, url):
    print(
        "Getting EPS-FHIR-DISPENSING-JWT authenticator configuration from environment variables"
    )
    client_id = APIGEE_APPS["EPS-FHIR-DISPENSING"]["client_id"]
    if (
        client_id is None
        or EPS_FHIR_DISPENSING_JWT_KID is None
        or EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY is None
    ):
        raise ValueError(
            "You must provide EPS_FHIR_DISPENSING_CLIENT_ID, "
            "EPS_FHIR_DISPENSING_JWT_KID and EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY"
        )
    config = ClientCredentialsConfig(
        environment=env,
        identity_service_base_url=url,  # pyright: ignore [reportArgumentType]
        client_id=client_id,
        jwt_private_key=EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY,
        jwt_kid=EPS_FHIR_DISPENSING_JWT_KID,
    )
    # fmt: off
    authenticator = ClientCredentialsAuthenticator(config=config)  # pyright: ignore [reportArgumentType]
    # fmt: on
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
        # this should be the callback url registered for the apigee application
        # changed from example.org so it is responsive
        # if this url is unavailable, then you will see tests fail on a request to keycloak
        # as keycloak returns a 302 eventually to a this callback url.
        callback_url="https://google.com",  # pyright: ignore [reportArgumentType]
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        login_form=login_form,
    )
    # fmt: off
    authenticator = AuthorizationCodeAuthenticator(config=config)  # pyright: ignore [reportArgumentType]
    # fmt: on
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
        # this should be the callback url registered for the apigee application
        # changed from example.org so it is responsive
        # if this url is unavailable, then you will see tests fail on a request to keycloak
        # as keycloak returns a 302 eventually to a this callback url.
        callback_url="https://google.com",  # pyright: ignore [reportArgumentType]
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        login_form=login_form,
    )
    # fmt: off
    authenticator = AuthorizationCodeAuthenticator(config=config)  # pyright: ignore [reportArgumentType]
    # fmt: on
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
        "EPS-FHIR-DISPENSING-JWT",
        "PFP-APIGEE",
        "PFP-PROXYGEN",
        "PSU",
        "EPS-ASSIST-ME",
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
    if product == "EPS-FHIR-DISPENSING-JWT":
        authenticator = get_eps_fhir_dispensing_jwt_authenticator(env, url)
    if product == "PFP-APIGEE" or product == "PFP-PROXYGEN":
        authenticator = get_pfp_apigee_authenticator(env, url)
    if product == "PSU":
        authenticator = get_psu_authenticator(env, url)
    if authenticator is not None:
        return get_token(authenticator)
    else:
        raise ValueError("Authentication failed because authenticator was not generated")


def get_token(authenticator):
    token_response = authenticator.get_token()
    assert "access_token" in token_response
    token = token_response["access_token"]
    return token


def assert_that(actual):
    allure.attach(body=str(actual), name="Actual", attachment_type=allure.attachment_type.TEXT)
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


def fetch_oidc_jwt() -> str:
    # fetch GitHub environment variables to make HTTP token fetch request
    req_url = environ.get("ACTIONS_ID_TOKEN_REQUEST_URL")
    assert req_url is not None, "expected ACTIONS_ID_TOKEN_REQUEST_URL environment variable not found"

    req_token = environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    assert req_token is not None, "expected ACTIONS_ID_TOKEN_REQUEST_TOKEN environment variable not found"

    req_url = req_url + "&audience=sts.amazonaws.com"
    # build HTTP request and execute
    request = urllib.request.Request(
        headers={"Authorization": "bearer " + req_token},
        url=req_url,
    )
    try:
        response = urllib.request.urlopen(request)
    except HTTPError as err:
        raise ValueError("unexpected error fetching OIDC web identity value: " + str(err.read())) from err

    # parse response, return `value` property - containing the desired web identity JWT
    try:
        token_data = json.load(response)
    except json.decoder.JSONDecodeError as exc:
        raise ValueError("unable to fetch OIDC web identity token - malformed HTTP response") from exc

    response.close()
    return token_data.get("value", "")


def assume_aws_role(role_arn: str, session_name: str):

    web_identity_token = fetch_oidc_jwt()
    # create STS client
    sts_client = boto3.client("sts")

    # call AssumeRoleWithWebIdentity to obtain temporary credentials
    try:
        response = sts_client.assume_role_with_web_identity(
            RoleArn=role_arn,
            RoleSessionName=session_name,
            WebIdentityToken=web_identity_token,
        )
    except (BotoCoreError, ClientError) as err:
        raise ValueError("Unable to assume AWS role: " + str(err)) from err

    # extract and return temporary credentials
    credentials = response.get("Credentials", {})
    if not credentials:
        raise ValueError("unable to assume AWS role - no credentials returned")

    return {
        "aws_access_key_id": credentials.get("AccessKeyId", ""),
        "aws_secret_access_key": credentials.get("SecretAccessKey", ""),
        "aws_session_token": credentials.get("SessionToken", ""),
    }
