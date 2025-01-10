# pylint: disable=no-name-in-module
import re
from behave import given, then  # pyright: ignore [reportAttributeAccessIssue]

from features.environment import (
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES,
    MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE,
)

select_your_role_url_pattern = re.compile(r".*/selectyourrole(?:/|\.html)$")

###############################################################################
# GIVEN
###############################################################################


@given("I am on the home page")
def i_am_on_home_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/")


@given("I am on the login page")
def i_am_on_login_page(context):
    context.execute_steps("given I am on the home page")
    context.page.get_by_test_id("eps_header_placeholder2").click()


@given("I am logged in")
def login(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url(select_your_role_url_pattern)

    # There should be cookies with names starting with "CognitoIdentityServiceProvider"
    cookies = context.page.context.cookies()
    cognito_cookies = [
        cookie
        for cookie in cookies
        if cookie["name"].startswith("CognitoIdentityServiceProvider")
    ]
    assert len(cognito_cookies) > 0


@given("I am logged in without access")
def login_without_access(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url(select_your_role_url_pattern)


@given("I am logged in with a single access role")
def login_single_role(context):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url(select_your_role_url_pattern)


###############################################################################
# WHEN
###############################################################################


###############################################################################
# THEN STEPS
###############################################################################


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
