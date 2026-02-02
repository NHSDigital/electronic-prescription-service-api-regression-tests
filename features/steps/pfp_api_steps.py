import json

# pylint: disable=no-name-in-module
from behave import when, then, step  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.pfp_api_methods import get_prescriptions
from methods.shared.common import assert_that, get_auth
from methods.api.eps_api_methods import call_validator
from messages.eps_fhir.prescription import Prescription


@step("I am authenticated with {app} app")
def i_am_authenticated(context, app):
    env = context.config.userdata["env"].lower()
    if "sandbox" in env:
        return
    context.auth_token = get_auth(env, app)


@when("I request my prescriptions")
def i_request_my_prescriptions(context):
    if (
        "sandbox" in context.config.userdata["env"].lower()
        and "PFP" in context.config.userdata["product"].upper()
    ):
        context.nhs_number = "9449304130"
    get_prescriptions(context)


@when("I request prescriptions for NHS number '{nhs_number}'")
def i_request_prescriptions_for_nhs_number(context, nhs_number):
    context.nhs_number = nhs_number
    get_prescriptions(context)


@when("I check the prescription item statuses for '{status}'")
def i_check_the_prescription_item_statuses_for_status(context, status):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    bundles = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]

    # Extract all status codes from MedicationRequest extensions
    status_codes = [
        extension["valueCoding"]["code"]
        for bundle in bundles
        for entry in bundle["resource"]["entry"]
        if entry["resource"]["resourceType"] == "MedicationRequest"
        for extension in entry["resource"]["extension"][0]["extension"]
        if extension["url"] == "status"
    ]

    # Assert all status codes match the expected status
    for status_code in status_codes:
        assert_that(status_code).is_equal_to(status)


@then("I can see my prescription '{prescription_id}'")
def i_can_see_my_prescription_by_id(context, prescription_id):
    context.prescription_id = prescription_id
    context.execute_steps("""
        Then I can see my prescription
        """)


@then("I can see my prescription and it has a status of '{status}'")
def i_can_see_my_prescription_inc_updates(context, status=None):
    assert_that(context.response.status_code).is_equal_to(200)
    print(f"Checking prescription: {context.prescription_id} for {context.nhs_number}")
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    if entries[0]:
        print(f"Diagnostics info from response: {entries[0]}")
    bundle = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ][0]["resource"]["entry"][0]["resource"]
    if "sandbox" in context.config.userdata["env"].lower():
        assert_that(bundle["subject"]["identifier"]["value"]).is_equal_to("9449304130")
        assert_that(bundle["groupIdentifier"]["value"]).is_equal_to(
            "24F5DA-A83008-7EFE6Z"
        )
        return
    print(
        f"Prescription retrieved: {bundle['groupIdentifier']['value']} for {bundle['subject']['identifier']['value']}"
    )
    expected_nhs_number = context.nhs_number
    expected_prescription_id = context.prescription_id
    assert_that(bundle["subject"]["identifier"]["value"]).is_equal_to(
        expected_nhs_number
    )
    assert_that(bundle["groupIdentifier"]["value"]).is_equal_to(
        expected_prescription_id
    )

    # only check in int as status updates are toggled off in lower environments
    if context.config.userdata["env"].lower() == "int" and status:
        actual_status = bundle["status"]
        print(f"Status found: {actual_status}")
        assert_that(actual_status).is_equal_to(status)

    if context.receiver_ods_code == "FA565":
        address_texts = [
            resource["resource"]["address"][0]["text"]
            for entry in entries
            for resource in entry["resource"]["entry"]
            if resource["resource"]["resourceType"] == "Organization"
            and "address" in resource["resource"]
            and resource["resource"]["address"]
            and "text" in resource["resource"]["address"][0]
        ]
        print(
            f"Address texts found: {address_texts} for ODS code {context.receiver_ods_code}"
        )
        assert_that(address_texts).is_not_empty()
        assert_that(address_texts[0]).is_equal_to(
            "63 BRIARFIELD ROAD, TIMPERLEY, ALTRINCHAM, CHESHIRE, CHESHIRE, WA15 7DD"
        )
    elif context.receiver_ods_code == "FLM49":
        urls = [
            resource["resource"]["telecom"][0]["value"]
            for entry in entries
            for resource in entry["resource"]["entry"]
            if resource["resource"]["resourceType"] == "Organization"
            and "telecom" in resource["resource"]
            and resource["resource"]["telecom"]
            and "system" in resource["resource"]["telecom"][0]
            and resource["resource"]["telecom"][0]["system"] == "url"
        ]
        assert_that(urls).is_not_empty()
        assert_that(urls[0]).is_equal_to("www.pharmacy2u.co.uk")


@then("I can see my prescription")
def i_can_see_my_prescription(context):
    i_can_see_my_prescription_inc_updates(context)


@then("I can see '{number}' of my prescriptions")
def i_can_see_my_prescriptions(context, number):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    total = json_response["total"]
    prescription_bundles = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]

    assert_that(total).is_equal_to(int(number))
    assert_that(len(prescription_bundles)).is_equal_to(int(number))
    assert_that(total).is_less_than_or_equal_to(25)


@then("I cannot see my unreleased prescriptions")
def i_cannot_see_my_prescription(context):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    bundle_entries = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]
    assert_that(len(bundle_entries)).is_equal_to(0)
    assert_that(json_response["total"]).is_equal_to(0)


@then("I validate the response for FHIR compliance")
def i_validate_the_response_for_fhir_compliance(context):
    context.nomination_code = "0004"
    context.intent = "order"
    context.type_code = "acute"
    validate_body = Prescription(context).body

    call_validator(context, "eps_fhir_dispensing", "true", validate_body)

    print("validation response:")
    print(context.response.content)
    print(context.response.status_code)


@then("I do not see an eRD prescription")
def i_do_not_see_an_erd_prescription(context):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    bundle_entries = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]
    for bundle_entry in bundle_entries:
        prescription_type = bundle_entry["resource"]["courseOfTherapyType"]["coding"][
            0
        ]["code"]
        assert_that(prescription_type).is_not_equal_to("continuous-repeat-dispensing")


@then("I validate the prescription matches my prepared prescription")
def i_validate_the_response_prescription_matches_my_prepared_prescription(context):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]

    # Mock prescription construct builds the same "prescription" each time
    # so using 0 index is safe for asserting values
    bundle = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]

    prescription = bundle[0]["resource"]["entry"]

    # Dynamically test against Medication Requests
    expected_entries = json.loads(context.prepare_body)["entry"]
    returned_medication_codeable_concepts = [
        each
        for each in prescription
        if each["resource"]["resourceType"] == "MedicationRequest"
    ]
    expected_medication_codeable_concepts = [
        each
        for each in expected_entries
        if each["resource"]["resourceType"] == "MedicationRequest"
    ]

    expected_items = expected_medication_codeable_concepts[0]["resource"][
        "medicationCodeableConcept"
    ]["coding"]
    returned_items = returned_medication_codeable_concepts[0]["resource"][
        "medicationCodeableConcept"
    ]["coding"]
    for item in expected_items:
        for key, value in item.items():
            if key != "system":
                assert_that(returned_items[0][key]).is_equal_to(value)
            else:
                # Skip system as the mock prescription uses http vs. PFP returning https address
                pass


@when("I set the statuses I will update through")
def set_statuses_for_pfp(context):
    context.statuses = [row["Status"] for row in context.table]


@then(
    "I process the status updates for the prescription items and verify they are returned"
)
def process_status_updates_and_verify(context):
    # For each prescription ID in the scenario, update the status according to data table
    # Loop over all available statuses
    # DON'T COPY THIS -- It's crude for now until we come back to it.
    for status in context.statuses:
        print(f"Processing status update to {status} for all prescription IDs")
        context.execute_steps("""
            When I am authorised to send prescription updates
            """)
        for prescription_id in context.prescription_ids:
            context.prescription_id = prescription_id
            print(f"Processing status update for prescription ID: {prescription_id}")
            if (
                status.upper() == "COLLECTED"
                or status.upper() == "DISPENSED"
                or status.upper() == "NOT DISPENSED"
            ):
                terminal = "completed"
            else:
                terminal = "in-progress"

            context.execute_steps(f"""
                When I send a '{status}' update with a status of '{terminal}'
                """)
        # Call the PFP API to get the prescriptions and verify the statuses
        print(f"Verifying updated prescription statuses to be {status}")
        context.execute_steps(f"""
            When I am authenticated with PFP-APIGEE app
            And I request my prescriptions
            And I check the prescription item statuses for '{status}'
            """)
