# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from eps_test_support.pages.prescription_not_found import PrescriptionNotFound


@then("I am on the prescription not found page with redirect to {}")
def i_am_on_prescription_not_found_page(context, tab_name):
    page = PrescriptionNotFound(context.active_page)

    expect(page.heading).to_be_visible()
    expect(page.query_summary).to_be_visible()
    expect(page.back_link).to_be_visible()

    # Map tab_name to the corresponding URL
    url_map = {
        "PrescriptionIdSearch": "/site/search-by-prescription-id",
        "NhsNumberSearch": "/site/search-by-nhs-number",
        "BasicDetailsSearch": "/site/search-by-basic-details",
    }

    # Get the appropriate URL based on tab_name or default to prescription-id search
    url_target = url_map.get(tab_name, "/site/search-by-prescription-id")

    expect(page.back_link).to_have_attribute("href", url_target)


@when("I click the Go Back link on the prescription not found page")
def i_click_go_back_presc_not_found(context):
    page = PrescriptionNotFound(context.active_page)

    page.back_link.click()


@then("I should see the prescription not found message")
def i_should_see_prescription_not_found_message(context):
    page = PrescriptionNotFound(context.active_page)
    expect(page.heading).to_be_visible()
    expect(page.query_summary).to_be_visible()
    expect(page.back_link).to_be_visible()
