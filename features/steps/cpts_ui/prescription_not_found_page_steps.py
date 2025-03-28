# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_not_found import PrescriptionNotFound


@then("I am on the prescription not found page with redirect to {}")
def i_am_on_prescription_not_found_page(context, tab_name):
    page = PrescriptionNotFound(context.page)

    expect(page.header).to_be_visible()
    expect(page.body1).to_be_visible()
    expect(page.back_link).to_be_visible()

    url_target = "/site/search"
    if tab_name:
        url_target += f"#{tab_name}"

    expect(page.back_link).to_have_attribute("href", url_target)


@when("I click the Go Back link on the prescription not found page")
def i_click_go_back_presc_not_found(context):
    page = PrescriptionNotFound(context.page)

    page.back_link.click()
