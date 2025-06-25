# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.unknown_error_message import UnknownErrorMessagePage


@then("I should see the unknown error message")
def i_should_see_unknown_error_message(context):
    page = UnknownErrorMessagePage(context.page)
    expect(page.heading).to_be_visible()
    expect(page.body_text).to_be_visible()
    expect(page.back_link).to_be_visible()
