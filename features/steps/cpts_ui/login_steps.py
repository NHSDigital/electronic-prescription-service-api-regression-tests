# pylint: disable=no-name-in-module
import time
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from features.environment import (
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES,
    MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE,
    MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT,
    MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE,
    MOCK_CIS2_LOGIN_ID_NO_ROLES,
)

from .home_steps import goto_page


###############################################################################
# GIVEN
###############################################################################
@given("I am on the login page")
def i_am_on_login_page(context):
    goto_page(context, "login")


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
# Helper functions to retry login
###############################################################################


def login(context, user_id):
    context.execute_steps("given I am on the login page")

    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(user_id)
    context.page.get_by_role("button", name="Sign In").click()

    context.execute_steps("When the login has finished")


def login_with_retries(context, user_id, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            login(context, user_id)
            break
        except Exception as e:
            if attempt == max_retries:
                raise RuntimeError("Login failed after 5 attempts") from e


###############################################################################
# WHEN
###############################################################################


@when("I log in as a user with multiple access roles")
def login_with_multiple_access_roles(context):
    current_tags = str(context.config.tags).split()
    assert (
        "multiple_access" not in current_tags
    ), f"{context.tags} : {current_tags}: Trying to use MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES in a test not tagged @multiple_access"  # noqa: E501
    login_with_retries(context, MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES)


@when("I log in as a user with no roles")
def login_with_no_roles(context):
    current_tags = str(context.config.tags).split()
    assert (
        "no_roles_no_access" not in current_tags
    ), f"{context.tags} : {current_tags}: Trying to use MOCK_CIS2_LOGIN_ID_NO_ROLES in a test not tagged @no_roles_no_access"  # noqa: E501
    login_with_retries(context, MOCK_CIS2_LOGIN_ID_NO_ROLES)


@when("I log in as a user with only roles that do not have access")
def login_with_without_access(context):
    current_tags = str(context.config.tags).split()
    assert (
        "multiple_roles_no_access" not in current_tags
    ), f"{context.tags} : {current_tags}: Trying to use MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE in a test not tagged @multiple_roles_no_access"  # noqa: E501
    login_with_retries(context, MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE)


@when("I log in with a single access role and multiple without access")
def login_with_single_role_with_access_multiple_without(context):
    current_tags = str(context.config.tags).split()
    assert (
        "multiple_roles_single_access" in current_tags
    ), f"{context.tags} : {current_tags}: Trying to use MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT in a test not tagged @multiple_roles_single_access"  # noqa: E501
    login_with_retries(
        context, MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT
    )


@when("I log in as a user with a pre selected role")
def login_with_pre_role_selected(context):
    current_tags = str(context.config.tags).split()
    assert (
        "multiple_access_pre_selected" in current_tags
    ), f"{context.tags} : {current_tags}: Trying to use MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE in a test not tagged @multiple_access_pre_selected"  # noqa: E501
    login_with_retries(
        context, MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE
    )


@when("I log in as a user with a single access role")
def login_with_single_role(context):
    current_tags = str(context.config.tags).split()
    assert (
        "single_access" in current_tags
    ), f"{context.tags} : {current_tags}: Trying to use MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE in a test not tagged @single_access"  # noqa: E501
    login_with_retries(context, MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE)


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

    context.page.wait_for_url(logged_in_urls, wait_until="load", timeout=2000)
    context.execute_steps("then I am logged in")


###############################################################################
# THEN STEPS
###############################################################################
@then("I am logged in")
def i_am_logged_in(context):
    timeout = 60  # 60 second timeout
    period = 5  # 5 second polling delay
    mustend = time.time() + timeout
    while time.time() < mustend:
        storage_state = context.browser.storage_state()
        for origin in storage_state.get("origins", []):
            for item in origin.get("localStorage", []):
                if item.get("name") == "isSignedIn":
                    is_signed_in_value = item.get("value")
                    break
        if is_signed_in_value == '{"isSignedIn":true}':  # type: ignore
            return
        time.sleep(period)
    raise TypeError("Not signed in")


@then("I am logged out")
def i_am_logged_out(context):
    timeout = 60  # 60 second timeout
    period = 5  # 5 second polling delay
    mustend = time.time() + timeout
    while time.time() < mustend:
        storage_state = context.browser.storage_state()
        for origin in storage_state.get("origins", []):
            for item in origin.get("localStorage", []):
                if item.get("name") == "isSignedIn":
                    is_signed_in_value = item.get("value")
                    break
        if is_signed_in_value == '{"isSignedIn":false}':  # type: ignore
            return
        time.sleep(period)
    raise TypeError("Not signed in")
