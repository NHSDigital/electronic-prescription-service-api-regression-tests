# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from eps_test_support.pages.prescription_information_banner import (
    PrescriptionInformationBanner,
)


@when("I go to the prescription details page without a prescription ID")
def go_to_details_page_no_id(context):
    context.active_page.goto(f"{context.cpts_ui_base_url}site/prescription-details")


@then("The prescription information banner is not visible")
def banner_not_visible(context):
    banner = PrescriptionInformationBanner(context.active_page)
    expect(banner.banner).not_to_be_visible()


@then("The prescription information banner is visible")
def banner_is_visible(context):
    banner = PrescriptionInformationBanner(context.active_page)

    expect(banner.banner).to_be_visible()
    expect(banner.prescription_id).not_to_have_text("")
    expect(banner.issue_date).not_to_have_text("")
    expect(banner.status).not_to_have_text("")
    expect(banner.prescription_type).not_to_have_text("")


@then("The prescription information banner displays repeat and days supply data")
def banner_has_repeat_and_days_supply(context):
    banner = PrescriptionInformationBanner(context.active_page)
    expect(banner.banner).to_be_visible()
    expect(banner.prescription_type).to_contain_text("eRD")
    expect(banner.days_supply).not_to_have_text("")


@when("I click the copy prescription ID button")
def click_copy_button(context):
    banner = PrescriptionInformationBanner(context.active_page)
    expect(banner.copy_button).to_be_visible(timeout=5000)
    banner.copy_button.click()


@then('The clipboard contains "{expected}"')
def clipboard_has_text(context, expected):
    copied = context.active_page.evaluate("() => window.__copiedText")
    assert copied == expected, f"Expected '{expected}' in mock clipboard, got '{copied}'"


@then('The page shows the loading message "{expected_message}"')
def check_loading_message(context, expected_message):
    heading = context.active_page.get_by_test_id("loading-message")
    expect(heading).to_have_text(expected_message)
