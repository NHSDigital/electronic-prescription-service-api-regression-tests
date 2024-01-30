import uuid
import allure
import requests
from assertpy import assert_that as assertpy_assert  # type: ignore


def assert_that(expected, context):
    allure.attach(expected, "Expected", allure.attachment_type.TEXT)
    allure.attach(context.actual, "Actual", allure.attachment_type.TEXT)
    description = (
        f"Actual Response: Status Code: {context.response.status_code}, "
        f"Body: {context.response.content}"
    )
    return assertpy_assert(expected, description=description)


def attach_api_information(context):
    allure.attach("REQUEST:", allure.attachment_type.TEXT)
    allure.attach("Headers: %s ", context.response.request.headers, allure.attachment_type.TEXT)
    allure.attach("Method: %s ", context.response.request.method, allure.attachment_type.TEXT)
    allure.attach("URL: %s ", context.response.request.url, allure.attachment_type.TEXT)
    allure.attach("Body: %s ", context.response.request.bod, allure.attachment_type.TEXT)
    allure.attach("RESPONSE:", allure.attachment_type.TEXT)
    allure.attach("Status Code: %s ", context.response.status_code, allure.attachment_type.TEXT)
    allure.attach("Headers: %s ", context.response.headers, allure.attachment_type.TEXT)
    allure.attach("Body: %s ", context.response.content, allure.attachment_type.TEXT)


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
    assert_that(context.response.status_code, context).is_equal_to(
        expected_response_code
    )
