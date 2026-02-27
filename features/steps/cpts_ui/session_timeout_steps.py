# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from features.environment import clear_scenario_user_sessions
import requests
import json
import uuid

from pages.session_logged_out import SessionLoggedOutPage
from pages.session_timeout_modal import SessionTimeoutModal


@when("the session expires because of automatic timeout")
def clear_active_session(context):
    # Call clear active session lambda for user
    clear_scenario_user_sessions(context, context.scenario.tags)


@then("I should see the timeout session logged out page")
def verify_timeout_logged_out_page(context):
    """Verify the timeout session logged out page is displayed"""
    logged_out_page = SessionLoggedOutPage(context.active_page)
    expect(logged_out_page.timeout_session_container).to_be_visible()
    expect(logged_out_page.timeout_title).to_have_text("For your security, we have logged you out")
    expect(logged_out_page.timeout_description).to_be_visible()
    expect(logged_out_page.timeout_description2).to_be_visible()


@when("I set lastActivityTime to be 13 minutes ago")
def set_last_activity_time_13_minutes_ago(context):
    """Call the test support endpoint to set lastActivityTime to 13 minutes in the past"""
    # pylint: disable=broad-exception-raised
    if "fake_time" not in context.tags:
        raise Exception("Fake_time tag required in this scenario. See README.md")

    # Wait a moment to ensure session is established after login
    context.active_page.wait_for_timeout(3000)

    # Determine username based on scenario tags
    username = None
    for tag in context.scenario.tags:
        if tag == "single_access":
            username = "Mock_555043300081"
            break
        elif tag == "multiple_access":
            username = "Mock_555043308597"
            break
        elif tag == "multiple_access_pre_selected":
            username = "Mock_555043304334"
            break
        elif tag == "multiple_roles_single_access":
            username = "Mock_555043303739"
            break

    if not username:
        raise Exception("No valid account tag found for setting lastActivityTime")

    request_id = str(uuid.uuid4())
    print(
        f"Setting lastActivityTime to 13 minutes ago for {username}. Request ID: {request_id}"
    )

    payload = json.dumps({"username": username, "request_id": request_id})

    # Call the lambda endpoint to set lastActivityTime to 13 minutes in the past
    response = requests.post(
        f"{context.cpts_ui_base_url}/api/test-support-fake-timer",
        data=payload,
        headers={
            "Source": f"{context.scenario.name}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code != 200:
        print(
            f"Failed to set lastActivityTime. Response: {response.status_code} - {response.text}"
        )
        raise Exception(f"Failed to set lastActivityTime: {response.status_code}")

    # fast forward clock by 13 minutes to make frontend think time has passed
    context.active_page.clock.fast_forward(13 * 60 * 1000)


@when("I fast forward 1 minute so that updateTracker event happens")
def fast_forward_1_minute(context):
    """Fast forward 1 minute to trigger the updateTracker periodic check"""
    # pylint: disable=broad-exception-raised
    if "fake_time" not in context.tags:
        raise Exception("Fake_time tag required in this scenario. See README.md")

    # Fast forward by 1 minute to trigger the 60-second interval
    context.active_page.clock.fast_forward(60 * 1000)

    # Give a moment for the periodic check to execute and React to update
    context.active_page.wait_for_timeout(2000)


@then("I should see the timeout session modal")
def verify_timeout_session_modal(context):
    """Verify the timeout session modal is displayed"""
    modal = SessionTimeoutModal(context.active_page)

    context.active_page.wait_for_timeout(3000)

    expect(modal.modal_container).to_be_visible(timeout=15000)
    expect(modal.stay_logged_in_button).to_be_visible(timeout=5000)
    expect(modal.logout_button).to_be_visible(timeout=5000)


@when("I fast forward 3 minutes so that updateTracker event happens")
def fast_forward_3_minutes(context):
    """Wait 2 minutes for natural session timeout"""
    # pylint: disable=broad-exception-raised
    if "fake_time" not in context.tags:
        raise Exception("Fake_time tag required in this scenario. See README.md")

    # Wait 2 minutes in real time for natural timeout
    context.active_page.wait_for_timeout(120000)


@then("I am redirected to the logged out for inactivity page")
def verify_timed_out_session_and_logged_out_page(context):
    """Verify that the session has timed out and user is redirected to session-logged-out URL"""

    # Wait for navigation to complete
    context.active_page.wait_for_load_state("networkidle", timeout=10000)

    # Get current URL and verify it contains session-logged-out
    current_url = context.active_page.url

    assert (
        "/session-logged-out" in current_url
    ), f"Expected URL to contain '/session-logged-out', but got: {current_url}"
