# # pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from features.environment import clear_scenario_user_sessions

from pages.session_logged_out import SessionLoggedOutPage


@when("the session expires because of automatic timeout")
def clear_active_session(context):
    # Call clear active session lambda for user
    clear_scenario_user_sessions(context, context.scenario.tags)


@then("I should see the timeout session logged out page")
def verify_timeout_logged_out_page(context):
    """Verify the timeout session logged out page is displayed"""
    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.timeout_session_container).to_be_visible()
    expect(logged_out_page.timeout_title).to_have_text(
        "For your security, we have logged you out"
    )
    expect(logged_out_page.timeout_description).to_be_visible()
    expect(logged_out_page.timeout_description2).to_be_visible()
