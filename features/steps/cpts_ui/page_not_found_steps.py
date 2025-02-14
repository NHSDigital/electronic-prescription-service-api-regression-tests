# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.page_not_found import PageNotFound


@when("I navigate to a non-existent page")
def i_navigate_to_a_nonexistent_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/spamandeggs")


@then("I am on the Page Not Found page")
def i_am_on_page_not_found(context):
    page = PageNotFound(context.page)

    expect(page.header_text).to_be_visible()
    expect(page.body1).to_be_visible()
    expect(page.body2).to_be_visible()
    expect(page.body3).to_be_visible()
