import uuid
import allure
import requests
from assertpy import assert_that as assertpy_assert  # type: ignore


def assert_that(expected, context):
    description = (
        f"Actual Response: Status Code: {context.response.status_code}, "
        f"Body: {context.response.content}"
    )
    return assertpy_assert(expected, description=description)


def attach_api_information(context):
    allure.attach(
        str(context.response.request.headers),
        "REQUEST Headers",
        allure.attachment_type.TEXT,
    )
    allure.attach(
        str(context.response.request.method),
        "REQUEST Method",
        allure.attachment_type.TEXT,
    )
    allure.attach(
        str(context.response.request.url), "REQUEST URL", allure.attachment_type.TEXT
    )
    allure.attach(
        str(context.response.request.body), "REQUEST Body", allure.attachment_type.JSON
    )
    allure.attach(
        str(context.response.status_code),
        "RESPONSE Status Code",
        allure.attachment_type.TEXT,
    )
    allure.attach(
        str(context.response.headers), "RESPONSE Headers", allure.attachment_type.TEXT
    )
    allure.attach(
        str(context.response.content), "RESPONSE Body", allure.attachment_type.JSON
    )


def get_default_headers():
    return {
        "x-request-id": str(uuid.uuid4()),
        "x-user-org-code": "Auto001",
    }


def request_ping(context):
    url = f"{context.fhir_base_url}/_ping"
    print(f"going to {url}")
    context.response = requests.get(url=url)
    attach_api_information(context)


def the_expected_response_code_is_returned(context, expected_response_code: int):
    actual_response_code = context.response.status_code
    allure.attach(str(expected_response_code), "Expected", allure.attachment_type.TEXT)
    allure.attach(str(actual_response_code), "Actual", allure.attachment_type.TEXT)
    assert_that(actual_response_code, context).is_equal_to(expected_response_code)
