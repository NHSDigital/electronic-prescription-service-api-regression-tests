import json

from features.environment import CIS2_USERS
from methods.api.common_api_methods import get_headers, get
from methods.shared.common import assert_that

PRESCRIPTION_DISPENSED = "9D4C80-A83008-5EA4D3"


def get_prescription_details(context):
    url = f"{context.cpts_fhir_base_url}/RequestGroup/{PRESCRIPTION_DISPENSED}"
    print(url)
    additional_headers = {
        "Content-Type": "application/json",
        "nhsd-organization-uuid": "A83008",
        "nhsd-session-urid": CIS2_USERS["prescriber"]["role_id"],
        "nhsd-session-jobrole": "S0030:G0100:R0570",
    }
    headers = get_headers(context, context.auth_method, additional_headers)

    context.response = get(url=url, context=context, headers=headers)


def assert_prescription_details(context):
    json_response = json.loads(context.response.content)
    expected_nhs_number = context.nhs_number
    expected_prescription_id = context.prescription_id
    assert_that(json_response["contained"][0]["identifier"][0]["value"]).is_equal_to(
        expected_nhs_number
    )
    assert_that(json_response["identifier"][0]["value"]).is_equal_to(
        expected_prescription_id
    )
