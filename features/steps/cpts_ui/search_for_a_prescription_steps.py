# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
import re

from pages.search_for_a_prescription import SearchForAPrescription

EMPTY_FIELD = "<empty>"


@given("I am on the search for a prescription page")
@when("I am on the search for a prescription page")
@then("I am on the search for a prescription page")
def i_am_on_the_search_prescription_page(context):
    page = SearchForAPrescription(context.page)
    expect(page.prescription_id_search_tab).to_be_visible()
    expect(page.prescription_id_input).to_be_visible()


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


@when("I enter text in an input box")
def i_enter_text_in_input_box(context):
    search_box = context.page.get_by_test_id("search-by-prescriptionid-box")
    search_box.click()
    search_box.fill("1234567890")
    search_box.press("ArrowLeft")
    search_box.press("ArrowRight")


@then("I am not redirected to another tab")
def i_am_not_redirected(context):
    page = SearchForAPrescription(context.page)
    expect(page.prescription_id_search_header).to_be_visible()
    expect(page.nhs_number_search_header).to_be_visible(visible=False)
    expect(page.basic_details_search_header).to_be_visible(visible=False)


@then("I can see the search for a prescription header")
def i_can_see_the_search_for_a_prescription_header(context):
    page = SearchForAPrescription(context.page)
    expect(page.hero_banner).to_be_visible()


@when('I enter prescription ID "{prescription_id}" into the input')
def enter_prescription_id(context, prescription_id):
    page = SearchForAPrescription(context.page)
    if prescription_id != EMPTY_FIELD:
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


@then("I see a prescription ID validation error is displayed")
def i_see_prescription_id_validation_error(context):
    page = SearchForAPrescription(context.page)
    expect(page.prescription_id_error).to_be_visible()
    assert page.prescription_id_error.text_content()


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
    url = context.page.url
    assert (
        "site/prescription-not-found?searchType=NhsNumberSearch" in url
    ), f"Unexpected URL: {url}"


@then('I am on the prescription list current page with NHS number "{nhs_number}"')
def redirected_to_nhs_current(context, nhs_number):
    expected_url = re.compile(
        rf"/site/prescription-list-current\?nhsNumber={nhs_number}"
    )
    context.page.wait_for_url(expected_url, wait_until="load", timeout=60000)


@when("I see a validation error is displayed")
@then("I see a validation error is displayed")
def i_see_validation_error_displayed(context):
    page = SearchForAPrescription(context.page)
    expect(page.error_summary).to_be_visible()
    assert page.error_summary.locator("li").count() > 0


@when("I click the first error summary link")
@then("I click the first error summary link")
def click_first_error_link(context):
    context.page.locator('[data-testid="error-summary"] a').first.click()


@then('the focus should be on the "{field_id}" input')
def assert_focus_on_input(context, field_id):
    active = context.page.evaluate("document.activeElement.id")
    assert active == field_id, f"Expected focus on '{field_id}', but got '{active}'"


@when(
    'I search using basic details: "{first}" "{last}" "{day}" "{month}" "{year}" "{postcode}"'
)
def search_by_basic_details(context, first, last, day, month, year, postcode):
    page = SearchForAPrescription(context.page)
    page.basic_details_search_tab.click()

    if first != EMPTY_FIELD:
        page.basic_details_first_name.fill(first)
    if last != EMPTY_FIELD:
        page.basic_details_last_name.fill(last)
    if day != EMPTY_FIELD:
        page.basic_details_dob_day.fill(day)
    if month != EMPTY_FIELD:
        page.basic_details_dob_month.fill(month)
    if year != EMPTY_FIELD:
        page.basic_details_dob_year.fill(year)
    if postcode != EMPTY_FIELD:
        page.basic_details_postcode.fill(postcode)

    page.find_patient_button.click()


@when('I search for a patient using a valid NHS number "{nhs_number}"')
def search_patient_by_nhs_number(context, nhs_number):
    page = SearchForAPrescription(context.page)
    page.nhs_number_search_tab.click()
    page.nhs_number_input.fill(nhs_number)
    page.find_patient_button.click()


@when('I update the basic details DOB fields to "{day}" "{month}" "{year}"')
def update_dob_fields(context, day, month, year):
    page = SearchForAPrescription(context.page)
    page.basic_details_dob_day.fill("")
    page.basic_details_dob_day.fill(day)
    page.basic_details_dob_month.fill("")
    page.basic_details_dob_month.fill(month)
    page.basic_details_dob_year.fill("")
    page.basic_details_dob_year.fill(year)


@then("the DOB inputs should have error styling")
def dob_fields_should_have_error_class(context):
    page = SearchForAPrescription(context.page)
    for field in [
        page.basic_details_dob_day,
        page.basic_details_dob_month,
        page.basic_details_dob_year,
    ]:
        classes = field.get_attribute("class") or ""
        assert (
            "nhsuk-input--error" in classes
        ), f"Expected error class on DOB field, got: {classes}"


@then("the search form should be pre-filled with")
def verify_search_form_prefilled(context):
    page = SearchForAPrescription(context.page)
    mapping = {
        "First name": page.basic_details_first_name,
        "Last name": page.basic_details_last_name,
        "Day": page.basic_details_dob_day,
        "Month": page.basic_details_dob_month,
        "Year": page.basic_details_dob_year,
        "Postcode": page.basic_details_postcode,
    }
    for row in context.table:
        field = row["Field"]
        value = row["Value"]
        locator = mapping[field]
        actual = locator.input_value()
        assert actual == value, f"For {field}: expected '{value}' got '{actual}'"
