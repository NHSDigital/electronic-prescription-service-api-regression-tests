from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
import re

from pages.prescription_list_page import PrescriptionListPage
from pages.search_for_a_prescription import SearchForAPrescription


@when('I search for a prescription using a valid prescription ID "{prescription_id}"')
def search_using_prescription_id(context, prescription_id):
    # Fill the input before clicking
    search_input = context.page.get_by_test_id("prescription-id-input")
    search_input.fill(prescription_id)

    context.page.get_by_test_id("find-prescription-button").click()


@given("I have accessed the prescription list page using a prescription ID search")
def access_list_page_via_prescription_id(context):
    # Navigate directly to the results page with a prescription ID parameter
    # FIXME: This should not be hardcoded once we can actually search for real data
    context.page.goto(
        context.cpts_ui_base_url
        + "site/prescription-list-current?prescriptionId=C0C757-A83008-C2D93O"
    )

    # Verify we're on the prescription list page using data-testid
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.page_container).to_be_visible()


@given("I have accessed the prescription list page using an NHS number search")
def access_list_page_via_nhs_number(context):
    # Navigate directly to the results page with an NHS number parameter
    # FIXME: This should not be hardcoded once we can actually search for real data
    context.page.goto(
        context.cpts_ui_base_url + "site/prescription-list-current?nhsNumber=1234567890"
    )

    # Verify we're on the prescription list page using data-testid
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.page_container).to_be_visible()


@then(
    'I am redirected to the prescription list page with prescription ID "{prescription_id}"'
)
def verify_prescription_list_page(context, prescription_id):
    expected_url = re.compile(
        r"/site/prescription-list-(?:current|past|future)\?prescriptionId="
        + prescription_id
    )
    context.page.wait_for_url(expected_url)

    # Verify we're on the prescription list page using POM
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.page_container).to_be_visible()


@then('I can see the heading "{heading_text}"')
def verify_heading(context, heading_text):
    # Use POM
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.heading).to_be_visible()
    # Still verify text content as that's the purpose of this step
    expect(prescription_list_page.heading).to_have_text(heading_text)


@then("I can see the results count message")
def verify_results_count(context):
    # Use POM
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.results_count).to_be_visible()
    # Since we're checking for the content pattern, we still need some text verification
    # but can make it more flexible
    count_text = prescription_list_page.results_count.text_content() or ""
    assert (
        "results" in count_text.lower()
    ), f"Expected 'results' in results count text: {count_text}"


@given("I am on the prescription list page for prescription ID {prescription_id}")
def i_am_on_the_prescription_list_page(context, prescription_id: str):
    context.execute_steps(
        f"""
        Given I am on the search for a prescription page
        When I search for a prescription using a valid prescription ID {prescription_id}
        Then I am redirected to the prescription list page with prescription ID {prescription_id}
        And I can see the heading "Prescriptions list"
    """
    )


@then("I can see the appropriate prescription results tab headings")
def i_see_results_headings(context):
    prescription_list_page = PrescriptionListPage(context.page)
    expect(
        prescription_list_page.current_prescriptions_results_tab_heading
    ).to_be_visible()
    expect(
        prescription_list_page.future_prescriptions_results_tab_heading
    ).to_be_visible()
    expect(
        prescription_list_page.past_prescriptions_results_tab_heading
    ).to_be_visible()


@then("I can see the current prescriptions results table")
def i_see_current_prescriptions_results_tab(context):
    prescription_list_page = PrescriptionListPage(context.page)
    expect(
        prescription_list_page.current_prescriptions_results_tab_table
    ).to_be_visible()

    expect(
        prescription_list_page.future_prescriptions_results_tab_table
    ).not_to_be_visible()
    expect(
        prescription_list_page.past_prescriptions_results_tab_table
    ).not_to_be_visible()


@then("I can see the future prescriptions results table")
def i_see_future_prescriptions_results_tab(context):
    prescription_list_page = PrescriptionListPage(context.page)
    expect(
        prescription_list_page.future_prescriptions_results_tab_table
    ).to_be_visible()

    expect(
        prescription_list_page.current_prescriptions_results_tab_table
    ).not_to_be_visible()
    expect(
        prescription_list_page.past_prescriptions_results_tab_table
    ).not_to_be_visible()


@then("I can see the past prescriptions results table")
def i_see_past_prescriptions_results_tab(context):
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.past_prescriptions_results_tab_table).to_be_visible()

    expect(
        prescription_list_page.current_prescriptions_results_tab_table
    ).not_to_be_visible()
    expect(
        prescription_list_page.future_prescriptions_results_tab_table
    ).not_to_be_visible()


@when("I click on the current prescriptions tab heading")
def i_click_current_prescription_tab_heading(context):
    prescription_list_page = PrescriptionListPage(context.page)
    prescription_list_page.current_prescriptions_results_tab_heading.click()


@when("I click on the past prescriptions tab heading")
def i_click_past_prescription_tab_heading(context):
    prescription_list_page = PrescriptionListPage(context.page)
    prescription_list_page.past_prescriptions_results_tab_heading.click()


@when("I click on the future prescriptions tab heading")
def i_click_future_prescription_tab_heading(context):
    prescription_list_page = PrescriptionListPage(context.page)
    prescription_list_page.future_prescriptions_results_tab_heading.click()


@when('I click on the "Go back" link')
def click_go_back_link(context):
    # Use POM
    prescription_list_page = PrescriptionListPage(context.page)
    prescription_list_page.back_link.click()


@then("I am redirected to the prescription ID search tab")
def verify_redirect_to_prescription_id_tab(context):
    # Use more relaxed URL checking
    current_url = context.page.url
    assert (
        "site/search-by-prescription-id" in current_url
    ), f"Expected URL to contain 'site/search-by-prescription-id', got: {current_url}"

    # Use the POM to verify we're on the Prescription ID search tab
    search_page = SearchForAPrescription(context.page)
    expect(search_page.prescription_id_search_header).to_be_visible()


@then("I am redirected to the NHS number search tab")
def verify_redirect_to_nhs_number_tab(context):
    # Use more relaxed URL checking
    current_url = context.page.url
    assert (
        "site/search-by-nhs-number" in current_url
    ), f"Expected URL to contain 'site/search-by-nhs-number', got: {current_url}"

    # Use the POM to verify we're on the NHS number search tab
    search_page = SearchForAPrescription(context.page)
    expect(search_page.nhs_number_search_header).to_be_visible()
