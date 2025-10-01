# # pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.session_selection import SessionSelectionPage
from pages.session_logged_out import SessionLoggedOutPage


# GIVEN
@given("I clear the session for the user")
def clear_user_session(context):
    """Clear the session to simulate timeout"""
    context.active_page.evaluate(
        "() => { localStorage.clear(); sessionStorage.clear(); }"
    )


# WHEN
@when('I click the "Close this window" button')
def click_close_window(context):
    """Click the close window button"""
    session_page = SessionSelectionPage(context.active_page)
    session_page.close_window_button.click()


@when("I click the login link")
def click_login_link(context):
    """Click the login link on the logged out page"""
    logged_out_page = SessionLoggedOutPage(context.active_page)
    # Click whichever login link is visible
    if logged_out_page.concurrent_session_container.is_visible():
        logged_out_page.concurrent_login_link.click()
    else:
        logged_out_page.timeout_login_link.click()


# THEN
@then('I click the "Start a new session" button')
def click_start_new_session(context):
    """Click the start new session button"""
    session_page = SessionSelectionPage(context.active_page)
    session_page.new_session_button.click()
    context.active_page.wait_for_load_state("networkidle", timeout=5000)


@then("I should see the session selection page")
def verify_session_selection_page(context):
    """Verify the session selection page is displayed"""

    session_page = SessionSelectionPage(context.active_page)
    expect(session_page.main_container).to_be_visible()
    expect(session_page.title).to_be_visible()
    expect(session_page.new_session_button).to_be_visible()
    expect(session_page.close_window_button).to_be_visible()
    expect(session_page.description).to_be_visible()
    expect(session_page.instructions).to_be_visible()


@then("I am not able to navigate away from session selection page")
def verify_blocked_navigation_session_selection(context):
    context.execute_steps('when I directly navigate to "/search-by-prescription-id"')
    context.execute_steps('then I should be redirected to "/select-active-session"')


@then('I should see the session selection title "{expected_title}"')
def verify_session_selection_title(context, expected_title):
    """Verify the session selection page title"""
    session_page = SessionSelectionPage(context.active_page)
    expect(session_page.title).to_have_text(expected_title)


@then('I should see the concurrent session title "{expected_title}"')
def verify_concurrent_session_title(context, expected_title):
    """Verify the concurrent session logged out title"""
    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.concurrent_title).to_have_text(expected_title)


@then("I should see the concurrent session description")
def verify_concurrent_session_description(context):
    """Verify the concurrent session description is visible"""
    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.concurrent_description).to_be_visible()
    expect(logged_out_page.concurrent_contact).to_be_visible()


@then("I should see the NHS service desk email link")
def verify_nhs_service_desk_email(context):
    """Verify the NHS service desk email link is visible"""
    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.nhs_service_desk_email).to_be_visible()
    expect(logged_out_page.nhs_service_desk_email).to_have_attribute(
        "href", "mailto:ssd.nationalservicedesk@nhs.net"
    )


# Session State Verification Steps
@then(
    'the "{context_name}" context should be logged out because of "{state}" protections'
)
def verify_context_logged_out(context, context_name, state):
    """Verify that a specific context is logged out"""
    original_page_context = context.active_page
    try:
        # Switch to the specified context
        context.execute_steps(f'Given I switch browser context to "{context_name}"')
        logged_out_page = SessionLoggedOutPage(context.active_page)
        if state == "concurrency":
            assert logged_out_page.is_concurrent_session_displayed()
        if state == "timeout":
            assert logged_out_page.is_timeout_session_displayed()
    finally:
        # Switch back to original context
        context.active_page = original_page_context


@then('the "{context_name}" context should remain logged in')
def verify_context_logged_in(context, context_name):
    """Verify that a specific context remains logged in"""
    original_context = context.active_context
    try:
        # Switch to the specified context
        context.execute_steps(f'Given I switch browser context to "{context_name}"')
        expect(
            context.active_page.get_by_test_id("session-logged-out-concurrent")
        ).not_to_be_visible()
        expect(
            context.active_page.get_by_test_id("session-logged-out-timeout")
        ).not_to_be_visible()
        # Check for search for prescription page properties?
    finally:
        context.active_context = original_context
        context.active_page = context.active_context.active_pages[0]


@then("I should be redirected to the session selection page")
def verify_redirected_to_session_selection(context):
    """Verify redirection to session selection page"""
    context.active_page.wait_for_url("**/session-selection")
    context.execute_steps("Then I should see the session selection page")
