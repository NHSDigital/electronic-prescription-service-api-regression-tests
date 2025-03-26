# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.cpts_api_methods import (
    get_prescription_list,
    assert_prescription_list,
    assert_empty_prescription_list,
    assert_both_identifier_error,
    get_prescription_details,
    get_prescription_not_found,
    get_path_parameter_not_provided,
    assert_prescription_details,
    assert_prescription_not_found,
    assert_path_parameter_not_provided,
)


@when("I request the list of prescriptions using the {identifier}")
def request_prescription_list(context, identifier):
    get_prescription_list(context, identifier)


@when("I request the list of prescriptions that don't exist using the {identifier}")
def request_empty_prescription_list(context, identifier):
    context.nhs_number = "3152699093"
    context.prescription_id = "EBA388-000X26-44ABAC"
    get_prescription_list(context, identifier)


@then("I can see the list of prescriptions")
def verify_prescription_list(context):
    assert_prescription_list(context)


@then("I see an empty list in the response")
def verify_empty_prescription_list(context):
    assert_empty_prescription_list(context)


@then("I am informed not to include both identifiers")
def verify_both_identifier_error(context):
    assert_both_identifier_error(context)


@when("I request the prescription details")
def request_prescription_details(context):
    get_prescription_details(context)


@when("I request the prescription details with a non-existent prescription id")
def request_prescription_details_with_incorrect_prescription_id(context):
    get_prescription_not_found(context)


@when("I request the prescription details without a path parameter")
def request_prescription_details_without_path_parameter(context):
    get_path_parameter_not_provided(context)


@then("I can see the prescription details")
def verify_prescription_details(context):
    assert_prescription_details(context)


@then("I can see the prescription not found message")
def i_can_see_prescription_not_found_message(context):
    assert_prescription_not_found(context)


@then("I can see the missing required path parameter message")
def i_can_see_missing_required_path_parameter_message(context):
    assert_path_parameter_not_provided(context)
