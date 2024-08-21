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
from methods.api.common_api_methods import get_headers, post
from methods.shared.common import the_expected_response_code_is_returned


def prepare_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$prepare"
    additional_headers = {"Content-Type": "application/json"}
    headers = get_headers(context, additional_headers)

    context.prepare_body = Prescription(context).body
    response = post(
        data=context.prepare_body, url=url, context=context, headers=headers
    )
    the_expected_response_code_is_returned(context, 200)

    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]
    context.algorithm = response.json()["parameter"][2]["valueString"]


def create_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#prescription-order"
    headers = get_headers(context)

    context.signed_body = SignedPrescription(context).body
    post(data=context.signed_body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)


def release_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task/$release"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.release_body = Release(context).body
    post(data=context.release_body, url=url, context=context, headers=headers)


def cancel_all_line_items(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["prescriber"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.cancel_body = Cancel(context).body
    post(data=context.cancel_body, url=url, context=context, headers=headers)


def dispense_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#dispense-notification"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    dispense_notification = DispenseNotification(context, False).body
    post(data=dispense_notification, url=url, context=context, headers=headers)


def amend_dispense_notification(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#dispense-notification"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    amended_dispense_notification = DispenseNotification(context, True).body
    post(data=amended_dispense_notification, url=url, context=context, headers=headers)


def withdraw_dispense_notification(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.dispense_notification_body = WithdrawDispenseNotification(context).body

    post(
        data=context.dispense_notification_body,
        url=url,
        context=context,
        headers=headers,
    )


def return_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.return_body = Return(context).body
    post(data=context.return_body, url=url, context=context, headers=headers)
