import json

# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.pfp_api_methods import get_delegated_prescriptions, get_prescriptions
from methods.shared.common import assert_that, get_auth


@when("I am authenticated with {app} app")
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


@when("I request prescriptions of the user I have delegated access to")
def i_request_delegated_prescriptions(context):
    # if (
    #     "sandbox" in context.config.userdata["env"].lower()
    #     and "PFP" in context.config.userdata["product"].upper()
    # ):
    #     context.nhs_number = "9449304130"
    get_delegated_prescriptions(context)


@then("I can see my prescription")
def i_can_see_my_prescription(context):
    json_response = json.loads(context.response.content)
    entries = json_response["entry"]
    bundle = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ][0]["resource"]["entry"][0]["resource"]
    if "sandbox" in context.config.userdata["env"].lower():
        assert_that(bundle["subject"]["identifier"]["value"]).is_equal_to("9449304130")
        assert_that(bundle["groupIdentifier"]["value"]).is_equal_to(
            "24F5DA-A83008-7EFE6Z"
        )
        return
    expected_nhs_number = context.nhs_number
    expected_prescription_id = context.prescription_id
    assert_that(bundle["subject"]["identifier"]["value"]).is_equal_to(
        expected_nhs_number
    )
    assert_that(bundle["groupIdentifier"]["value"]).is_equal_to(
        expected_prescription_id
    )


@then("I can see the delegated prescription")
def i_can_see_the_delegated_prescription(context):
    # json_response = json.loads(context.response.content)
    # with open("delegated prescription.json", "w") as f:
    #     json.dump(json_response, f, indent=2)
    i_can_see_my_prescription(context)
