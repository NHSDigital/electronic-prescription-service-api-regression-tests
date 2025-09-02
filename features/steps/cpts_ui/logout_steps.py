# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.logout import Logout


###############################################################################
# GIVEN
###############################################################################


@given("the logout confirmation modal is displayed")
def given_logout_modal_is_displayed(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_header_link.click()
    expect(logout_page.logout_modal_content).to_be_visible()


@given("I am on the logout successful page")
def given_on_logout_successful_page(context):
    context.execute_steps("Given the logout confirmation modal is displayed")
    context.execute_steps("When I confirm the logout")

    logout_page = Logout(context.page)

    expect(logout_page.logout_page_heading).to_be_visible()
    expect(logout_page.logout_page_content).to_be_visible()
    expect(logout_page.logout_page_login_link).to_be_visible()


###############################################################################
# WHEN
###############################################################################


@when("I click the logout button")
def when_i_click_logout_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_header_link.click()


@when("I confirm the logout")
def when_i_confirm_the_logout(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_logout_button.click()


@when('I click the "log back in" button')
def when_i_click_log_back_in_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_page_login_link.click()


@when("I close the modal with the cross")
def when_i_close_modal_with_cross(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_close_button.click()


@when("I close the modal with the cancel button")
def when_i_close_modal_with_cancel_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_cancel_button.click()


@when("I close the modal by clicking outside the modal")
def when_i_close_modal_with_overlay(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_overlay.click(force=True, position={"x": 0, "y": 0})


@when("I close the modal by hitting escape")
def when_i_close_modal_by_hitting_escape(context):
    logout_page = Logout(context.page)
    logout_page.page.keyboard.press("Escape")


@when("I navigate back using browser history")
def navigate_back_browser_history(context):
    """Simulate user pressing browser back button"""
    context.page.go_back()
    context.page.wait_for_load_state("networkidle")


@when('I directly navigate to "{route}"')
def directly_navigate_to_route(context, route):
    """Navigate directly to a protected route URL"""
    full_url = f"{context.cpts_ui_base_url}{route.lstrip('/')}"
    context.page.goto(full_url)
    context.page.wait_for_load_state("networkidle")


###############################################################################
# THEN STEPS
###############################################################################


@then("I see the logout confirmation modal")
def then_i_see_logout_confirmation_modal(context):
    logout_page = Logout(context.page)
    expect(logout_page.logout_modal_content.get_by_role("heading")).to_contain_text(
        "Are you sure you want to log out?"
    )
    expect(logout_page.logout_modal_content.get_by_role("paragraph")).to_contain_text(
        "Logging out will end your session."
    )


@then("the logout confirmation modal is not displayed")
def then_logout_confirmation_modal_not_displayed(context):
    logout_page = Logout(context.page)
    expect(logout_page.logout_modal_content).not_to_be_visible()


@then("I see the logout successful page")
def then_i_see_logout_successful_page(context):
    logout_page = Logout(context.page)
    expect(logout_page.logout_page_heading).to_be_visible()
    expect(logout_page.logout_page_content).to_be_visible()


@then("I am on the login page")
def then_i_am_on_login_page(context):
    environment = context.config.userdata["env"].lower()
    if environment == "internal-qa":
        context.page.wait_for_url("**/login")
    else:
        context.page.wait_for_url("**/identity.ptl.api.platform.nhs.uk/**")


@then("I should be redirected to the login page")
def should_be_redirected_to_login(context):
    """Verify user is redirected to login page"""
    context.page.wait_for_load_state("networkidle", timeout=5000)

    current_url = context.page.url

    login_redirect = "/login" in current_url
    oauth_redirect = "identity.ptl.api.platform.nhs.uk" in current_url

    assert (
        login_redirect or oauth_redirect
    ), f"Expected to be redirected to login (local or OAuth), but URL is: {current_url}"
