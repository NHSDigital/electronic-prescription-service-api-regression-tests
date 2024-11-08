import json
import logging
import uuid

# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]

from features.steps import pfp_api_steps
from methods.api.psu_api_methods import send_status_update
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


@when("I send an {status} update with a terminal status of {terminal}")
def i_send_an_update(context, status, terminal):
    if "e2e" not in context.tags or "sandbox" in context.config.userdata["env"].lower():
        context.receiver_ods_code = "FA565"
        context.prescription_id = generate_short_form_id(context.receiver_ods_code)
        context.prescription_item_id = uuid.uuid4()
        context.nhs_number = generate_single()
    context.terminal_status = terminal
    context.item_status = status

    send_status_update(context)


@then(
    "The prescription item has a status of Collected with a terminal status of completed"
)
def prescription_has_status_with_terminal_status(context):
    if "sandbox" in context.config.userdata["env"].lower():
        return
    pfp_api_steps.i_am_authenticated(context)
    pfp_api_steps.i_request_my_prescriptions(context)
    json_response = json.loads(context.response.content)
    logging.debug(context.response.content)
    entries = json_response["entry"]
    bundle = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ][0]["resource"]["entry"][0]["resource"]
    expected_item_id = context.prescription_item_id
    expected_item_status = context.item_status
    expected_terminal_status = context.terminal_status

    assert_that(bundle["identifier"][0]["value"].lower()).is_equal_to(expected_item_id)
    assert_that(bundle["status"]).is_equal_to(expected_terminal_status)
    assert_that(
        bundle["extension"][0]["extension"][0]["valueCoding"]["code"]
    ).is_equal_to(expected_item_status)
