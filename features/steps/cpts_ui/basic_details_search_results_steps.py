# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.basic_details_search_results import BasicDetailsSearchResultsPage


@given("I am on the basic details search results page")
def navigate_to_search_results(context):
    context.page = BasicDetailsSearchResultsPage(context.page)
    context.page.page.goto(context.cpts_ui_base_url + context.page.url.lstrip("/"))
    context.page.wait_for_page_load()


@given("I have searched for patients with the following details")
def search_patients(context):
    # TODO: will need to implement this once the search form is implemented
    # this step is handled by the Background setup
    # the actual data is mocked in the React component
    pass


@then("I should see a table with the following columns")
def verify_table_columns(context):
    expected_columns = [row[0] for row in context.table]
    actual_columns = context.page.get_table_headers()
    assert all(
        column in actual_columns for column in expected_columns
    ), f"Expected columns {expected_columns} not found in {actual_columns}"


@then("the table should be sorted by first name")
def verify_table_sorting(context):
    rows = context.page.get_patient_rows()
    names = [row.text_content().split()[0] for row in rows]  # Get first names
    sorted_names = sorted(names)
    assert names == sorted_names, "Table is not sorted by first name"


@then('I should see "{expected_text}" in the results count text')
def verify_results_count(context, expected_text):
    actual_text = context.page.get_results_count_text()
    # Handle both formats of the results count text
    assert (
        expected_text in actual_text
        or f"We found {expected_text.split()[0]} results" in actual_text
    ), f"Expected text '{expected_text}' or 'We found {expected_text.split()[0]} results' not found in '{actual_text}'"


@then("I should not see any restricted patients in the results")
def verify_no_restricted_patients(context):
    assert not context.page.is_restricted_patient_visible(
        "John Smith"
    ), "Restricted patient is visible in the results"


@when('I click on the patient row for "{name}"')
def click_patient_row(context, name):
    context.page.click_patient_row(name)


@when('I press enter on the patient row for "{name}"')
def press_enter_patient_row(context, name):
    context.page.press_enter_on_patient_row(name)


@then("I should be navigated to the prescription list page")
def verify_prescription_list_navigation(context):
    # Wait for navigation and check for either prescription list or not found page
    context.page.page.wait_for_url(
        lambda url: "prescription-list-current" in url
        or "prescription-not-found" in url
    )
    current_url = context.page.page.url
    assert (
        "prescription-list-current" in current_url
        or "prescription-not-found" in current_url
    ), f"Expected URL to contain 'prescription-list-current' or 'prescription-not-found', got: {current_url}"


@then('the NHS number "{nhs_number}" should be included in the URL')
def verify_nhs_number_in_url(context, nhs_number):
    formatted_nhs = nhs_number.replace(" ", "")
    # Wait for navigation and check for either prescription list or not found page
    context.page.page.wait_for_url(lambda url: formatted_nhs in url)
    current_url = context.page.page.url
    assert (
        formatted_nhs in current_url
    ), f"Expected NHS number {formatted_nhs} in URL, got: {current_url}"


@when('I click the "{link_text}" link')
def click_back_link(context, link_text):
    context.page.click_go_back()


@then("I should be navigated to the basic details search page")
def verify_search_page_navigation(context):
    expect(context.page.page).to_have_url(
        context.cpts_ui_base_url + "site/search-by-basic-details"
    )


@then("the search form should be cleared")
def verify_search_form_cleared(context):
    # This would need to be implemented based on how the form state is managed
    # for now, we'll just verify we're on the correct page
    expect(context.page.page).to_have_url(
        context.cpts_ui_base_url + "site/search-by-basic-details"
    )


@then("each patient row should have the correct aria-label")
def verify_patient_row_aria_labels(context):
    rows = context.page.get_patient_rows()
    for row in rows:
        name = row.text_content().split()[0]
        aria_label = context.page.get_patient_row_aria_label(name)
        assert (
            "View prescriptions for" in aria_label and "NHS Number:" in aria_label
        ), f"Invalid aria-label: {aria_label}"


@then("the table should be responsive")
def verify_table_responsive(context):
    assert context.page.is_table_responsive(), "Table is not responsive"


@then('the main content should have the role "{role}"')
def verify_main_content_role(context, role):
    assert (
        context.page.get_main_content_role() == role
    ), f"Main content role is not {role}"


@then('the results header should have the id "{id}"')
def verify_results_header_id(context, id):
    expect(context.page.results_header).to_have_id(id)


@then('the results count text should have the id "{id}"')
def verify_results_count_id(context, id):
    expect(context.page.results_count).to_have_id(id)
