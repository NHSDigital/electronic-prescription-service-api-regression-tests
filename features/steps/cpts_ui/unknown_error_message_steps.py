# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.unknown_error_message import UnknownErrorMessagePage


@then("I see the unknown error message page")
def unknown_error_message_displayed(context):
    page = UnknownErrorMessagePage(context.page)
    expect(page.heading).to_have_text("Sorry, there is a problem with this service")
    expect(page.body_text).to_have_text("Try again later.")


@then("I see the go back link with a valid search route")
def check_go_back_link(context):
    page = UnknownErrorMessagePage(context.page)
    href = page.back_link.get_attribute("href")
    assert href is not None and any(
        path in href
        for path in [
            "/site/search-by-prescription-id",
            "/site/search-by-nhs-number",
            "/site/search-by-basic-details",
            "/site/prescription-list-current",
        ]
    ), f"Unexpected go-back link href: {href}"
