import json

from methods.api.common_api_methods import get_headers, get
from methods.shared.common import assert_that


def get_prescription_details(context):
    url = f"{context.cpts_fhir_base_url}/RequestGroup/{context.prescription_id}"
    additional_headers = {"Content-Type": "application/json"}
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
