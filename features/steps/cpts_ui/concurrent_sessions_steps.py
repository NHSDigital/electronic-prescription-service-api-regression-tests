# # pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.session_selection import SessionSelectionPage
from pages.session_logged_out import SessionLoggedOutPage


# WHEN
@when('I click the "Close this window" button')
def click_close_window(context):
    """Click the close window button"""
    session_page = SessionSelectionPage(context.active_page)
    session_page.close_window_button.click()
    context.active_page.wait_for_load_state("networkidle", timeout=5000)


# THEN
@when('I should be logged out because of "{state}" protections')
@then('I should be logged out because of "{state}" protections')
def verify_context_logged_out(context, state):
    """Verify that a specific context is logged out"""
    if state == "concurrency":
        logged_out_page = SessionLoggedOutPage(context.active_page)

        context.active_page.clock.fast_forward(
            "06:00"
        )  # Jump 6 mins to trigger auto-check

        logged_out_page = SessionLoggedOutPage(context.active_page)
        expect(logged_out_page.concurrent_session_container).to_be_visible()

        context.execute_steps(
            "then I should see the concurrent session logged out page"
        )

    if state == "timeout":
        logged_out_page = SessionLoggedOutPage(context.active_page)
        context.active_page.wait_for_load_state("networkidle", timeout=5000)
        expect(logged_out_page.timeout_session_container).to_be_visible()


@when("I should see the session selection page")
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


@then('I click the "Start a new session" button')
def click_start_new_session(context):
    """Click the start new session button"""
    session_page = SessionSelectionPage(context.active_page)
    session_page.new_session_button.click()
    context.active_page.wait_for_load_state("networkidle", timeout=5000)


@then("I am not able to navigate away from session selection page")
def verify_blocked_navigation_session_selection(context):
    context.execute_steps('when I directly navigate to "/search-by-prescription-id"')
    context.execute_steps('then I should be redirected to "/select-active-session"')


@then("I should see the concurrent session logged out page")
def verify_concurrent_session_title(context):
    """Verify the concurrent session logged out title"""
    title = "You have been logged out"
    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.concurrent_title).to_have_text(title)
    expect(logged_out_page.concurrent_description).to_be_visible()
    expect(logged_out_page.concurrent_contact).to_be_visible()
    expect(logged_out_page.nhs_service_desk_email).to_be_visible()
    expect(logged_out_page.nhs_service_desk_email).to_have_attribute(
        "href", "mailto:ssd.nationalservicedesk@nhs.net"
    )
