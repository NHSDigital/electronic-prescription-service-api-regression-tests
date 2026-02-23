import json
import uuid

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.psu_api_methods import send_status_update, check_status_updates
from methods.api.psu_api_methods import CODING_TO_STATUS_MAP
from methods.shared.common import get_auth, assert_that
from utils.prescription_id_generator import generate_short_form_id
from utils.random_nhs_number_generator import generate_single


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
        print(f"id from here {context.prescription_id}")
        context.prescription_item_id = uuid.uuid4()
        context.nhs_number = generate_single()
    context.terminal_status = status
    context.item_status = coding
    print(
        f"""Sending update for prescription ID: {context.prescription_id}: coding: {coding} status: {status}"""
    )
    send_status_update(context)


@when("I send a '{coding}' update with a status of '{status}'")
def i_send_an_update(context, coding, status):
    send_status_update_helper(context, coding, status)


@when("I send a '{coding}' update")
def i_send_an_update_without_status(context, coding):
    if coding not in CODING_TO_STATUS_MAP:
        raise ValueError(
            f"Unknown coding '{coding}'. Supported codings: {', '.join(CODING_TO_STATUS_MAP.keys())}"
        )
    status = CODING_TO_STATUS_MAP[coding]
    send_status_update_helper(context, coding, status)


@then(
    "The prescription item has a coding of '{expected_coding}' with a status of '{expected_status}'"
)
def verify_update_recorded(context, expected_coding, expected_status):
    if "sandbox" in context.config.userdata["env"].lower():
        print("Skipping verification in sandbox environment")
        return

    prescription_id = context.prescription_id

    response = check_status_updates(context, prescription_id=prescription_id)
    assert_that(response.status_code).is_equal_to(200)

    response_data = json.loads(response.content)
    matching_items = [
        items
        for items in response_data.get("items", [])
        if items.get("PrescriptionID") == prescription_id
    ]
    if matching_items:
        # Note that multiple items are possible, though not in any of our current tests
        item = matching_items[0]

        assert_that(item.get("TerminalStatus")).is_equal_to(expected_status)
        assert_that(item.get("Status")).is_equal_to(expected_coding)
