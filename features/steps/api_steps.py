# pylint: disable=missing-module-docstring
import json

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.eps_fhir.api_methods import (
    assert_ok_status_code,
    cancel_all_line_items,
    create_signed_prescription,
    prepare_prescription,
    release_signed_prescription,
    assert_ok_status_code,
    return_prescription,
)
from methods.shared import common
from methods.shared.api import request_ping
from methods.shared.common import assert_that, get_auth
from utils.nhs_number_generator import random_nhs_number_generator


@given("I successfully prepare and sign a {prescription_type} prescription")
def i_prepare_and_sign_a_prescription(context, prescription_type="nominated"):
    i_prepare_a_new_prescription(context, prescription_type)
    i_sign_a_new_prescription(context=context)


@given("a prescription has been created and released")
def a_prescription_has_been_created_and_released(context):
    i_am_an_authorised_user(context, "prescriber")
    i_prepare_and_sign_a_prescription(context)
    i_am_an_authorised_user(context, "dispenser")
    i_release_a_prescription(context)
    indicate_successful_response(context)


@given("I am an authorised {user}")
@when("I am an authorised {user}")
def i_am_an_authorised_user(context, user):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    env = context.config.userdata["env"]
    context.user = user
    context.auth_token = get_auth(user, env)


def i_prepare_a_new_prescription(context, prescription_type):
    context.nhs_number = random_nhs_number_generator()
    if prescription_type == "non-nominated":
        context.nomination_code = "0004"
    if prescription_type == "nominated":
        context.nomination_code = "P1"
    prepare_prescription(context)


def i_sign_a_new_prescription(context):
    create_signed_prescription(context)


@when("I release a prescription")
def i_release_a_prescription(context):
    release_signed_prescription(context)


@when("I return the prescription")
def i_return_the_prescription(context):
    return_prescription(context)


@then("the response indicates success")
@when("I cancel all line items on the prescription")
def i_cancel_all_line_items(context):
    cancel_all_line_items(context)


@then("the response indicates a success")
def indicate_successful_response(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    assert_ok_status_code(context)


@then("the response body indicates a successful {action_type} action")
def body_indicates_successful_action(context, action_type):
    def _prescribe_assertion():
        assert_that(json_response["parameter"][0]["resource"]["total"]).is_equal_to(1)

    def _cancel_assertion():
        entries = json_response["entry"]
        message_header = [
            entry
            for entry in entries
            if entry["resource"]["resourceType"] == "MessageHeader"
        ][0]
        assert_that(message_header["resource"]["response"]["code"]).is_equal_to("ok")

    json_response = json.loads(context.response.content)
    action_assertions = {
        "prescribe": [_prescribe_assertion],
        "cancel": [_cancel_assertion],
    }
    [assertion() for assertion in action_assertions.get(action_type, [])]


@when('I make a request to the "{product}" ping endpoint')
def i_make_a_request_to_the_ping_endpoint(context, product):
    base_url = None
    if product == "pfp_apigee":
        base_url = context.pfp_apigee_base_url
    if product == "eps_fhir":
        base_url = context.eps_fhir_base_url
    if base_url is not None:
        request_ping(context, base_url)
    else:
        raise ValueError(f"unable to find base url for '{product}'")


@then("I get a {status_code:n} response code")
def i_get_a_status_code(context, status_code: int):
    common.the_expected_response_code_is_returned(context, status_code)


@then("I can see the version information in the response")
def i_see_version_in_response(context):
    response = context.response.json()
    assert_that(response["version"]).is_not_none()
    assert_that(response["version"]).is_not_empty()


@then("I can see the revision information in the response")
def i_see_revision_in_response(context):
    response = context.response.json()
    assert_that(response["revision"]).is_not_none()
    assert_that(response["revision"]).is_not_empty()


@then("I can see the releaseId information in the response")
def i_see_release_id_in_response(context):
    response = context.response.json()
    assert_that(response["releaseId"]).is_not_none()
    assert_that(response["releaseId"]).is_not_empty()


@then("I can see the commitId information in the response")
def i_see_commit_id_in_response(context):
    response = context.response.json()
    assert_that(response["commitId"]).is_not_none()
    assert_that(response["commitId"]).is_not_empty()


@then("I can see the ping information in the response")
def i_can_see_the_ping_information(context):
    i_see_version_in_response(context)
    i_see_revision_in_response(context)
    i_see_release_id_in_response(context)
    i_see_commit_id_in_response(context)


@then("I can see the prescription in the response")
def i_can_see_the_prescription_in_the_response(context):
    json_response = json.loads(context.response.content)
    assert_that(json_response["parameter"][0]["resource"]["total"]).is_equal_to(1)


@then("I can see an informational operation outcome in the response")
def i_can_see_an_informational_operation_outcome_in_the_response(context):
    json_response = json.loads(context.response.content)
    assert_that(json_response["resourceType"]).is_equal_to("OperationOutcome")
    assert_that(json_response["issue"][0]["code"]).is_equal_to("informational")
    assert_that(json_response["issue"][0]["severity"]).is_equal_to("information")
