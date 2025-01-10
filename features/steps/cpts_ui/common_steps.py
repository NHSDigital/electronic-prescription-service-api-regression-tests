# pylint: disable=no-name-in-module
from behave import given, then  # pyright: ignore [reportAttributeAccessIssue]

from features.environment import (
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES,
    MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE,
)


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


# @given("I am logged in") #AEA-4809
# def login(context):
#     # TODO: This /site/ is not generic. Also, the .html will need to be removed when the SPA is fixed
#     context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
#     context.page.get_by_role("button", name="Log in with mock CIS2").click()
#     context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES)
#     context.page.get_by_role("button", name="Sign In").click()
#     context.page.wait_for_url("**/selectyourrole.html")

#     # There should be cookies with names starting with "CognitoIdentityServiceProvider"
#     cookies = context.page.context.cookies()
#     cognito_cookies = [
#         cookie
#         for cookie in cookies
#         if cookie["name"].startswith("CognitoIdentityServiceProvider")
#     ]
#     assert len(cognito_cookies) > 0


@given("I am logged in")
def login(context):
    context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url("**/selectyourrole.html")


@given("I am logged in without access")
def login_without_access(context):
    context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url("**/selectyourrole.html")


@then("I am on the login page")
def i_am_on_login_page(context):
    # TODO: This needs to cover the .html for the broken SPA. Will need to be removed.
    assert context.page.url == context.cpts_ui_base_url + "site/login"
