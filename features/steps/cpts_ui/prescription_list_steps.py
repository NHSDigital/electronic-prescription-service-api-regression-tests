from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
import re

from pages.prescription_list_page import PrescriptionListPage
from pages.search_for_a_prescription import SearchForAPrescription


@when("I search for the prescription by prescription ID")
def search_context_prescription_id(context):
    prescription_id = context.prescription_id
    context.execute_steps(
        f"""
        When I search for a prescription using a valid prescription ID "{prescription_id}"
        """
    )


@when('I search for a prescription using a valid prescription ID "{prescription_id}"')
def search_using_prescription_id(context, prescription_id):
    # Fill the input before clicking
    search_input = context.page.get_by_test_id("prescription-id-input")
    search_input.fill(prescription_id)

    context.page.get_by_test_id("find-prescription-button").click()


@when("I click on the NHS number search tab")
def click_on_nhs_number_search_tab(context):
    context.page.get_by_test_id("eps-tab-heading /search-by-nhs-number").click()


@when("I search for the prescription by NHS number search")
def search_context_nhs_number(context):
    nhs_number = context.nhs_number
    context.execute_steps(
        f"""
        When I search for a prescription using a valid NHS number "{nhs_number}"
        """
    )


@when('I search for a prescription using a valid NHS number "{nhs_number}"')
def search_using_nhs_number(context, nhs_number):
    # Fill the input before clicking
    search_input = context.page.get_by_test_id("nhs-number-input")
    search_input.fill(nhs_number)

    context.page.get_by_test_id("find-patient-button").click()


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
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )

    prescription_list_page = PrescriptionListPage(context.page)

    expect(
        prescription_list_page.page.locator(
            '[data-testid="current-prescriptions-results-table"]'
        )
    ).to_be_visible()
    expect(
        prescription_list_page.page.locator(
            '[data-testid="past-prescriptions-results-table"]'
        )
    ).not_to_be_visible()
    expect(
        prescription_list_page.page.locator(
            '[data-testid="future-prescriptions-results-table"]'
        )
    ).not_to_be_visible()


@then("I see the table summary text Showing {count} of {count}")
def i_see_the_showing_count_text(context, count):
    summary_row = context.page.get_by_test_id("table-summary-row")
    expected_text = f"Showing {count} of {count}"
    expect(summary_row).to_be_visible()
    expect(summary_row).to_have_text(expected_text)


@then("the table displays {count} prescription rows")
def table_displays_prescription_rows(context, count):
    prescription_list_page = PrescriptionListPage(context.page)
    expect(
        prescription_list_page.current_prescriptions_results_tab_table
    ).to_be_visible()
    rows = prescription_list_page.current_prescriptions_results_tab_table.locator(
        "tbody tr:not(:last-child)"
    )

    expect(rows).to_have_count(int(count))


@then("I can see the future prescriptions results table")
# STEP HERE TO CHECK IF THERE ARE FUTURE DATED PRESCRIPTIONS AND/OR NEED TO CHECK FOR THE MESSAGE IF THERES NONE
def i_see_future_prescriptions_results_tab(context):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )
    prescription_list_page = PrescriptionListPage(context.page)
    print("PAGE CONTENT:", context.page.content())

    expect(
        prescription_list_page.page.locator(
            '[data-testid="future-prescriptions-results-table"]'
        )
    ).to_be_visible()
    expect(
        prescription_list_page.page.locator(
            '[data-testid="current-prescriptions-results-table"]'
        )
    ).not_to_be_visible()
    expect(
        prescription_list_page.page.locator(
            '[data-testid="past-prescriptions-results-table"]'
        )
    ).not_to_be_visible()


@then("I can see the past prescriptions results table")
def i_see_past_prescriptions_results_tab(context):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )

    prescription_list_page = PrescriptionListPage(context.page)

    expect(
        prescription_list_page.page.locator(
            '[data-testid="past-prescriptions-results-table"]'
        )
    ).to_be_visible()
    expect(
        prescription_list_page.page.locator(
            '[data-testid="future-prescriptions-results-table"]'
        )
    ).not_to_be_visible()
    expect(
        prescription_list_page.page.locator(
            '[data-testid="current-prescriptions-results-table"]'
        )
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
    print(f"Current URL after save: {current_url}")
    context.page.screenshot(path="summary_row_failure.png")

    assert (
        "site/search-by-nhs-number" in current_url
    ), f"Expected URL to contain 'site/search-by-nhs-number', got: {current_url}"

    # Use the POM to verify we're on the NHS number search tab
    search_page = SearchForAPrescription(context.page)
    expect(search_page.nhs_number_search_header).to_be_visible()


@when('I sort the table by "{column_name}"')
def sort_table_by_column(context, column_name):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )

    column_mapping = {
        "Issue date": "eps-prescription-table-sort-issueDate",
        "Prescription type": "eps-prescription-table-sort-prescriptionTreatmentType",
        "Status": "eps-prescription-table-sort-statusCode",
        "Pending cancellation": "eps-prescription-table-sort-cancellationWarning",
        "Prescription ID": "eps-prescription-table-sort-prescriptionId",
    }

    column_key = column_mapping.get(column_name)
    assert column_key, f"Column name '{column_name}' not found in mapping"

    # issue date starts descending as standard, the others are ascending
    initial_directions = {
        "Issue date": "descending",
        "Prescription type": "none",
        "Status": "none",
        "Pending cancellation": "none",
        "Prescription ID": "none",
    }

    scenario_name = context.scenario.name
    target_direction = "descending" if "descending" in scenario_name else "ascending"
    initial_direction = initial_directions.get(column_name, "none")

    header_locator = context.page.locator(f'[data-testid="{column_key}"]')
    header_locator.wait_for(state="visible", timeout=5000)

    if initial_direction == "descending" and target_direction == "ascending":
        header_locator.click()
    elif initial_direction == "descending" and target_direction == "descending":
        pass
    elif initial_direction == "none" and target_direction == "ascending":
        header_locator.click()
    elif initial_direction == "none" and target_direction == "descending":
        header_locator.click()
        context.page.wait_for_timeout(500)
        header_locator.click()


@then('the table is sorted by "{column_name}" in "{direction}" order')
def check_table_sort_order(context, column_name, direction):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )
    column_mapping = {
        "Issue date": "issueDate",
        "Prescription type": "prescriptionTreatmentType",
        "Status": "statusCode",
        "Pending cancellation": "cancellationWarning",
        "Prescription ID": "prescriptionId",
    }
    column_key = column_mapping.get(column_name)
    assert column_key, f"Column name '{column_name}' not found in mapping"

    header_locator = context.page.locator(
        f'[data-testid="eps-prescription-table-header-{column_key}"]'
    )
    header_locator.wait_for(state="visible", timeout=5000)

    expected_aria_sort = direction.lower()
    actual_aria_sort = header_locator.get_attribute("aria-sort")
    assert (
        actual_aria_sort == expected_aria_sort
    ), f"Expected aria-sort to be '{expected_aria_sort}', but was '{actual_aria_sort}'"

    if direction.lower() == "ascending":
        up_arrow = header_locator.locator(".up-arrow")
        up_arrow_class = up_arrow.get_attribute("class") or ""
        assert (
            "selected-arrow" in up_arrow_class
        ), f"Up arrow is not selected for ascending sort. Arrow classes: {up_arrow_class}"

        down_arrow = header_locator.locator(".down-arrow")
        down_arrow_class = down_arrow.get_attribute("class") or ""
        assert (
            "selected-arrow" not in down_arrow_class
        ), f"Down arrow should not be selected for ascending sort. Arrow classes: {down_arrow_class}"

    else:
        down_arrow = header_locator.locator(".down-arrow")
        down_arrow_class = down_arrow.get_attribute("class") or ""
        assert (
            "selected-arrow" in down_arrow_class
        ), f"Down arrow is not selected for descending sort. Arrow classes: {down_arrow_class}"

        up_arrow = header_locator.locator(".up-arrow")
        up_arrow_class = up_arrow.get_attribute("class") or ""
        assert (
            "selected-arrow" not in up_arrow_class
        ), f"Up arrow should not be selected for descending sort. Arrow classes: {up_arrow_class}"

    all_headers = context.page.locator(
        '[data-testid^="eps-prescription-table-header-"]'
    )
    header_count = all_headers.count()

    for i in range(header_count):
        header = all_headers.nth(i)
        header_testid = header.get_attribute("data-testid")

        if header_testid == f"eps-prescription-table-header-{column_key}":
            continue

        other_aria_sort = header.get_attribute("aria-sort")
        assert (
            other_aria_sort == "none"
        ), f"Header {header_testid} should have aria-sort='none', but has '{other_aria_sort}'"


@when("I click on the view prescription link")
def click_view_prescriptions_link(context):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=4000
    )
    prescription_id = context.prescription_id
    context.page.get_by_test_id(f"view-prescription-link-{prescription_id}").click()


@then("I am taken to the correct prescription page")
def check_url_redirect_for_prescriptions(context):
    expected_url_pattern = re.compile(
        r"/site/prescription-details\?prescriptionId=[\w-]+"
    )
    context.page.wait_for_url(expected_url_pattern)
