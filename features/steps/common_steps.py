# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.shared import common
from methods.api.common_api_methods import request_ping
from methods.api.common_api_methods import request_metadata

from features.environment import AWS_ROLES
from methods.shared.common import assert_that
from playwright.sync_api import Route

TAG_TO_LOGIN_MAP = {
    "single_access": "when I log in as a user with a single access role",
    "multiple_access": "when I log in as a user with multiple access roles",
    "multiple_access_pre_selected": "when I log in as a user with a pre selected role",
    "multiple_roles_no_access": "when I log in as a user with only roles that do not have access",
    "multiple_roles_single_access": "when I log in with a single access role and multiple without access",
    "no_roles_no_access": "when I log in as a user with no roles",
}


def login_by_access_tag(context):
    """
    Master function to login based on scenario tags containing '_access' or 'no_roles'.
    Automatically detects the appropriate login method from scenario tags.
    """
    current_tags = set(str(context.config.tags).split())

    # Find matching tag using set intersection - O(1) average case
    matching_tags = current_tags & TAG_TO_LOGIN_MAP.keys()

    if matching_tags:
        # Use first matching tag
        tag = next(iter(matching_tags))
        context.execute_steps(TAG_TO_LOGIN_MAP[tag])
        return

    # If no matching tag found, raise an error
    available_tags = ", ".join(f"@{tag}" for tag in TAG_TO_LOGIN_MAP.keys())
    raise AssertionError(
        f"No valid access tag found in scenario tags: {current_tags}. "
        f"Available tags: {available_tags}"
    )


def switch_browser_context(context, browser):
    # pylint: disable=broad-exception-raised
    if "concurrency" not in context.tags:
        raise Exception("Concurrency tag required for this scenario. See README.md")
    # pylint: enable=broad-exception-raised
    if browser == "primary":
        if not hasattr(context, "primary_page"):
            context.primary_page = context.primary_context.new_page()
        context.active_browser_context = context.primary_context
        context.active_page = context.primary_page

    elif browser == "concurrent":
        if not hasattr(context, "concurrent_page"):
            context.concurrent_page = context.concurrent_context.new_page()
        context.active_browser_context = context.concurrent_context
        context.active_page = context.concurrent_page

    else:
        raise ValueError(f"Unknown browser context: {browser}")


@when('I switch the browser context to "{browser}" and login again')
def switch_browser_context_and_login(context, browser):
    switch_browser_context(context, browser)
    login_by_access_tag(context)


# Switch active browser context to make use of 2 browsers
@given('I switch the browser context to "{browser}"')
@when('I switch the browser context to "{browser}"')
@then('I switch the browser context to "{browser}"')
def switch_browser_context_step(context, browser):
    switch_browser_context(context, browser)


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


@when('I directly navigate to "{route}"')
def directly_navigate_to_route(context, route):
    """Navigate directly to a protected route URL"""
    full_url = f"{context.cpts_ui_base_url}{route.lstrip('/')}"
    context.active_page.goto(full_url)
    context.active_page.wait_for_load_state("networkidle")


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


@given("I am authenticated with AWS for eps-assist-me")
def step_given(context):
    product = "eps-assist-me"
    role_arn = AWS_ROLES[product]["role_id"]
    if role_arn is None:
        raise ValueError(
            f"Role ARN for '{product}' is not set in environment variables"
        )
    context.aws_credentials = common.assume_aws_role(
        role_arn=role_arn, session_name="regression_tests"
    )


@then("the {code:d} error occurs")
def simulate_http_error(context, code):
    def handler(route: Route):
        # Simulate an HTTP error only for the prescription-list API endpoint
        route.fulfill(status=code, body=f"{code} error")

    # Limit interception to requests hitting the prescription-list endpoint
    context.active_page.route("**/prescription-list*", handler)


@then('I see a go back link to "{target_path}"')
def see_go_back_link_to(context, target_path):
    back_link = context.active_page.get_by_test_id("go-back-link")
    assert back_link is not None, "No go-back-link found on the page"

    href = back_link.get_attribute("href")
    assert (
        href and target_path in href
    ), f"Expected go-back link to contain '{target_path}', but got '{href}'"


@then('I should be redirected to "{expected_path}"')
def should_be_redirected_to_path(context, expected_path):
    """Verify user is redirected to expected path"""
    context.active_page.wait_for_load_state("networkidle", timeout=5000)
    current_url = context.active_page.url

    assert (
        expected_path in current_url
    ), f"Expected to be redirected to {expected_path}, but URL is: {current_url}"
