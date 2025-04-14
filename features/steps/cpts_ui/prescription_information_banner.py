# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_information_banner import PrescriptionInformationBanner


@when('I go to the prescription details page with prescription ID "{prescription_id}"')
def go_to_details_page(context, prescription_id):
    context.page.goto(
        f"{context.cpts_ui_base_url}site/prescription-details?prescriptionId={prescription_id}"
    )


@when("I go to the prescription details page without a prescription ID")
def go_to_details_page_no_id(context):
    context.page.goto(f"{context.cpts_ui_base_url}site/prescription-details")


@then("The prescription information banner is not visible")
def banner_not_visible(context):
    banner = PrescriptionInformationBanner(context.page)
    expect(banner.banner).not_to_be_visible()


@then("The prescription information banner shows")
def banner_shows_data(context):
    banner = PrescriptionInformationBanner(context.page)
    expect(banner.banner).to_be_visible()
    for row in context.table:
        field, value = row.cells
        if field == "Prescription ID":
            expect(banner.prescription_id).to_contain_text(value)
        elif field == "Issue Date":
            expect(banner.issue_date).to_contain_text(value)
        elif field == "Status":
            expect(banner.status).to_contain_text(value)
        elif field == "Type":
            expect(banner.prescription_type).to_contain_text(value)
        elif field == "Repeat":
            expect(banner.repeat).to_contain_text(value)
        elif field == "Days Supply":
            expect(banner.days_supply).to_contain_text(value)


@when("I click the copy prescription ID button")
def click_copy_button(context):
    banner = PrescriptionInformationBanner(context.page)
    expect(banner.copy_button).to_be_visible(timeout=5000)
    banner.copy_button.click()


@then('The clipboard contains "{expected}"')
def clipboard_has_text(context, expected):
    copied = context.page.evaluate("() => window.__copiedText")
    assert (
        copied == expected
    ), f"Expected '{expected}' in mock clipboard, got '{copied}'"


@then('The page shows the loading message "{expected_message}"')
def check_loading_message(context, expected_message):
    heading = context.page.get_by_test_id("loading-message")
    expect(heading).to_have_text(expected_message)
