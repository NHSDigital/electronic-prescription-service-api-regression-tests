# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
import re

from pages.search_for_a_prescription import SearchForAPrescription


@given("I am on the search for a prescription page")
@when("I am on the search for a prescription page")
@then("I am on the search for a prescription page")
def i_am_on_the_search_prescription_page(context):
    page = SearchForAPrescription(context.page)
    expect(page.temp_text).to_be_visible()


@when("I click on tab {}")
def i_click_on_tab(context, tab_name):
    page = SearchForAPrescription(context.page)
    match tab_name.lower():
        case "prescription id search":
            page.prescription_id_search_tab.click()
        case "nhs number search":
            page.nhs_number_search_tab.click()
        case "basic details search":
            page.basic_details_search_tab.click()
        case _:
            raise AssertionError(f"Unknown tab {tab_name}")


@then("I am on tab {}")
def i_am_on_tab(context, tab_name):
    page = SearchForAPrescription(context.page)
    match tab_name.lower():
        case "prescription id search":
            expect(page.prescription_id_search_header).to_be_visible()
            expect(page.nhs_number_search_header).to_be_visible(visible=False)
            expect(page.basic_details_search_header).to_be_visible(visible=False)
        case "nhs number search":
            expect(page.prescription_id_search_header).to_be_visible(visible=False)
            expect(page.nhs_number_search_header).to_be_visible()
            expect(page.basic_details_search_header).to_be_visible(visible=False)
        case "basic details search":
            expect(page.prescription_id_search_header).to_be_visible(visible=False)
            expect(page.nhs_number_search_header).to_be_visible(visible=False)
            expect(page.basic_details_search_header).to_be_visible()
        case _:
            raise AssertionError(f"Unknown tab {tab_name}")


@then("I can see the search for a prescription header")
def i_can_see_the_search_for_a_prescription_header(context):
    page = SearchForAPrescription(context.page)
    expect(page.hero_banner).to_be_visible()


@when('I enter prescription ID "{prescription_id}" into the input')
def enter_prescription_id(context, prescription_id):
    page = SearchForAPrescription(context.page)
    page.prescription_id_input.fill(prescription_id)


@when("I click the Find a prescription button")
def click_search_button(context):
    page = SearchForAPrescription(context.page)
    page.find_prescription_button.click()


@then('I am redirected to the prescription results page for "{prescription_id}"')
def redirected_to_results(context, prescription_id):
    expected_url = re.compile(
        r"/site/prescription-list-(?:current|past|future)\?prescriptionId="
        + prescription_id
    )
    context.page.wait_for_url(expected_url)


@then('I see a validation message saying "{message}"')
def i_see_validation_message(context, message):
    page = SearchForAPrescription(context.page)
    expect(page.error_summary).to_contain_text(message)


@then("the outcome should be: {outcome}")
def step_with_dynamic_outcome(context, outcome):
    context.execute_steps(f"Then {outcome}")


@when('I enter NHS number "{nhs_number}" into the input')
def enter_nhs_number(context, nhs_number):
    page = SearchForAPrescription(context.page)
    page.nhs_number_input.fill(nhs_number)


@when("I click the Find a patient button")
def click_find_patient_button(context):
    page = SearchForAPrescription(context.page)
    page.find_patient_button.click()


@then("I am on the prescription not found page with redirect to NhsNumSearch")
def redirected_to_nhs_not_found(context):
    expected_url = "/site/prescription-not-found"
    context.page.wait_for_url(expected_url, wait_until="load", timeout=60000)


@then('I am on the prescription list current page with NHS number "{nhs_number}"')
def redirected_to_nhs_current(context, nhs_number):
    expected_url = re.compile(
        rf"/site/prescription-list-current\?nhsNumber={nhs_number}"
    )
    context.page.wait_for_url(expected_url, wait_until="load", timeout=60000)


@then("I see a validation error is displayed")
def i_see_validation_error_displayed(context):
    page = SearchForAPrescription(context.page)
    expect(page.error_summary).to_be_visible()
    assert page.error_summary.locator("li").count() > 0
