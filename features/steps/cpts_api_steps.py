# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.cpts_api_methods import (
    get_prescription_details,
    assert_prescription_details,
)


@when("I request the prescription details")
def request_prescription_details(context):
    get_prescription_details(context)


@then("I can see the prescription details")
def verify_prescription_details(context):
    assert_prescription_details(context)
