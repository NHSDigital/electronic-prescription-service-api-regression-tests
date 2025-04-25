# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from methods.api.cpts_api_methods import (
    get_prescription_list,
    assert_prescription_list,
    assert_empty_prescription_list,
    assert_both_identifier_error,
    get_patient_list,
    assert_patient_list,
)


@when("I request the list of prescriptions using the {identifier}")
def request_prescription_list(context, identifier):
    get_prescription_list(context, identifier)


@when("I request the list of prescriptions that don't exist using the {identifier}")
def request_empty_prescription_list(context, identifier):
    context.nhs_number = "3152699093"
    context.prescription_id = "EBA388-000X26-44ABAC"
    get_prescription_list(context, identifier)


@then("I can see the list of prescriptions")
def verify_prescription_list(context):
    assert_prescription_list(context)


@then("I see an empty list in the response")
def verify_empty_prescription_list(context):
    assert_empty_prescription_list(context)


@then("I am informed not to include both identifiers")
def verify_both_identifier_error(context):
    assert_both_identifier_error(context)


@when("I request the list of patients")
def request_patient_list(context):
    context.family_name = "CHISLETT"
    context.date_of_birth = "2008-09-20"
    context.postcode = "KT19 0ST"

    context.expected_given_name = "OCTAVIA"
    context.expected_gender = "female"
    context.expected_address = ["1 RAVENSFIELD GARDENS", "EPSOM", "SURREY"]
    context.expected_nhs_number = "9449305552"
    get_patient_list(context)


@then("I can see the list of patients")
def verify_patient_list(context):
    assert_patient_list(context)
