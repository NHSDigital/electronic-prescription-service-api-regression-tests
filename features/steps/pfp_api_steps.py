import json

# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.pfp_api_methods import get_prescriptions
from methods.shared.common import assert_that, get_auth
from methods.api.eps_api_methods import call_validator
from messages.eps_fhir.prescription import Prescription


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
    print(context.response)


@when("I attempt to request my prescriptions via '{method}' method")
def i_attempt_to_request_my_prescriptions_via_method(context, method):
    if (
        "sandbox" in context.config.userdata["env"].lower()
        and "PFP" in context.config.userdata["product"].upper()
    ):
        context.nhs_number = "9449304130"
    get_prescriptions(context, method=method)


@then("I can see my prescription")
def i_can_see_my_prescription(context):
    json_response = json.loads(context.response.content)
    print(json_response)
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


@then("I cannot see my prescription")
def i_cannot_see_my_prescription(context):
    json_response = json.loads(context.response.content)
    print(json_response)
    entries = json_response["entry"]
    bundle_entries = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]
    assert_that(len(bundle_entries)).is_equal_to(0)
    assert_that(json_response["total"]).is_equal_to(0)


@then("I validate the response for FHIR compliance")
def i_validate_the_response_for_fhir_compliance(context):
    json_response = json.loads(context.response.content)
    print(json_response)

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
    print(json_response)
    entries = json_response["entry"]
    bundle_entries = [
        entry for entry in entries if entry["resource"]["resourceType"] == "Bundle"
    ]
    for bundle_entry in bundle_entries:
        prescription_type = bundle_entry["resource"]["courseOfTherapyType"]["coding"][
            0
        ]["code"]
        assert_that(prescription_type).is_not_equal_to("continuous-repeat-dispensing")
