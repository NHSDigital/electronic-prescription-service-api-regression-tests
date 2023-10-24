# pylint: disable=no-member,no-name-in-module
from behave import then, when  # type: ignore

from methods import api_methods


@when("I make a request to the ping endpoint")
def i_make_a_request_to_the_ping_endpoint(context):
    api_methods.request_ping(context)


@then("I get a {status_code:n} response code")
def i_get_a_status_code(context, status_code: int):
    api_methods.the_expected_response_code_is_returned(context, status_code)
