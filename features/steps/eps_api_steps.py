import json

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.eps_api_methods import (
    cancel_all_line_items,
    create_signed_prescription,
    dispense_prescription,
    dispense_erd_prescription,
    amend_dispense_notification,
    prepare_prescription,
    try_prepare_prescription,
    release_signed_prescription,
    return_prescription,
    withdraw_dispense_notification,
    call_validator,
)
from features.environment import APIGEE_APPS
from methods.shared.common import assert_that, get_auth
from utils.random_nhs_number_generator import generate_single
from messages.eps_fhir.prescription import Prescription
from jycm.jycm import YouchamaJsonDiffer


def setup_new_prescription(context, nomination, prescription_type):
    context.nhs_number = generate_single()
    if nomination == "non-nominated":
        context.nomination_code = "0004"
    if nomination == "nominated":
        context.nomination_code = "P1"
    if prescription_type == "acute":
        context.type_code = "acute"
        context.intent = "order"
    if prescription_type == "repeat":
        context.type_code = "continuous"
        context.intent = "instance-order"
    if prescription_type == "eRD":
        context.type_code = "continuous-repeat-dispensing"
        context.intent = "original-order"


@given("I successfully prepare and sign a prescription")
def i_prepare_and_sign_a_prescription(context):
    if (
        "sandbox" in context.config.userdata["env"].lower()
        and context.config.userdata["product"].upper() != "EPS-FHIR"
    ):
        return
    context.execute_steps(
        """
        Given I successfully prepare a nominated acute prescription
        When I sign the prescription
        """
    )


@given(
    "I successfully prepare and sign a {nomination} {prescription_type} prescription"
)
def i_prepare_and_sign_a_type_prescription(context, nomination, prescription_type):
    context.execute_steps(
        f"""
        Given I successfully prepare a {nomination} {prescription_type} prescription
        When I sign the prescription
        """
    )


@given("a {nomination} {prescription_type} prescription has been created")
def a_proxygen_prescription_has_been_created(context, nomination, prescription_type):
    a_prescription_has_been_created(context, nomination, prescription_type, "proxygen")


@given(
    "a {nomination} {prescription_type} prescription has been created using {deployment_method} apis"
)
def a_prescription_has_been_created(
    context, nomination, prescription_type, deployment_method
):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    if deployment_method == "apim":
        prescribe_product = "EPS-FHIR"
    elif deployment_method == "proxygen":
        prescribe_product = "EPS-FHIR-PRESCRIBING"
    else:
        raise ValueError(f"Unknown deployment_method {deployment_method}")
    context.execute_steps(
        f"""
        Given I am an authorised prescriber with {prescribe_product} app
        And I successfully prepare a {nomination} {prescription_type} prescription
        When I sign the prescription
        """
    )


@given("a {nomination} {prescription_type} prescription has been created and released")
def a_proxygen_prescription_has_been_created_and_released(
    context, nomination, prescription_type
):
    a_prescription_has_been_created_and_released(
        context, nomination, prescription_type, "proxygen"
    )


@given(
    "a {nomination} {prescription_type} prescription has been created and released to {receiver_ods_code}"
)
def a_proxygen_prescription_has_been_created_and_released_to(
    context, nomination, prescription_type, receiver_ods_code
):
    context.execute_steps(
        f"Given a {nomination} {prescription_type} prescription has been created using proxygen apis"
    )
    context.receiver_ods_code = receiver_ods_code
    context.execute_steps(
        "Given the prescription has been released using proxygen apis"
    )


@given(
    "a {nomination} {prescription_type} prescription has been created and released using {deployment_method} apis"
)
def a_prescription_has_been_created_and_released(
    context, nomination, prescription_type, deployment_method
):
    context.execute_steps(
        f"""
        Given a {nomination} {prescription_type} prescription has been created using {deployment_method} apis
        And the prescription has been released using {deployment_method} apis
        """
    )


@given("the prescription has been released using {deployment_method} apis")
def the_prescription_has_been_released(context, deployment_method):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    if deployment_method == "apim":
        dispense_product = "EPS-FHIR"
    elif deployment_method == "proxygen":
        dispense_product = "EPS-FHIR-DISPENSING"
    else:
        raise ValueError(f"Unknown deployment_method {deployment_method}")
    context.execute_steps(
        f"""
        Given I am an authorised dispenser with {dispense_product} app
        When I release the prescription
        """
    )


@given("a new prescription has been dispensed")
def a_proxygen_prescription_has_been_dispensed(context):
    a_new_prescription_has_been_dispensed(context, "proxygen")


@given("a new prescription has been dispensed using {deployment_method} apis")
def a_new_prescription_has_been_dispensed(context, deployment_method):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    context.execute_steps(
        f"""
        Given a nominated acute prescription has been created and released using {deployment_method} apis
        When I dispense the prescription
        """
    )


@given("the prescription has been cancelled")
def the_proxygen_prescription_has_been_cancelled(context):
    context.execute_steps(
        """
        Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
        When I cancel all line items on the prescription
        """
    )


@given("I am an authorised {user} with {app} app")
@when("I am an authorised {user} with {app} app")
def i_am_an_authorised_user(context, user, app):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    env = context.config.userdata["env"]
    print(user)
    if user == "api user":
        context.api_key = APIGEE_APPS[app]["client_id"]
        context.auth_method = "api_key"
    else:
        context.user = user
        context.auth_token = get_auth(env, app, user)
        context.auth_method = "oauth2"


@given("I successfully prepare a {nomination} {prescription_type} prescription")
def i_prepare_a_new_prescription(context, nomination, prescription_type):
    setup_new_prescription(context, nomination, prescription_type)
    prepare_prescription(context)


# TODO: create deleted prescription step


@when("I try to prepare a {nomination} {prescription_type} prescription")
def i_try_to_prepare_a_new_prescription(context, nomination, prescription_type):
    setup_new_prescription(context, nomination, prescription_type)
    try_prepare_prescription(context)


@when("I sign the prescription")
def i_sign_a_new_prescription(context):
    create_signed_prescription(context)


@when("I try to release the prescription")
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
    if context.type_code == "continuous-repeat-dispensing":
        dispense_erd_prescription(context)
    else:
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
        context.intent = "order"
        context.type_code = "acute"
        validate_body = Prescription(context).body
    else:
        validate_body = "foo"
    call_validator(context, product, show_validation, validate_body)


@when("I make a request with file {filename} to the {product} validator endpoint")
def i_make_a_request_to_the_validator_endpoint_with_file(context, filename, product):
    with open(f"messages/examples/{filename}") as f:
        validate_body = json.load(f)
    call_validator(context, product, "unset", json.dumps(validate_body))


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
    with open(f"messages/examples/{filename}") as f:
        expected_response = json.load(f)
    json_response = json.loads(context.response.content)
    # create the YouChaMa (ycm) json diff class with expected and actual response
    ycm = YouchamaJsonDiffer(expected_response, json_response)
    # get the differences
    diff_result = ycm.get_diff()
    # and there should be none
    assert_that(diff_result).is_equal_to({"just4vis:pairs": []})


@then("the signing algorithm is {algorithm}")
def the_signing_algorithm_is(context, algorithm):
    assert_that(algorithm).is_equal_to(context.algorithm)
