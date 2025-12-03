from features.environment import CIS2_USERS
from messages.eps_fhir.cancel import Cancel
from messages.eps_fhir.dispense_notification import DispenseNotification

from messages.eps_fhir.prescription import Prescription
from messages.eps_fhir.prescription_return import Return
from messages.eps_fhir.release import Release
from messages.eps_fhir.signed_prescription import SignedPrescription
from messages.eps_fhir.withdraw_dispense_notification import (
    WithdrawDispenseNotification,
)
from messages.eps_fhir.dispense_notification import DNProps
from methods.api.common_api_methods import get_headers, post
from methods.shared.common import the_expected_response_code_is_returned

PRESCRIBING_BASE_URL = ""
DISPENSING_BASE_URL = ""


def calculate_eps_fhir_base_url(context):
    product = context.config.userdata["product"].upper()
    global PRESCRIBING_BASE_URL
    global DISPENSING_BASE_URL
    if product == "EPS-FHIR":
        PRESCRIBING_BASE_URL = context.eps_fhir_base_url
        DISPENSING_BASE_URL = context.eps_fhir_base_url
    else:
        PRESCRIBING_BASE_URL = context.eps_fhir_prescribing_base_url
        DISPENSING_BASE_URL = context.eps_fhir_dispensing_base_url


def prepare_prescription(context):
    url = f"{PRESCRIBING_BASE_URL}/FHIR/R4/$prepare"
    additional_headers = {"Content-Type": "application/json"}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.prepare_body = Prescription(context).body
    response = post(
        data=context.prepare_body, url=url, context=context, headers=headers
    )
    the_expected_response_code_is_returned(context, 200)

    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]
    context.algorithm = response.json()["parameter"][2]["valueString"]


def try_prepare_prescription(context):
    url = f"{PRESCRIBING_BASE_URL}/FHIR/R4/$prepare"
    additional_headers = {"Content-Type": "application/json"}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.prepare_body = Prescription(context).body
    post(data=context.prepare_body, url=url, context=context, headers=headers)


def create_signed_prescription(context):
    url = f"{PRESCRIBING_BASE_URL}/FHIR/R4/$process-message#prescription-order"
    headers = get_headers(context, context.auth_method)

    context.signed_body = SignedPrescription(context).body
    response = post(data=context.signed_body, url=url, context=context, headers=headers)
    print(response.content)
    the_expected_response_code_is_returned(context, 200)


def release_signed_prescription(context):
    url = f"{DISPENSING_BASE_URL}/FHIR/R4/Task/$release"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.release_body = Release(context).body
    post(data=context.release_body, url=url, context=context, headers=headers)


def cancel_all_line_items(context, reason):
    url = f"{PRESCRIBING_BASE_URL}/FHIR/R4/$process-message"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["prescriber"]["role_id"]}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.cancel_body = Cancel(context, reason).body
    post(data=context.cancel_body, url=url, context=context, headers=headers)


def dispense_prescription(context, dn_props: DNProps):
    url = f"{DISPENSING_BASE_URL}/FHIR/R4/$process-message#dispense-notification"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, context.auth_method, additional_headers)

    dispense_notification = DispenseNotification(dn_props)
    context.dispense_notification_id = dispense_notification.dispense_notification_id
    post(data=dispense_notification.body, url=url, context=context, headers=headers)


def withdraw_dispense_notification(context):
    url = f"{DISPENSING_BASE_URL}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.dispense_notification_body = WithdrawDispenseNotification(context).body

    post(
        data=context.dispense_notification_body,
        url=url,
        context=context,
        headers=headers,
    )


def return_prescription(context):
    url = f"{DISPENSING_BASE_URL}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.return_body = Return(context).body
    post(data=context.return_body, url=url, context=context, headers=headers)


def call_validator(context, product, show_validation, validate_body):
    if product == "eps_fhir_dispensing":
        base_url = context.eps_fhir_dispensing_base_url
    elif product == "eps_fhir_prescribing":
        base_url = context.eps_fhir_prescribing_base_url
    else:
        base_url = context.eps_fhir_base_url
    url = f"{base_url}/FHIR/R4/$validate"
    if show_validation == "false" or show_validation == "true":
        additional_headers = {
            "Content-Type": "application/json",
            "x-show-validation-warnings": show_validation,
        }
    else:
        additional_headers = {"Content-Type": "application/json"}
    headers = get_headers(context, context.auth_method, additional_headers)

    context.validate_body = validate_body
    post(data=context.validate_body, url=url, context=context, headers=headers)
