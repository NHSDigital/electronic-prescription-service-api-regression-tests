from methods.eps_fhir.api_request_body_generators import (
    create_fhir_bundle,
    create_fhir_signed_bundle,
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


def create_new_prepare_body(context):
    context.sender_ods_code = "RBA"
    context.receiver_ods_code = "FA565"
    context.prescription_id = generate_short_form_id(ods_code=context.sender_ods_code)
    message_header = generate_message_header(
        sender_ods_code=context.sender_ods_code,
        receiver_ods_code=context.receiver_ods_code,
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
    )
    patient = generate_patient(nhs_number=context.nhs_number)
    organization = generate_organization()
    practitioner_role = generate_practitioner_role()
    practitioner = generate_practitioner()
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
    body = create_new_prepare_body(context)
    with open("./records/prepare_prescription.json", "w") as f:
        print(body, file=f)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"Content-Type": "application/json"})
    response = post(data=body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)
    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]
    print(f"DIGEST:{context.digest}")


def create_new_signed_body(context):
    context.signature = get_signature(context.digest, True)
    message_header = generate_message_header(
        sender_ods_code=context.sender_ods_code,
        receiver_ods_code=context.receiver_ods_code,
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
    )
    patient = generate_patient(nhs_number=context.nhs_number)
    organization = generate_organization()
    practitioner_role = generate_practitioner_role()
    practitioner = generate_practitioner()
    provenance = generate_provenance(
        signature=context.signature, timestamp=context.timestamp
    )
    body = create_fhir_signed_bundle(
        message_header=message_header,
        medication_request=medication_request,
        patient=patient,
        organization=organization,
        practitioner_role=practitioner_role,
        practitioner=practitioner,
        provenance=provenance,
    )
    return body


def create_release_body(context):
    prescription_order_number = context.prescription_id
    group_identifier = generate_group_identifier(
        prescription_order_number=prescription_order_number
    )
    owner = generate_owner()
    agent = generate_agent()
    body = create_fhir_parameter(
        group_identifier=group_identifier, owner=owner, agent=agent
    )
    return body


def create_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$process-message#prescription-order"
    body = create_new_signed_body(context)
    with open("./records/create_signed_prescription.json", "w") as f:
        print(body, file=f)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"NHSD-Session-URID": "555083343101"})
    post(data=body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)


def release_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task/$release"
    body = create_release_body(context)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"NHSD-Session-URID": "555083343101"})
    post(data=body, url=url, context=context, headers=headers)
    x_request_id = context.response.headers["x-request-id"]
    print(f"x-request-id: {x_request_id}")
    with open("./records/release_signed_prescription.json", "w") as f:
        print(body, file=f)


def indicate_success(context):
    the_expected_response_code_is_returned(context, 200)
