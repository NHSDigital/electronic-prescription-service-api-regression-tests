# pylint: disable=no-name-in-module
from behave import when, then, step  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.cpts_api_methods import (
    get_prescription_list,
    assert_prescription_list,
    assert_empty_prescription_list,
    assert_both_identifier_error,
    get_prescription_details,
    assert_prescription_details,
    assert_prescription_not_found,
    assert_path_parameter_not_provided,
    PrescriptionDetailsAssertions,
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
    get_prescription_details(context, None)


@when("I request the prescription details with an issue number")
def request_prescription_details_with_issue_number(context):
    get_prescription_details(context, 2)


@when("I request the prescription details with a non-existent prescription id")
def request_prescription_details_with_incorrect_prescription_id(context):
    context.prescription_id = "F281C0-000X26-4811B5"
    get_prescription_details(context, None)


@when("I request the prescription details without a path parameter")
def request_prescription_details_without_path_parameter(context):
    context.prescription_id = ""
    get_prescription_details(context, None)


@then("I can see the prescription details")
def verify_prescription_details(context):
    assertions: PrescriptionDetailsAssertions = {
        "prescription_id": context.prescription_id,
        "nhs_number": context.nhs_number,
        "status": "To Be Dispensed",
    }
    assert_prescription_details(context.response.content, assertions)


@step("I can see the prescription details with the correct issue details")
def verify_prescription_issue_details(context):
    assertions: PrescriptionDetailsAssertions = {
        "prescription_id": context.prescription_id,
        "nhs_number": context.nhs_number,
        "status": "To Be Dispensed",
        "issue_number": 2,
    }
    assert_prescription_details(context.response.content, assertions)


@step(
    'I can see the prescription details with the correct "{reason}" non-dispensing reason'
)
def verify_prescription_non_dispensing_reason(context, reason):
    assertions: PrescriptionDetailsAssertions = {
        "prescription_id": context.prescription_id,
        "nhs_number": context.nhs_number,
        "status": "Not Dispensed",
        "medication_dispenses": [
            {
                "md_id": context.dispense_notification_id,
                "line_item_id": context.prescription_item_id,
                "status": "Item not dispensed",
                "non_dispensing_reason": reason,
            }
        ],
    }
    assert_prescription_details(context, assertions)


@step(
    'I can see the prescription details with the correct "{reason}" cancellation reason'
)
def verify_prescription_cancellation_reason(context, reason):
    assertions: PrescriptionDetailsAssertions = {
        "prescription_id": context.prescription_id,
        "nhs_number": context.nhs_number,
        "status": "Cancelled",
        "medication_requests": [
            {
                "line_item_id": context.prescription_item_id,
                "status": "Item Cancelled",
                "cancellation_reason": reason,
            }
        ],
    }
    assert_prescription_details(context, assertions)


@then("I can see the prescription not found message")
def i_can_see_prescription_not_found_message(context):
    assert_prescription_not_found(context)


@then("I can see the missing required path parameter message")
def i_can_see_missing_required_path_parameter_message(context):
    assert_path_parameter_not_provided(context)
