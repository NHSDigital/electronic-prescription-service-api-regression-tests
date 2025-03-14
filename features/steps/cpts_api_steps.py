# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.cpts_api_methods import (
    get_prescription_details,
    get_prescription_not_found_message,
    assert_prescription_details,
    assert_prescription_not_found,
)


@when("I request the prescription details")
def request_prescription_details(context):
    get_prescription_details(context)


@when("I request the prescription details with a non-existent prescription id")
def request_prescription_details_with_incorrect_prescription_id(context):
    get_prescription_not_found_message(context)


@then("I can see the prescription details")
def verify_prescription_details(context):
    assert_prescription_details(context)


@then("I can see the prescription not found message")
def i_can_see_prescription_not_found_message(context):
    assert_prescription_not_found(context)
