import json

from features.environment import CIS2_USERS
from methods.api.common_api_methods import get_headers, get
from methods.shared.common import assert_that

PRESCRIPTION_ID_NOT_EXIST = "111111-222222-333333"


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


def assert_prescription_details(context, issue_number):
    json_response = json.loads(context.response.content)
    expected_nhs_number = context.nhs_number
    expected_prescription_id = context.prescription_id
    assert_that(json_response["contained"][0]["identifier"][0]["value"]).is_equal_to(
        expected_nhs_number
    )
    assert_that(json_response["identifier"][0]["value"]).is_equal_to(
        expected_prescription_id
    )
    if issue_number:
        repeat_information = next(
            extension
            for extension in json_response["extension"]
            if extension["url"]
            == "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-RepeatInformation"
        )
        number_of_repeats_issued = next(
            extension
            for extension in repeat_information["extension"]
            if extension["url"] == "numberOfRepeatsIssued"
        )
        assert_that(number_of_repeats_issued["valueInteger"]).is_equal_to(issue_number)


def get_prescription_not_found(context):
    url = f"{context.cpts_fhir_base_url}/RequestGroup/{PRESCRIPTION_ID_NOT_EXIST}"
    print(url)
    additional_headers = {
        "Content-Type": "application/json",
        "nhsd-organization-uuid": "A83008",
        "nhsd-session-urid": CIS2_USERS["prescriber"]["role_id"],
        "nhsd-session-jobrole": "S0030:G0100:R0570",
    }
    headers = get_headers(context, context.auth_method, additional_headers)

    context.response = get(url=url, context=context, headers=headers)


def assert_prescription_not_found(context):
    json_response = json.loads(context.response.content)
    print(json_response)
    assert_that(json_response["issue"][0]["code"]).is_equal_to("not-found")


def get_path_parameter_not_provided(context):
    url = f"{context.cpts_fhir_base_url}/RequestGroup/"
    print(url)

    headers = get_headers(context, context.auth_method)

    context.response = get(url=url, context=context, headers=headers)


def assert_path_parameter_not_provided(context):
    json_response = json.loads(context.response.content)
    print(json_response)
    assert_that(json_response["issue"][0]["code"]).is_equal_to("value")
