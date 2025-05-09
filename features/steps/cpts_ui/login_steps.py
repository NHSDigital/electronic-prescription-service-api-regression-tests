# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from features.environment import (
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES,
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE,
    MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT,
    MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_NO_ROLES,
)


###############################################################################
# GIVEN
###############################################################################
@given("I am on the login page")
def i_am_on_login_page(context):
    context.execute_steps("given I am on the homepage")


@given("I am logged in as a user with no roles")
def login_no_role(context):
    context.execute_steps("when I log in as a user with no roles")


@given("I am logged in as a user with a single access role")
def login_single_role(context):
    context.execute_steps("when I log in as a user with a single access role")


@given("I am logged in as a user with multiple access roles")
def login_multiple_access_roles(context):
    context.execute_steps("when I log in as a user with multiple access roles")


@given("I am logged in as a user with only roles that do not have access")
def login_without_access(context):
    context.execute_steps(
        "when I log in as a user with only roles that do not have access"
    )


@given("I am logged in as a user with a pre selected role")
def login_pre_role_selected(context):
    context.execute_steps("when I log in as a user with a pre selected role")


@given("I am logged in with a single access role and multiple without access")
def login_single_role_with_access_multiple_without(context):
    context.execute_steps(
        "when I log in with a single access role and multiple without access"
    )


###############################################################################
# WHEN
###############################################################################
@when("I log in as a user with multiple access roles")
def login_with_multiple_access_roles(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES)
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


@when("I log in as a user with no roles")
def login_with_no_roles(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_NO_ROLES)
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


@when("I log in as a user with only roles that do not have access")
def login_with_without_access(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


@when("I log in with a single access role and multiple without access")
def login_with_single_role_with_access_multiple_without(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(
        MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT
    )
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


@when("I log in as a user with a pre selected role")
def login_with_pre_role_selected(context):
    context.execute_steps("given I am on the login page")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(
        MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE
    )
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


@when("I log in as a user with a single access role")
def login_with_single_role(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


@when("The login has finished")
def the_login_is_finished(context):
    def logged_in_urls(url):
        valid_urls = [
            f"{context.cpts_ui_base_url}site/select-your-role",
            f"{context.cpts_ui_base_url}site/select-your-role/",
            f"{context.cpts_ui_base_url}site/search-by-prescription-id",
            f"{context.cpts_ui_base_url}site/search-by-prescription-id/",
        ]
        return url in valid_urls

    context.page.wait_for_url(logged_in_urls)
    context.execute_steps("then I am logged in")


###############################################################################
# THEN STEPS
###############################################################################
@then("I am logged in")
def i_am_logged_in(context):
    # There should be cookies with names starting with "CognitoIdentityServiceProvider"
    cookies = context.page.context.cookies()
    cognito_cookies = [
        cookie
        for cookie in cookies
        if cookie["name"].startswith("CognitoIdentityServiceProvider")
    ]
    assert len(cognito_cookies) > 0


@then("I am logged out")
def i_am_logged_out(context):
    # No cookies with names starting with "CognitoIdentityServiceProvider" should be present
    cookies = context.page.context.cookies()
    cognito_cookies = [
        cookie
        for cookie in cookies
        if cookie["name"].startswith("CognitoIdentityServiceProvider")
    ]
    assert len(cognito_cookies) == 0
