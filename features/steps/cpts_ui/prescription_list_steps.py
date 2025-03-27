from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_list_page import PrescriptionListPage
from pages.search_for_a_prescription import SearchForAPrescription


@when('I search for a prescription using a valid prescription ID "{prescription_id}"')
def search_using_prescription_id(context, prescription_id):
    # Fill the input before clicking
    search_input = context.page.get_by_test_id("prescription-id-input")
    search_input.fill(prescription_id)

    # Use data-testid to find the button instead of text content
    context.page.locator('[data-testid="find-prescription-button"]').click()


@given("I have accessed the prescription list page using a prescription ID search")
def access_list_page_via_prescription_id(context):
    # Navigate directly to the results page with a prescription ID parameter
    context.page.goto(
        context.cpts_ui_base_url
        + "site/prescription-results?prescriptionId=C0C757-A83008-C2D93O"
    )

    # Verify we're on the prescription list page using data-testid
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.page_container).to_be_visible()


@given("I have accessed the prescription list page using an NHS number search")
def access_list_page_via_nhs_number(context):
    # Navigate directly to the results page with an NHS number parameter
    context.page.goto(
        context.cpts_ui_base_url + "site/prescription-results?nhsNumber=123456"
    )

    # Verify we're on the prescription list page using data-testid
    prescription_list_page = PrescriptionListPage(context.page)
    expect(prescription_list_page.page_container).to_be_visible()


@then(
    'I am redirected to the prescription list page with prescription ID "{prescription_id}"'
)
def verify_prescription_list_page(context, prescription_id):
    # Wait until the URL includes prescription-results
    context.page.wait_for_url(lambda url: "site/prescription-results" in url)

    current_url = context.page.url
    assert (
        "site/prescription-results" in current_url
    ), f"Expected URL to contain 'site/prescription-results', got: {current_url}"
    assert (
        "prescriptionId=" in current_url
    ), f"Expected URL to contain 'prescriptionId=', got: {current_url}"

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
        "site/search" in current_url
    ), f"Expected URL to contain 'site/search', got: {current_url}"

    # Use the POM to verify we're on the Prescription ID search tab
    search_page = SearchForAPrescription(context.page)
    expect(search_page.prescription_id_search_header).to_be_visible()


@then("I am redirected to the NHS number search tab")
def verify_redirect_to_nhs_number_tab(context):
    # Use more relaxed URL checking
    current_url = context.page.url
    assert (
        "site/search" in current_url
    ), f"Expected URL to contain 'site/search', got: {current_url}"

    # Use the POM to verify we're on the NHS number search tab
    search_page = SearchForAPrescription(context.page)
    expect(search_page.nhs_number_search_header).to_be_visible()
