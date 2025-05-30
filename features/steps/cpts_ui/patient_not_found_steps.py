# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.patient_not_found import PatientNotFoundMessage


@then("I am on the patient not found page")
def i_am_on_patient_not_found_page(context):
    page = PatientNotFoundMessage(context.page)
    expect(page.results_page).to_be_visible()
