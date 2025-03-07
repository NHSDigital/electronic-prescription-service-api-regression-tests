
# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.cpts_api_methods import (
  get_prescription_list
  assert_prescription_list
)

@when("When I request the list of prescriptions using the {}")
def request_prescription_list(context, identifier)
  get_prescription_list(context, identifier)

@then("I can see the list of prescriptions")
def verify_prescription_list(context)
  assert_prescription_list(context)
