# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.shared import common
from methods.api.common_api_methods import request_ping
from methods.api.common_api_methods import request_metadata
from methods.shared.common import assert_that
from playwright.sync_api import Route


@when('I make a request to the "{product}" ping endpoint')
def i_make_a_request_to_the_ping_endpoint(context, product):
    base_url = None
    if product == "pfp":
        base_url = context.pfp_base_url
    if product == "eps_fhir":
        base_url = context.eps_fhir_base_url
    if product == "eps_fhir_prescribing":
        base_url = context.eps_fhir_prescribing_base_url
    if product == "eps_fhir_dispensing":
        base_url = context.eps_fhir_dispensing_base_url
    if product == "cpts_fhir":
        base_url = context.cpts_fhir_base_url
    if base_url is not None:
        request_ping(context, base_url)
    else:
        raise ValueError(f"unable to find base url for '{product}'")


@when('I make a request to the "{product}" metadata endpoint')
def i_make_a_request_to_the_metadata_endpoint(context, product):
    base_url = None
    if product == "pfp":
        base_url = context.pfp_base_url
    if product == "eps_fhir":
        base_url = context.eps_fhir_base_url
    if product == "eps_fhir_prescribing":
        base_url = context.eps_fhir_prescribing_base_url
    if product == "eps_fhir_dispensing":
        base_url = context.eps_fhir_dispensing_base_url
    if product == "cpts_fhir":
        base_url = context.cpts_fhir_base_url
    if base_url is not None:
        request_metadata(context, base_url)
    else:
        raise ValueError(f"unable to find base url for '{product}'")


@then("the response indicates a success")
def indicate_successful_response(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    common.the_expected_response_code_is_returned(context, 200)


@then("the response indicates unauthorised")
def indicate_unauthorised_response(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    common.the_expected_response_code_is_returned(context, 401)


@then("the response indicates a record was created")
def indicate_record_created(context):
    common.the_expected_response_code_is_returned(context, 201)


@then("the response indicates a bad request")
def indicate_bad_request_response(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    common.the_expected_response_code_is_returned(context, 400)


@then("the response indicates not found resource")
def indicate_not_found_response(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    common.the_expected_response_code_is_returned(context, 404)


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


@then("the {code:d} error occurs")
def simulate_http_error(context, code):
    def handler(route: Route):
        # Simulate an HTTP error only for the prescription-list API endpoint
        route.fulfill(status=code, body=f"{code} error")

    # Limit interception to requests hitting the prescription-list endpoint
    context.page.route("**/prescription-list*", handler)


@then('I see a go back link to "{target_path}"')
def see_go_back_link_to(context, target_path):
    back_link = context.page.get_by_test_id("go-back-link")
    assert back_link is not None, "No go-back-link found on the page"

    href = back_link.get_attribute("href")
    assert (
        href and target_path in href
    ), f"Expected go-back link to contain '{target_path}', but got '{href}'"
