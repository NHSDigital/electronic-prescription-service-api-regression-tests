# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.logout import Logout


@when("I click the logout button")
def i_click_logout_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_header_link.click()


@then("I can see the logout modal")
def i_can_see_logout_modal(context):
    logout_page = Logout(context.page)
    expect(logout_page.logout_modal_content.get_by_role("heading")).to_contain_text(
        "Are you sure you want to log out?"
    )
    expect(logout_page.logout_modal_content.get_by_role("paragraph")).to_contain_text(
        "Logging out will end your session."
    )


@then("I cannot see the logout modal")
def i_cannot_see_logout_modal(context):
    logout_page = Logout(context.page)
    expect(logout_page.logout_modal_content).not_to_be_visible()


@when("I close the modal with the cross")
def i_can_close_modal_with_cross(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_close_button.click()


@when("I close the modal with the close button")
def i_can_close_modal_with_cancel_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_cancel_button.click()


@when("I close the modal with the overlay")
def i_can_close_modal_with_overlay(context):
    logout_page = Logout(context.page)
    print("overlay", logout_page.logout_modal_overlay)
    logout_page.logout_modal_overlay.click(force=True, position={"x": 0, "y": 0})


@when("I close the modal by hitting escape")
def i_can_close_modal_with_escape(context):
    logout_page = Logout(context.page)

    logout_page.page.keyboard.press("Escape")


@when("I click on the logout modal confirm button")
def i_click_confirm_logout_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_modal_logout_button.click()


@then("I can see the logout successful page")
def i_can_see_logout_successful_page(context):
    logout_page = Logout(context.page)
    expect(logout_page.logout_page_heading).to_be_visible()
    expect(logout_page.logout_page_content).to_be_visible()


@when("I click the log back in button")
def i_click_log_back_in_button(context):
    logout_page = Logout(context.page)
    logout_page.logout_page_login_link.click()
