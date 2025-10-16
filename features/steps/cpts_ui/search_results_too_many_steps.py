# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.search_results_too_many import SearchResultsTooManyMessage


@when("I am on the too many results page")
@then("I am on the too many results page")
def i_am_on_too_many_results_page(context):
    page = SearchResultsTooManyMessage(context.active_page)
    expect(page.results_page).to_be_visible()


@then("the too many results page should display all required messages")
def verify_too_many_results_messages(context):
    page = SearchResultsTooManyMessage(context.active_page)
    expect(page.results_message).to_be_visible()
    expect(page.results_count_text).to_be_visible()
    expect(page.results_alt_options).to_be_visible()
