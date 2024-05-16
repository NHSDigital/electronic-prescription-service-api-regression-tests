import json
import uuid

from features.environment import CIS2_USERS
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
)
from methods.shared.common import the_expected_response_code_is_returned
from methods.shared.api import post, get_default_headers
from utils.prescription_id_generator import generate_short_form_id
from utils.signing import get_signature


def _create_new_prepare_body(context):
    context.sender_ods_code = "A83008"
    context.receiver_ods_code = "FA565"
    context.prescription_item_id = str(uuid.uuid4())
    context.prescription_id = generate_short_form_id(ods_code=context.sender_ods_code)
    context.long_prescription_id = str(uuid.uuid4())
    context.secondary_care_type = "inpatient"
    user_id = CIS2_USERS["prescriber"]["user_id"]
    sds_role_id = CIS2_USERS["prescriber"]["role_id"]
    message_header = generate_message_header(
        sender_ods_code=context.sender_ods_code,
        receiver_ods_code=context.receiver_ods_code,
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
        prescription_item_id=context.prescription_item_id,
        long_prescription_id=context.long_prescription_id,
        secondary_care_type=context.secondary_care_type,
        receiver_ods_code=context.receiver_ods_code,
    )
    patient = generate_patient(
        nhs_number=context.nhs_number, sender_ods_code=context.sender_ods_code
    )
    organization = generate_organization()
    practitioner_role = generate_practitioner_role(sds_role_id=sds_role_id)
    practitioner = generate_practitioner(user_id=user_id)
    body = create_fhir_bundle(
        message_header=message_header,
        medication_request=medication_request,
        patient=patient,
        organization=organization,
        practitioner_role=practitioner_role,
        practitioner=practitioner,
    )
    return body


def prepare_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$prepare"
    context.prepare_body = _create_new_prepare_body(context)
    headers = get_default_headers()
    if "SANDBOX" not in context.config.userdata["env"]:
        headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"Content-Type": "application/json"})
    response = post(
        data=context.prepare_body, url=url, context=context, headers=headers
    )
    the_expected_response_code_is_returned(context, 200)
    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]


def _create_signed_body(context):
    context.signature = get_signature(
        env=context.config.userdata["env"], digest=context.digest
    )
    body = json.loads(context.prepare_body)
    provenance = generate_provenance(
        signature=context.signature, timestamp=context.timestamp
    )
    body["entry"].append(provenance)
    body = json.dumps(body)
    return body


def create_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#prescription-order"
    context.signed_body = _create_signed_body(context)
    headers = get_default_headers()
    if "SANDBOX" not in context.config.userdata["env"]:
        headers.update({"Authorization": f"Bearer {context.auth_token}"})
    post(data=context.signed_body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)


def _create_release_body(context):
    prescription_order_number = context.prescription_id
    group_identifier = generate_group_identifier(
        prescription_order_number=prescription_order_number
    )
    owner = generate_owner(receiver_ods_code=context.receiver_ods_code)
    agent = generate_agent()
    body = create_fhir_parameter(
        group_identifier=group_identifier, owner=owner, agent=agent
    )
    return body


def release_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task/$release"
    context.release_body = _create_release_body(context)
    headers = get_default_headers()
    if "SANDBOX" not in context.config.userdata["env"]:
        headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"NHSD-Session-URID": CIS2_USERS["dispenser"]["role_id"]})
    post(data=context.release_body, url=url, context=context, headers=headers)


def assert_ok_status_code(context):
    the_expected_response_code_is_returned(context, 200)
