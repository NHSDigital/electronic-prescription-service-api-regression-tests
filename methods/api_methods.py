import uuid
import allure
import requests
from assertpy import assert_that as assertpy_assert  # type: ignore


def assert_that(expected, context):
    allure.attach(str(expected), "Expected", allure.attachment_type.TEXT)
    allure.attach(str(context.response), "Actual", allure.attachment_type.TEXT)
    description = (
        f"Actual Response: Status Code: {context.response.status_code}, "
        f"Body: {context.response.content}"
    )
    return assertpy_assert(expected, description=description)


def attach_api_information(context):
    allure.attach(str(context.response.request.headers), "REQUEST Headers", allure.attachment_type.TEXT)
    allure.attach(str(context.response.request.method), "REQUEST Method", allure.attachment_type.TEXT)
    allure.attach(str(context.response.request.url), "REQUEST URL", allure.attachment_type.TEXT)
    allure.attach(str(context.response.request.body), "REQUEST Body", allure.attachment_type.TEXT)
    allure.attach(str(context.response.status_code), "RESPONSE Status Code", allure.attachment_type.TEXT)
    allure.attach(str(context.response.headers), "RESPONSE Headers", allure.attachment_type.TEXT)
    allure.attach(str(context.response.content), "RESPONSE Body", allure.attachment_type.TEXT)


def get_default_headers():
    return {
        "x-request-id": str(uuid.uuid4()),
        "x-user-org-code": "Auto001",
    }


def request_ping(context):
    url = f"{context.fhir_base_url}/_ping"
    print(f"going to {url}")
    context.response = requests.get(url=url)
    # attach_api_information(context)


def the_expected_response_code_is_returned(context, expected_response_code: int):
    assert_that(context.response.status_code, context).is_equal_to(
        expected_response_code
    )
