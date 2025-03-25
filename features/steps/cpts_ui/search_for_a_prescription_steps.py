# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.search_for_a_prescription import SearchForAPrescription


@given("I am on the search for a prescription page")
@when("I am on the search for a prescription page")
@then("I am on the search for a prescription page")
def i_am_on_the_search_prescription_page(context):
    search_for_a_prescription = SearchForAPrescription(context.page)
    expect(search_for_a_prescription.temp_text).to_be_visible()


@when("I click on tab {}")
def i_click_on_tab(context, tab_name):
    search_for_a_prescription = SearchForAPrescription(context.page)
    match tab_name.lower():
        case "prescription id search":
            search_for_a_prescription.prescription_id_search_tab.click()
        case "nhs number search":
            search_for_a_prescription.nhs_number_search_tab.click()
        case "basic details search":
            search_for_a_prescription.basic_details_search_tab.click()
        case _:
            raise AssertionError("Unknown tab {}".format(tab_name))


@then("I am on tab {}")
def i_am_on_tab(context, tab_name):
    search_for_a_prescription = SearchForAPrescription(context.page)
    match tab_name.lower():
        case "prescription id search":
            expect(
                search_for_a_prescription.prescription_id_search_header
            ).to_be_visible()
            expect(search_for_a_prescription.nhs_number_search_header).to_be_visible(
                visible=False
            )
            expect(search_for_a_prescription.basic_details_search_header).to_be_visible(
                visible=False
            )
        case "nhs number search":
            expect(
                search_for_a_prescription.prescription_id_search_header
            ).to_be_visible(visible=False)
            expect(search_for_a_prescription.nhs_number_search_header).to_be_visible()
            expect(search_for_a_prescription.basic_details_search_header).to_be_visible(
                visible=False
            )
        case "basic details search":
            expect(
                search_for_a_prescription.prescription_id_search_header
            ).to_be_visible(visible=False)
            expect(search_for_a_prescription.nhs_number_search_header).to_be_visible(
                visible=False
            )
            expect(
                search_for_a_prescription.basic_details_search_header
            ).to_be_visible()
        case _:
            raise AssertionError("Unknown tab {}".format(tab_name))


@then("I can see the search for a prescription header")
def i_can_see_the_search_for_a_prescription_header(context):
    search_for_a_prescription = SearchForAPrescription(context.page)
    expect(search_for_a_prescription.hero_banner).to_be_visible()


@when('I enter prescription ID "{prescription_id}" into the input')
def enter_prescription_id(context, prescription_id):
    search_input = context.page.get_by_test_id("prescription-id-input")
    search_input.fill(prescription_id)


@when("I click the Find a prescription button")
def click_search_button(context):
    button = context.page.get_by_test_id("find-prescription-button")
    button.click()


@then('I am redirected to the prescription results page for "{prescription_id}"')
def redirected_to_results(context, prescription_id):
    expected_url = f"/site/prescription-results?prescriptionId={prescription_id}"
    context.page.wait_for_url(lambda url: expected_url in url)


@then("I am redirected to the prescription not found page")
def redirected_to_not_found(context):
    context.page.wait_for_url(lambda url: "/site/prescription-not-found" in url)


@then('I see a validation message saying "{message}"')
def i_see_validation_message(context, message):
    error_summary = context.page.get_by_test_id("error-summary")
    expect(error_summary).to_contain_text(message)


@then("the outcome should be: {outcome}")
def step_with_dynamic_outcome(context, outcome):
    context.execute_steps(f"Then {outcome}")
