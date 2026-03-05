from datetime import UTC, datetime, timedelta
import json
import logging
import time
import uuid

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.psu_api_methods import (
    get_status_updates,
    send_status_update,
    check_status_updates,
)
from methods.api.psu_api_methods import CODING_TO_STATUS_MAP
from methods.shared.common import get_auth, assert_that
from utils.prescription_id_generator import generate_short_form_id
from utils.random_nhs_number_generator import generate_single

logger = logging.getLogger(__name__)


@given("I am authorised to send prescription updates")
@when("I am authorised to send prescription updates")
def i_am_authorised_to_send_prescription_updates(context):
    env = context.config.userdata["env"].lower()
    if "sandbox" in env:
        return
    context.auth_token = get_auth(env, "PSU")


@given("status updates are enabled")
def step_impl(context):
    env = context.config.userdata["env"].lower()
    if "int" == env:
        context.config.status_updates_enabled = True
    else:
        context.config.status_updates_enabled = False


def send_status_update_helper(context, coding, status):
    """Helper function to send a status update with the given coding and status values."""
    if "e2e" not in context.tags or "sandbox" in context.config.userdata["env"].lower():
        context.receiver_ods_code = "FA565"
        context.prescription_id = generate_short_form_id(context.receiver_ods_code)
        logger.debug(f"id from here {context.prescription_id}")
        context.prescription_item_id = uuid.uuid4()
        context.nhs_number = generate_single()
    context.terminal_status = status
    context.item_status = coding
    logger.debug(
        f"""Sending update for prescription ID: {context.prescription_id}: coding: {coding} status: {status}"""
    )
    send_status_update(context)


@when("I send a '{coding}' update with a status of '{status}'")
def i_send_an_update(context, coding, status):
    send_status_update_helper(context, coding, status)


@when("I send a '{coding}' update")
def i_send_an_update_without_status(context, coding):
    if coding not in CODING_TO_STATUS_MAP:
        raise ValueError(f"Unknown coding '{coding}'. Supported codings: {', '.join(CODING_TO_STATUS_MAP.keys())}")
    status = CODING_TO_STATUS_MAP[coding]
    send_status_update_helper(context, coding, status)


@when("I send a '{coding}' post-dated update")
def i_send_a_postdated_update(context, coding):
    """Send a post-dated status update with lastModified timestamp in the future."""
    if coding not in CODING_TO_STATUS_MAP:
        raise ValueError(f"Unknown coding '{coding}'. Supported codings: {', '.join(CODING_TO_STATUS_MAP.keys())}")
    status = CODING_TO_STATUS_MAP[coding]

    # Configure post-dated delay (30 seconds for test environments)
    post_dated_delay = getattr(context.config.userdata, "post_dated_delay", 30)
    context.post_dated_delay = post_dated_delay

    # Calculate future timestamp
    context.post_dated_timestamp = (datetime.now(UTC) + timedelta(seconds=post_dated_delay)).isoformat()

    logger.debug(f"Sending post-dated update with lastModified: {context.post_dated_timestamp}")
    send_status_update_helper(context, coding, status)


@when("I advance the clock to beyond the post-dated time")
def advance_clock_beyond_postdated(context):
    """Poll the API until the post-dated time has passed and status update takes effect."""
    if "sandbox" in context.config.userdata["env"].lower():
        logger.debug("Skipping clock advancement in sandbox environment")
        return

    prescription_id = context.prescription_id
    expected_coding = context.item_status

    # Polling configuration
    timeout = context.post_dated_delay + 30  # Add 30 second buffer
    period = 5  # Poll every 5 seconds
    mustend = time.time() + timeout

    logger.debug(f"Polling for status update to take effect (timeout: {timeout}s, interval: {period}s)")

    while time.time() < mustend:
        response = check_status_updates(context, prescription_id=prescription_id)

        if response.status_code == 200:
            response_data = json.loads(response.content)
            matching_items = [
                items for items in response_data.get("items", []) if items.get("PrescriptionID") == prescription_id
            ]

            if matching_items:
                item = matching_items[0]
                current_status = item.get("Status")
                logger.debug(f"Current status: {current_status}, Expected: {expected_coding}")

                # Check if the post-dated update has taken effect
                if current_status == expected_coding:
                    logger.debug(f"Post-dated status update has taken effect: {expected_coding}")
                    return

        time.sleep(period)

    raise TimeoutError(
        f"Post-dated status update did not take effect within {timeout} seconds. " f"Expected status: {expected_coding}"
    )


@then("The prescription item has a coding of '{expected_coding}' with a status of '{expected_status}'")
def verify_update_recorded(context, expected_coding, expected_status):
    if "sandbox" in context.config.userdata["env"].lower():
        logger.debug("Skipping verification in sandbox environment")
        return

    prescription_id = context.prescription_id

    # response = check_status_updates(context, prescription_id=prescription_id)
    response = get_status_updates(context)
    assert_that(response.status_code).is_equal_to(200)

    response_data = json.loads(response.content)
    matching_items = [
        items for items in response_data.get("items", []) if items.get("PrescriptionID") == prescription_id
    ]
    if matching_items:
        # Note that multiple items are possible, though not in any of our current tests
        item = matching_items[0]

        assert_that(item.get("TerminalStatus")).is_equal_to(expected_status)
        assert_that(item.get("Status")).is_equal_to(expected_coding)
