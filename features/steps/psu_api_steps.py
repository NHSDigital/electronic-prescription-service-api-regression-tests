import uuid

# pylint: disable=no-name-in-module
from behave import given, when  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.psu_api_methods import send_status_update
from methods.shared.common import get_auth
from utils.prescription_id_generator import generate_short_form_id
from utils.random_nhs_number_generator import generate_single


@given("I am authorised to send prescription updates")
def i_am_authorised_to_send_prescription_updates(context):
    env = context.config.userdata["env"].lower()
    if "sandbox" in env:
        return
    context.auth_token = get_auth(env, "PSU")


@when("I send an {status} update with a terminal status of {terminal}")
def i_send_an_update(context, status, terminal):
    context.receiver_ods_code = "FA565"
    context.prescription_id = generate_short_form_id(context.receiver_ods_code)
    context.prescription_item_id = uuid.uuid4()
    context.terminal_status = terminal
    context.item_status = status
    context.nhs_number = generate_single()
    send_status_update(context)
