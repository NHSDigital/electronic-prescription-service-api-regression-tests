import logging
import uuid
import requests
from assertpy import assert_that as assertpy_assert  # type: ignore


def assert_that(expected, context):
    description = (
        f"Actual Response: Status Code: {context.response.status_code}, "
        f"Body: {context.response.content}"
    )
    return assertpy_assert(expected, description=description)


def log_api_information(context):
    logging.debug("REQUEST:")
    logging.debug("Headers: %s ", context.response.request.headers)
    logging.debug("Method: %s ", context.response.request.method)
    logging.debug("URL: %s ", context.response.request.url)
    logging.debug("Body: %s ", context.response.request.body)
    logging.debug("RESPONSE:")
    logging.debug("Status Code: %s ", context.response.status_code)
    logging.debug("Headers: %s ", context.response.headers)
    logging.debug("Body: %s ", context.response.content)


def get_default_headers():
    return {
        "x-request-id": str(uuid.uuid4()),
        "x-user-org-code": "Auto001",
    }


def request_ping(context):
    url = f"{context.base_url}/_ping"
    print(f"going to {url}")
    context.response = requests.get(url=url)
    log_api_information(context)


def the_expected_response_code_is_returned(context, expected_response_code: int):
    assert_that(context.response.status_code, context).is_equal_to(
        expected_response_code
    )
