import json

# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.pfp_api_methods import get_prescriptions
from methods.shared.common import assert_that, get_auth


@when("I am authenticated")
def i_am_authenticated(context):
    context.auth_token = get_auth("dispenser", "int", "PFP-APIGEE")


@when("I request my prescriptions")
def i_request_my_prescriptions(context):
    get_prescriptions(context)


@then("I can see my prescription")
def i_can_see_my_prescription(context):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    bundle = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ][0]["resource"]["entry"][0]["resource"]
    assert_that(bundle["subject"]["identifier"]["value"]).is_equal_to(
        context.nhs_number
    )
    assert_that(bundle["groupIdentifier"]["value"]).is_equal_to(context.prescription_id)
