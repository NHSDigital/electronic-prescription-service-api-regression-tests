import json
import time
import uuid

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

# from features.steps import pfp_api_steps
from methods.api.psu_api_methods import send_status_update, check_status_updates
from methods.shared.common import get_auth, assert_that
from utils.prescription_id_generator import generate_short_form_id
from utils.random_nhs_number_generator import generate_single

# Map coding types to status values
CODING_TO_STATUS_MAP = {
    "With Pharmacy": "in-progress",
    "Ready to Collect": "in-progress",
    "Collected": "completed",
}


@given("I am authorised to send prescription updates")
@when("I am authorised to send prescription updates")
def i_am_authorised_to_send_prescription_updates(context):
    env = context.config.userdata["env"].lower()
    if "sandbox" in env:
        return
    context.auth_token = get_auth(env, "PSU")


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


@when("I send a {coding} update with a status of {status}")
def i_send_an_update(context, coding, status):
    send_status_update_helper(context, coding, status)


@when("I send a {coding} update")
def i_send_an_update_without_status(context, coding):
    if coding not in CODING_TO_STATUS_MAP:
        raise ValueError(
            f"Unknown coding '{coding}'. Supported codings: {', '.join(CODING_TO_STATUS_MAP.keys())}"
        )
    status = CODING_TO_STATUS_MAP[coding]
    send_status_update_helper(context, coding, status)


# @then("The prescription item has a status of {expected_status} with a terminal status of {expected_terminal_status}")
# def prescription_has_status_with_terminal_status(context, expected_status, expected_terminal_status):
#     if "sandbox" in context.config.userdata["env"].lower():
#         return
#     pfp_api_steps.i_am_authenticated(context, "PFP-APIGEE")
#     pfp_api_steps.i_request_my_prescriptions(context)
#     json_response = json.loads(context.response.content)
#     logging.debug(context.response.content)
#     entries = json_response["entry"]
#     bundle = [entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"][0]["resource"]["entry"][0][
#         "resource"
#     ]
#     expected_item_id = context.prescription_item_id
#     assert_that(expected_terminal_status).is_equal_to(STATUS_TO_TERMINAL_MAP[expected_status])

#     assert_that(bundle["identifier"][0]["value"].lower()).is_equal_to(expected_item_id)
#     assert_that(bundle["status"]).is_equal_to(expected_terminal_status)
#     assert_that(bundle["extension"][0]["extension"][0]["valueCoding"]["code"]).is_equal_to(expected_status)


@then(
    "The prescription item has a coding of {expected_coding} with a status of {expected_status}"
)
def verify_update_recorded(context, expected_coding, expected_status):
    if "sandbox" in context.config.userdata["env"].lower():
        print("Skipping verification in sandbox environment")
        return

    check_update_with_retries(context, expected_coding, expected_status)


def check_update_with_retries(context, expected_coding, expected_status):
    prescription_id = context.prescription_id
    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        if attempt > 0:
            print(f"Retry attempt {attempt}/{max_retries - 1}")
            time.sleep(retry_delay)

        response = check_status_updates(context, prescription_id=prescription_id)

        if response.status_code != 200:
            print(f"Check endpoint returned status {response.status_code}")
            continue

        try:
            response_data = json.loads(response.content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse response: {e}")
            continue

        matching_items = [
            items
            for items in response_data.get("items", [])
            if items.get("PrescriptionID") == prescription_id
        ]
        if matching_items:
            # TODO: need to handle multiple items
            item = matching_items[0]

            assert_that(item.get("TerminalStatus")).is_equal_to(expected_status)
            assert_that(item.get("Status")).is_equal_to(expected_coding)
            return

    # If we exhausted all retries without finding the update
    raise AssertionError(
        f"Failed to verify status update for prescription {prescription_id} "
        f"after {max_retries} attempts. Expected coding '{expected_coding}' "
        f"with status '{expected_status}' was not found."
    )
