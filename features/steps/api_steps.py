from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.eps_fhir.api_methods import (
    prepare_prescription,
    create_signed_prescription,
)
from methods.shared import common
from methods.shared.api import request_ping
from methods.shared.common import assert_that, get_auth
from utils.nhs_number_generator import random_nhs_number_generator


@given("I am an authorised {user}")
@when("I am an authorised {user}")
def i_am_an_authorised_user(context, user):
    env = context.config.userdata["env"]
    context.auth_token = get_auth(user, env)


@given("I successfully prepare, sign and send a {prescription_type} prescription")
def i_prepare_sign_release_a_prescription(context, prescription_type):
    i_prepare_a_new_prescription(context, prescription_type)
    i_sign_a_new_prescription(context=context)
    # raise NotImplementedError(
    #     "STEP: And I successfully prepare, sign and send a <Type> prescription"
    # )


def i_prepare_a_new_prescription(context, prescription_type):
    context.nhs_number = random_nhs_number_generator()
    if prescription_type == "non-nominated":
        context.nomination_code = "0004"
    prepare_prescription(context)


def i_sign_a_new_prescription(context):
    create_signed_prescription(context)


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
