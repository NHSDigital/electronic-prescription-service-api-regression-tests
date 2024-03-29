from behave import then, when  # pyright: ignore [reportAttributeAccessIssue]

from methods.shared import common
from methods.shared.api import request_ping
from methods.shared.common import assert_that


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


@then("I can see the revision information in the response")
def i_see_revision_in_response(context):
    response = context.response.json()
    assert_that(response["revision"]).is_not_none()


@then("I can see the releaseId information in the response")
def i_see_release_id_in_response(context):
    response = context.response.json()
    assert_that(response["releaseId"]).is_not_none()


@then("I can see the commitId information in the response")
def i_see_commit_id_in_response(context):
    response = context.response.json()
    assert_that(response["commitId"]).is_not_none()


@then("I can see the ping information in the response")
def step_impl(context):
    i_see_version_in_response(context)
    i_see_revision_in_response(context)
    i_see_release_id_in_response(context)
    i_see_commit_id_in_response(context)
