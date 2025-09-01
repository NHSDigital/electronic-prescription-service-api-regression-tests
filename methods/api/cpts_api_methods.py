import json
from typing import NotRequired, TypedDict

from features.environment import CIS2_USERS
from methods.api.common_api_methods import get_headers, get
from methods.shared.common import assert_that
from messages.eps_fhir.common_maps import (
    LINE_ITEM_STATUS_MAP,
    NON_DISPENSING_REASON_MAP,
    CANCELLATION_REASON_MAP,
)


def get_prescription_list(context, identifier):
    match identifier.lower():
        case "nhs number":
            url = f"{context.cpts_fhir_base_url}/RequestGroup?nhsNumber={context.nhs_number}"
        case "prescription id":
            url = f"{context.cpts_fhir_base_url}/RequestGroup?prescriptionId={context.prescription_id}"
        case "nhs number and prescription id":
            url = (
                f"{context.cpts_fhir_base_url}/RequestGroup?prescriptionId={context.prescription_id}"
                f"&nhsNumber={context.nhs_number}"
            )
        case _:
            raise AssertionError("Unknown Identifier {}".format(identifier))

    print(url)
    additional_headers = {
        "Content-Type": "application/json",
        "nhsd-organization-uuid": "A83008",
        "nhsd-session-jobrole": "S0030:G0100:R0570",
    }
    headers = get_headers(context, context.auth_method, additional_headers)

    context.response = get(url=url, context=context, headers=headers)


def assert_prescription_list(context):
    json_response = json.loads(context.response.content)
    expected_nhs_number = context.nhs_number
    expected_prescription_id = context.prescription_id
    assert_that(
        json_response["entry"][0]["resource"]["identifier"][0]["value"]
    ).is_equal_to(expected_nhs_number)
    assert_that(
        json_response["entry"][1]["resource"]["identifier"][0]["value"]
    ).is_equal_to(expected_prescription_id)


def assert_empty_prescription_list(context):
    json_response = json.loads(context.response.content)
    assert_that(len(json_response["entry"])).is_equal_to(0)


def assert_both_identifier_error(context):
    json_response = json.loads(context.response.content)
    assert_that(json_response["issue"][0]["diagnostics"]).is_equal_to(
        "Invalid query string parameters; only prescriptionId or nhsNumber must be provided, not both."
    )


def get_prescription_details(context, issue_number):
    query_params = f"?issueNumber={issue_number}" if issue_number else ""
    url = f"{context.cpts_fhir_base_url}/RequestGroup/{context.prescription_id}{query_params}"
    print(url)
    additional_headers = {
        "Content-Type": "application/json",
        "nhsd-organization-uuid": "A83008",
        "nhsd-session-urid": CIS2_USERS["prescriber"]["role_id"],
        "nhsd-session-jobrole": "S0030:G0100:R0570",
    }
    headers = get_headers(context, context.auth_method, additional_headers)

    context.response = get(url=url, context=context, headers=headers)


class MedicationRequestAssertions(TypedDict):
    line_item_id: str
    status: str
    cancellation_reason: NotRequired[str]


class MedicationDispenseAssertions(TypedDict):
    md_id: str
    line_item_id: str
    status: str
    non_dispensing_reason: NotRequired[str]


class PrescriptionDetailsAssertions(TypedDict):
    prescription_id: str
    nhs_number: str
    status: str
    issue_number: NotRequired[int]
    medication_requests: NotRequired[list[MedicationRequestAssertions]]
    medication_dispenses: NotRequired[list[MedicationDispenseAssertions]]


class Resources(TypedDict):
    request_group: dict
    patient: dict
    practitioner_role: list[dict]
    medication_request: list[dict]
    medication_dispense: list[dict]


def assert_prescription_details(
    response_content, assertions: PrescriptionDetailsAssertions
):
    json_response = json.loads(response_content)
    bundle_entries = json_response["entry"]

    resources: Resources = {
        "request_group": {},
        "patient": {},
        "practitioner_role": [],
        "medication_request": [],
        "medication_dispense": [],
    }

    for bundle_entry in bundle_entries:
        resource_type = bundle_entry["resource"]["resourceType"]
        match resource_type:
            case "RequestGroup":
                resources["request_group"] = bundle_entry["resource"]
            case "Patient":
                resources["patient"] = bundle_entry["resource"]
            case "PractitionerRole":
                resources["practitioner_role"].append(bundle_entry["resource"])
            case "MedicationRequest":
                resources["medication_request"].append(bundle_entry["resource"])
            case "MedicationDispense":
                resources["medication_dispense"].append(bundle_entry["resource"])

    print("----------------------")
    print(json_response)
    print("----------------------")
    print(bundle_entries)
    print("----------------------")
    print(resources)
    print("----------------------")

    assert_that(resources["request_group"]["identifier"][0]["value"]).is_equal_to(
        assertions["prescription_id"]
    )
    assert_that(resources["patient"]["identifier"][0]["value"]).is_equal_to(
        assertions["nhs_number"]
    )
    try:
        history = next(
            action
            for action in resources["request_group"]["action"]
            if action["title"] == "Prescription status transitions"
        )
    except StopIteration as exc:
        raise AssertionError("No prescription history found on RequestGroup.") from exc

    print("----------------------")
    print(history)
    print("----------------------")

    if "issue_number" in assertions:
        assert_issue_number(resources["request_group"], assertions["issue_number"])

    if "medication_requests" in assertions:
        assert_medication_requests(
            resources["medication_request"], assertions["medication_requests"]
        )

    if "medication_dispenses" in assertions:
        assert_medication_dispenses(
            resources["medication_dispense"],
            history,
            assertions["medication_dispenses"],
        )


def assert_issue_number(request_group, issue_number: int):
    try:
        repeat_information = next(
            extension
            for extension in request_group["extension"]
            if extension["url"]
            == "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-RepeatInformation"
        )
    except StopIteration as exc:
        raise AssertionError(
            "No RepeatInformation extension found on RequestGroup."
        ) from exc

    try:
        number_of_repeats_issued = next(
            extension
            for extension in repeat_information["extension"]
            if extension["url"] == "numberOfRepeatsIssued"
        )
    except StopIteration as exc:
        raise AssertionError(
            "No numberOfRepeatsIssued extension on RepeatInformation extension."
        ) from exc

    assert_that(number_of_repeats_issued["valueInteger"]).is_equal_to(issue_number)


def assert_medication_requests(
    medication_requests: list, assertions: list[MedicationRequestAssertions]
):
    for mr_assertions in assertions:
        try:
            medication_request = next(
                mr
                for mr in medication_requests
                if mr["identifier"][0]["value"] == mr_assertions["line_item_id"]
            )
        except StopIteration as exc:
            raise AssertionError(
                f"MedicationRequest with for line item id {mr_assertions["line_item_id"]} not found in Bundle."
            ) from exc
        assert_medication_request_details(medication_request, mr_assertions)


def assert_medication_request_details(
    medication_request, assertions: MedicationRequestAssertions
):
    try:
        status = next(
            extension
            for extension in medication_request["extension"]
            if extension["url"]
            == "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-DispensingInformation"
        )
    except StopIteration as exc:
        raise AssertionError(
            "No DispensingInformation extension found on MedicationRequest."
        ) from exc

    assert_that(status["extension"][0]["valueCoding"]["display"]).is_equal_to(
        assertions["status"]
    )
    assert_that(status["extension"][0]["valueCoding"]["code"]).is_equal_to(
        LINE_ITEM_STATUS_MAP[assertions["status"]]
    )

    if "cancellation_reason" in assertions:
        assert_that(
            medication_request["statusReason"]["coding"][0]["display"]
        ).is_equal_to(assertions["cancellation_reason"])
        assert_that(
            medication_request["statusReason"]["coding"][0]["code"]
        ).is_equal_to(CANCELLATION_REASON_MAP[assertions["cancellation_reason"]])


def assert_medication_dispenses(
    medication_dispenses: list, history, assertions: list[MedicationDispenseAssertions]
):
    md_ids = {}
    for action in history["action"]:
        if action["title"] == "Dispense notification successful":
            try:
                dn_id_code = next(
                    code
                    for code in action["code"]
                    if code["coding"][0]["system"]
                    == "https://tools.ietf.org/html/rfc4122"
                )
            except StopIteration as exc:
                raise AssertionError(
                    "No dispense notification ID code found on history event."
                ) from exc

            dn_id = dn_id_code["coding"][0]["code"]
            md_ids[dn_id] = []
            for ref_action in action["action"]:
                md_ref = ref_action["resource"]["reference"]
                md_ids[dn_id].append(md_ref[9:])

    for md_assertions in assertions:
        try:
            medication_dispense = next(
                md
                for md in medication_dispenses
                if md["id"] in md_ids[md_assertions["md_id"]]
                and md["identifier"][0]["value"] == md_assertions["line_item_id"]
            )
        except StopIteration as exc:
            raise AssertionError(
                f"MedicationDispense for dispense notification id {md_assertions["md_id"]} and line item id {md_assertions["line_item_id"]} not found in Bundle"  # noqa: E501
            ) from exc

        assert_medication_dispense_details(medication_dispense, md_assertions)


def assert_medication_dispense_details(
    medication_dispense, assertions: MedicationDispenseAssertions
):
    assert_that(medication_dispense["type"]["coding"][0]["display"]).is_equal_to(
        assertions["status"]
    )
    assert_that(medication_dispense["type"]["coding"][0]["code"]).is_equal_to(
        LINE_ITEM_STATUS_MAP[assertions["status"]]
    )

    if "non_dispensing_reason" in assertions:
        assert_that(
            medication_dispense["statusReasonCodeableConcept"]["coding"][0]["display"]
        ).is_equal_to(assertions["non_dispensing_reason"])
        assert_that(
            medication_dispense["statusReasonCodeableConcept"]["coding"][0]["code"]
        ).is_equal_to(NON_DISPENSING_REASON_MAP[assertions["non_dispensing_reason"]])


def assert_prescription_not_found(context):
    json_response = json.loads(context.response.content)
    print(json_response)
    assert_that(json_response["issue"][0]["code"]).is_equal_to("not-found")


def assert_path_parameter_not_provided(context):
    json_response = json.loads(context.response.content)
    print(json_response)
    assert_that(json_response["issue"][0]["code"]).is_equal_to("value")
