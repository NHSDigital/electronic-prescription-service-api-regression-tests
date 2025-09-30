# # pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from features.environment import clear_scenario_user_sessions

from pages.session_logged_out import SessionLoggedOutPage
from datetime import datetime


@when("the session expires because of automatic timeout")
def clear_active_session(context):
    # Call clear active session lambda for user
    context.active_page.clock.install(
        time=datetime(2025, 1, 1, 8, 0, 0)
    )  # Set artificial system clock
    clear_scenario_user_sessions(context, [context.config.tags])


@then("I should see the timeout session logged out page")
def verify_timeout_logged_out_page(context):
    """Verify the timeout session logged out page is displayed"""
    context.active_page.clock.fast_forward("05:00")  # Jump 5 mins to trigger auto-check

    context.active_page.wait_for_load_state(
        "networkidle", timeout=5000
    )  # Wait for reload

    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.timeout_session_container).to_be_visible()
    expect(logged_out_page.timeout_title).to_have_text(
        "For your security, we have logged you out"
    )
    expect(logged_out_page.timeout_description).to_be_visible()
    expect(logged_out_page.timeout_description2).to_be_visible()
    assert logged_out_page.is_timeout_session_displayed()
