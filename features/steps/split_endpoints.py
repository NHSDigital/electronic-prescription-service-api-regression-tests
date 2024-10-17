import json

# import os
# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from features.steps.common_steps import indicate_successful_response
from methods.api.eps_split_endpoints_api_methods import (
    create_signed_prescription_prescribing_endpoint,
    release_signed_prescription_prescribing_endpoint,
    dispense_prescription_dispensing_endpoint,
    prepare_prescription_prescribing_endpoint,
    return_prescription_dispensing_endpoint,
    withdraw_dispense_notification_dispensing_endpoint,
    amend_dispense_notification_dispensing_endpoint,
    cancel_all_line_items_prescribing_endpoint,
)
from methods.shared.common import assert_that, get_auth
from utils.random_nhs_number_generator import generate_single

# @given("I am using the split endpoints")
# def using_split_endpoints(context):
#     context.prescribing_endpoint = os.getenv('PRESCRIBING_ENDPOINT')
#     context.dispensing_endpoint = os.getenv('DISPENSING_ENDPOINT')
#     assert context.prescribing_endpoint, "PRESCRIBING_ENDPOINT is not set"
#     assert context.dispensing_endpoint, "DISPENSING_ENDPOINT is not set"


@given("I successfully prepare and sign a prescription using the prescribing endpoint")
def i_prepare_and_sign_prescription_prescribing(context, prescription_type):
    if (
        "sandbox" in context.config.userdata["env"].lower()
        and context.config.userdata["product"].upper() != "EPS-FHIR-PRESCRIBING"
    ):
        return
    i_prepare_a_new_prescription_prescribing_endpoint(context, prescription_type)
    i_sign_a_new_prescription_prescribing_endpoint(context)


@given("I successfully prepare and sign a {prescription_type} prescription")
def i_prepare_and_sign_a_type_prescription_prescribing_endpoint(
    context, prescription_type
):
    i_prepare_a_new_prescription_prescribing_endpoint(context, prescription_type)
    i_sign_a_new_prescription_prescribing_endpoint(context=context)


@given("a prescription has been created and released")
def a_prescription_has_been_created_and_released(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    i_am_an_authorised_prescriber(context, "prescriber")
    i_prepare_and_sign_prescription_prescribing(context, "prescriber")
    i_am_an_authorised_dispenser(context, "dispenser")
    i_release_the_prescription_prescribing_endpoint(context)
    indicate_successful_response(context)


@given("a new prescription has been dispensed")
def a_new_prescription_has_been_dispensed_dispensing_endpoint(context):
    a_prescription_has_been_created_and_released(context)
    i_dispense_the_prescription_dispensing_endpoint(context)
    indicate_successful_response(context)


@given("I am an authorised prescriber")
def i_am_an_authorised_prescriber(context, user):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    env = context.config.userdata["env"]
    context.user = user
    context.auth_token = get_auth(env, "EPS-FHIR-PRESCRIBING", user)


@when("I am an authorised dispenser")
def i_am_an_authorised_dispenser(context, user):
    context.auth = get_auth(context, "dispenser")
    if "sandbox" in context.config.userdata["env"].lower():
        return
    env = context.config.userdata["env"]
    context.user = user
    context.auth_token = get_auth(env, "EPS-FHIR-DISPENSING", user)


def i_prepare_a_new_prescription_prescribing_endpoint(context, prescription_type):
    context.nhs_number = generate_single()
    if prescription_type == "non-nominated":
        context.nomination_code = "0004"
    if prescription_type == "nominated":
        context.nomination_code = "P1"
    prepare_prescription_prescribing_endpoint(context)


def i_sign_a_new_prescription_prescribing_endpoint(context):
    create_signed_prescription_prescribing_endpoint(context)


@when("I release the prescription with the prescribing endpoint")
def i_release_the_prescription_prescribing_endpoint(context):
    release_signed_prescription_prescribing_endpoint(context)


@when("I return the prescription with the prescribing endpoint")
def i_return_the_prescription_prescribing_endpoint(context):
    return_prescription_dispensing_endpoint(context)


@when("I cancel all line items on the prescription with the prescribing endpoint")
def i_cancel_all_line_items_prescribing_endpoint(context):
    cancel_all_line_items_prescribing_endpoint(context)


@when("I dispense the prescription with the dispensing endpoint")
def i_dispense_the_prescription_dispensing_endpoint(context):
    dispense_prescription_dispensing_endpoint(context)


@when("I amend the dispense notification with the dispensing endpoint")
def i_amend_a_dispense_notification_dispensing_endpoint(context):
    amend_dispense_notification_dispensing_endpoint(context)


@when("I withdraw the dispense notification with the dispensing endpoint")
def i_withdraw_the_dispense_notification_dispensing_endpoint(context):
    withdraw_dispense_notification_dispensing_endpoint(context)


@then(
    "the response body indicates a successful {action_type} action with the dispensing endpoint"
)
def body_indicates_successful_action(context, action_type):
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
        if "sandbox" in context.config.userdata["env"].lower():
            return
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
