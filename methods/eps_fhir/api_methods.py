import uuid
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
    context.sender_ods_code = "A83008"
    context.receiver_ods_code = "FA565"
    context.prescription_item_id = str(uuid.uuid4())
    context.prescription_id = generate_short_form_id(ods_code=context.sender_ods_code)
    message_header = generate_message_header(
        sender_ods_code=context.sender_ods_code,
        receiver_ods_code=context.receiver_ods_code,
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
        prescription_item_id=context.prescription_item_id,
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
    context.body = create_new_prepare_body(context)
    with open("./records/prepare_prescription.json", "w") as f:
        print(context.body, file=f)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"Content-Type": "application/json"})
    response = post(data=context.body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)
    context.digest = response.json()["parameter"][0]["valueString"]
    context.timestamp = response.json()["parameter"][1]["valueString"]
    # print(f"DIGEST:{context.digest}")


def convert_prepared_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$convert"
    body = context.body
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"Content-Type": "application/json"})
    response = post(data=body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)
    # Write the response body to a file
    with open("./records/convert_prepare_prescription.xml", "w") as f:
        f.write(response.text)


def create_new_signed_body(context):
    context.signature = get_signature(context.digest, True)
    message_header = generate_message_header(
        sender_ods_code=context.sender_ods_code,
        receiver_ods_code=context.receiver_ods_code,
    )
    medication_request = generate_medication_request(
        short_prescription_id=context.prescription_id,
        code=context.nomination_code,
        prescription_item_id=context.prescription_item_id,
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
    context.signed_body = create_new_signed_body(context)
    with open("./records/create_signed_prescription.json", "w") as f:
        print(context.signed_body, file=f)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    # headers.update({"NHSD-Session-URID": "555083343101"})
    post(data=context.signed_body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)


def convert_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$convert"
    body = context.signed_body
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"Content-Type": "application/json"})
    response = post(data=body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)
    # Write the response body to a file
    with open("./records/convert_signed_prescription.xml", "w") as f:
        f.write(response.text)


def release_signed_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/Task/$release"
    context.release_body = create_release_body(context)
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"NHSD-Session-URID": "555083343101"})
    post(data=context.release_body, url=url, context=context, headers=headers)
    x_request_id = context.response.headers["x-request-id"]
    with open("./records/release_signed_prescription.json", "w") as f:
        # print(f"x-request-id: {x_request_id}")
        print(context.release_body, file=f)


def convert_released_prescription(context):
    url = f"{context.eps_fhir_base_url}/FHIR/R4/$convert"
    body = context.release_body
    headers = get_default_headers()
    headers.update({"Authorization": f"Bearer {context.auth_token}"})
    headers.update({"Content-Type": "application/json"})
    headers.update({"NHSD-Session-URID": "555083343101"})
    response = post(data=body, url=url, context=context, headers=headers)
    the_expected_response_code_is_returned(context, 200)
    # Write the response body to a file
    with open("./records/convert_released_prescription.xml", "w") as f:
        f.write(response.text)


def indicate_success(context):
    the_expected_response_code_is_returned(context, 200)
