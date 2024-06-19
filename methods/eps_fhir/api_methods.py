import json
import uuid

from features.environment import CIS2_USERS
from messages.eps_fhir.api_request_dn_body_generators import (
    create_dispense_notification,
    create_dn_message_header,
    create_dn_medication_dispense,
    create_dn_medication_request,
    create_dn_organisation,
    create_dn_practitioner_role,
)
from methods.eps_fhir.api_request_body_generators import (
    create_fhir_bundle,
    create_fhir_parameter,
    generate_message_header,
    generate_medication_request,
    generate_patient,
    generate_organization,
    generate_practitioner_role,
    generate_practitioner,
    generate_provenance,
    generate_agent,
    generate_owner,
    generate_group_identifier,
    generate_return,
)
from methods.shared.common import the_expected_response_code_is_returned
from methods.shared.api import post, get_headers
from utils.prescription_id_generator import generate_short_form_id
from utils.signing import get_signature


def _create_new_prepare_body(context):
    context.sender_ods_code = "A83008"
    context.receiver_ods_code = "FA565"

    context.long_prescription_id = str(uuid.uuid4())
    context.prescription_id = generate_short_form_id(context.sender_ods_code)
    context.prescription_item_id = str(uuid.uuid4())

    user_id = CIS2_USERS["prescriber"]["user_id"]
    sds_role_id = CIS2_USERS["prescriber"]["role_id"]

    message_header = generate_message_header(
        context.sender_ods_code,
        context.receiver_ods_code,
    )

    medication_request = generate_medication_request(
        context.prescription_id,
        context.prescription_item_id,
        context.long_prescription_id,
        context.receiver_ods_code,
        context.nomination_code,
    )

    patient = generate_patient(context.nhs_number, context.sender_ods_code)

    organization = generate_organization()
    practitioner_role = generate_practitioner_role(sds_role_id)
    practitioner = generate_practitioner(user_id)

    body = create_fhir_bundle(
        message_header,
        medication_request,
        patient,
        organization,
        practitioner_role,
        practitioner,
    )
    return body


def _cancel_medication_request(medication_request):
    medication_request["resource"]["status"] = "cancelled"
    medication_request["resource"]["statusReason"] = {
        "coding": [
            {
                "system": "https://fhir.nhs.uk/CodeSystem/medicationrequest-status-reason",
                "code": "0001",
                "display": "Prescribing Error",
            }
        ]
    }


def _create_cancel_body(context):
    cancel_body = json.loads(context.prepare_body)

    medication_requests = [
        e
        for e in cancel_body["entry"]
        if e["resource"]["resourceType"] == "MedicationRequest"
    ]
    [_cancel_medication_request(mr) for mr in medication_requests]

    message_header = [
        e
        for e in cancel_body["entry"]
        if e["resource"]["resourceType"] == "MessageHeader"
    ][0]
    event_coding = message_header["resource"]["eventCoding"]
    event_coding["code"] = "prescription-order-update"
    event_coding["display"] = "Prescription Order Update"

    return json.dumps(cancel_body)


def _create_dispense_notification_body(context):
    organisation_uuid = uuid.uuid4()
    practitioner_role_uuid = uuid.uuid4()
    practitioner_role = create_dn_practitioner_role(
        practitioner_role_uuid, organisation_uuid
    )

    patient_uuid = uuid.uuid4()
    medication_request_uuid = uuid.uuid4()
    medication_request = create_dn_medication_request(
        medication_request_uuid,
        context.prescription_item_id,
        patient_uuid,
        context.long_prescription_id,
        context.prescription_id,
        practitioner_role_uuid,
    )

    message_header = create_dn_message_header(context.receiver_ods_code)

    medication_dispense_uuid = uuid.uuid4()
    medication_dispense = create_dn_medication_dispense(
        medication_dispense_uuid,
        context.nhs_number,
        practitioner_role_uuid,
        practitioner_role,
        medication_request_uuid,
        medication_request,
        context.prescription_item_id,
    )

    organisation = create_dn_organisation(organisation_uuid, context.receiver_ods_code)

    body = create_dispense_notification(
        message_header, medication_dispense, organisation
    )

    return json.dumps(body)


def _replace_ids(body):
    old_id = json.loads(body)["id"]
    return body.replace(old_id, str(uuid.uuid4()))


def prepare_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$prepare"
    additional_headers = {"Content-Type": "application/json"}
    headers = get_headers(context, additional_headers)

    context.prepare_body = _create_new_prepare_body(context)
    response = post(
        data=context.prepare_body, url=url, context=context, headers=headers
    )
    the_expected_response_code_is_returned(context, 200)

    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]


def _create_signed_body(context):
    context.signature = get_signature(digest=context.digest)
    body = json.loads(context.prepare_body)
    provenance = generate_provenance(
        signature=context.signature, timestamp=context.timestamp
    )
    body["entry"].append(provenance)
    body = json.dumps(body)
    return body


def create_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#prescription-order"
    headers = get_headers(context)

    context.signed_body = _create_signed_body(context)
    post(data=context.signed_body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)


def _create_release_body(context):
    prescription_order_number = context.prescription_id
    group_identifier = generate_group_identifier(
        prescription_order_number=prescription_order_number
    )
    owner = generate_owner(receiver_ods_code=context.receiver_ods_code)
    agent = generate_agent()
    body = create_fhir_parameter(group_identifier, owner, agent)
    return body


def _create_return_body(context):
    short_prescription_id = context.prescription_id
    nhs_number = context.nhs_number

    body = generate_return(nhs_number, short_prescription_id)
    return json.dumps(body)


def _create_withdraw_dispense_notification_body(context):
    short_prescription_id = context.prescription_id
    nhs_number = context.nhs_number

    body = generate_return(nhs_number, short_prescription_id)
    return json.dumps(body)


def release_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task/$release"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.release_body = _create_release_body(context)
    post(data=context.release_body, url=url, context=context, headers=headers)


def cancel_all_line_items(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["prescriber"]["role_id"]}
    headers = get_headers(context, additional_headers)

    cancel_body = _create_cancel_body(context)
    cancel_body = _replace_ids(cancel_body)
    context.cancel_body = cancel_body

    post(data=cancel_body, url=url, context=context, headers=headers)


def dispense_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#dispense-notification"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    dispense_notification_body = _create_dispense_notification_body(context)

    post(data=dispense_notification_body, url=url, context=context, headers=headers)


def withdraw_dispense_notification(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    dispense_notification_body = _create_withdraw_dispense_notification_body(context)

    post(data=dispense_notification_body, url=url, context=context, headers=headers)


def return_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task"
    additional_headers = {"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]}
    headers = get_headers(context, additional_headers)

    context.return_body = _create_return_body(context)
    post(data=context.return_body, url=url, context=context, headers=headers)


def assert_ok_status_code(context):
    the_expected_response_code_is_returned(context, 200)
