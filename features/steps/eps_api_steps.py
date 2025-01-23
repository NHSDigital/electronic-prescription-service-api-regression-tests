import json

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from features.steps.common_steps import indicate_successful_response
from methods.api.eps_api_methods import (
    cancel_all_line_items,
    create_signed_prescription,
    dispense_prescription,
    amend_dispense_notification,
    prepare_prescription,
    release_signed_prescription,
    return_prescription,
    withdraw_dispense_notification,
    call_validator,
)
from methods.shared.common import assert_that, get_auth
from utils.random_nhs_number_generator import generate_single
from messages.eps_fhir.prescription import Prescription


@given("I successfully prepare and sign a prescription")
def i_prepare_and_sign_a_prescription(context):
    if (
        "sandbox" in context.config.userdata["env"].lower()
        and context.config.userdata["product"].upper() != "EPS-FHIR"
    ):
        return
    i_prepare_a_new_prescription(context, "nominated")
    i_sign_a_new_prescription(context=context)


@given("I successfully prepare and sign a {prescription_type} prescription")
def i_prepare_and_sign_a_type_prescription(context, prescription_type):
    i_prepare_a_new_prescription(context, prescription_type)
    i_sign_a_new_prescription(context=context)


@given("a prescription has been created and released")
def a_prescription_has_been_created_and_released(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    i_am_an_authorised_user(context, "prescriber")
    i_prepare_and_sign_a_prescription(context)
    i_am_an_authorised_user(context, "dispenser")
    i_release_the_prescription(context)
    indicate_successful_response(context)


@given("a new prescription has been dispensed")
def a_new_prescription_has_been_dispensed(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    a_prescription_has_been_created_and_released(context)
    i_dispense_the_prescription(context)
    indicate_successful_response(context)


@given("I am an authorised {user}")
@when("I am an authorised {user}")
def i_am_an_authorised_user(context, user):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    env = context.config.userdata["env"]
    context.user = user
    context.auth_token = get_auth(env, "EPS-FHIR", user)


def i_prepare_a_new_prescription(context, prescription_type):
    context.nhs_number = generate_single()
    if prescription_type == "non-nominated":
        context.nomination_code = "0004"
    if prescription_type == "nominated":
        context.nomination_code = "P1"
    prepare_prescription(context)


def i_sign_a_new_prescription(context):
    create_signed_prescription(context)


@when("I release the prescription")
def i_release_the_prescription(context):
    release_signed_prescription(context)


@when("I return the prescription")
def i_return_the_prescription(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    return_prescription(context)


@when("I cancel all line items on the prescription")
def i_cancel_all_line_items(context):
    cancel_all_line_items(context)


@when("I dispense the prescription")
def i_dispense_the_prescription(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    dispense_prescription(context)


@when("I amend the dispense notification")
def i_amend_a_dispense_notification(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    amend_dispense_notification(context)


@when("I withdraw the dispense notification")
def i_withdraw_the_dispense_notification(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    withdraw_dispense_notification(context)


@then("the response body indicates a successful {action_type} action")
def body_indicates_successful_action(context, action_type):
    if "sandbox" in context.config.userdata["env"].lower():
        return

    def _withdraw_dispense_notification_assertion():
        i_can_see_an_informational_operation_outcome_in_the_response(context)

    def _cancel_assertion():
        entries = json_response["entry"]
        medication_request = [
            entry
            for entry in entries
            if entry["resource"]["resourceType"] == "MedicationRequest"
        ][0]
        assert_that(
            medication_request["resource"]["extension"][0]["extension"][0][
                "valueCoding"
            ]["display"]
        ).is_equal_to("Prescription/item was cancelled")

    def _dispense_assertion():
        i_can_see_an_informational_operation_outcome_in_the_response(context)

    def _amend_dispense_assertion():
        i_can_see_an_informational_operation_outcome_in_the_response(context)

    def _release_assertion():
        assert_that(json_response["parameter"][0]["resource"]["total"]).is_equal_to(1)

    def _return_assertion():
        i_can_see_an_informational_operation_outcome_in_the_response(context)

    json_response = json.loads(context.response.content)
    action_assertions = {
        "cancel": [_cancel_assertion],
        "dispense": [_dispense_assertion],
        "amend dispense": [_amend_dispense_assertion],
        "dispense withdrawal": [_withdraw_dispense_notification_assertion],
        "release": [_release_assertion],
        "return": [_return_assertion],
    }
    [assertion() for assertion in action_assertions.get(action_type, [])]


@then("I can see an informational operation outcome in the response")
def i_can_see_an_informational_operation_outcome_in_the_response(context):
    json_response = json.loads(context.response.content)
    assert_that(json_response["resourceType"]).is_equal_to("OperationOutcome")
    assert_that(json_response["issue"][0]["code"]).is_equal_to("informational")
    assert_that(json_response["issue"][0]["severity"]).is_equal_to("information")


@when(
    "I make a {validity} request to the {product} validator endpoint with show validation set to {show_validation}"
)
def i_make_a_request_to_the_validator_endpoint(
    context, validity, product, show_validation
):
    if validity == "valid":
        context.nhs_number = generate_single()
        context.nomination_code = "0004"
        validate_body = Prescription(context).body
    else:
        validate_body = "foo"
    call_validator(context, product, show_validation, validate_body)


@when("I make a request with file {filename} to the {product} validator endpoint")
def i_make_a_request_to_the_validator_endpoint_with_file(context, filename, product):
    with open(f"../../messages/examples/{filename}") as f:
        validate_body = json.load(f)
    call_validator(context, product, "unset", validate_body)


@then("the validator response has {expected_issue_count} {issue_type} issue")
def validator_response_has_n_issues_of_type(context, expected_issue_count, issue_type):
    json_response = json.loads(context.response.content)
    assert_that(json_response["resourceType"]).is_equal_to("OperationOutcome")
    actual_issue_count = sum(
        p["severity"] == issue_type for p in json_response["issue"]
    )
    if expected_issue_count == "many":
        assert_that(actual_issue_count).is_greater_than(0)
    else:
        assert_that(int(expected_issue_count)).is_equal_to(actual_issue_count)


@then("the validator response has error with diagnostic containing {diagnostic}")
def validator_response_has_error_issue_with_diagnostic(context, diagnostic):
    json_response = json.loads(context.response.content)
    assert_that(json_response["resourceType"]).is_equal_to("OperationOutcome")
    print(f"expected diagnostic: {diagnostic}")
    actual_issue_count = sum(
        p["severity"] == "error" and diagnostic in p["diagnostics"]
        for p in json_response["issue"]
    )
    assert_that(actual_issue_count).is_equal_to(1)


@then("the validator response matches {filename}")
def validator_response_matches_file(context, filename):
    with open(f"../../messages/examples/{filename}") as f:
        expected_response = json.load(f)
    json_response = json.loads(context.response.content)
    assert_that(json_response).is_equal_to(expected_response)
