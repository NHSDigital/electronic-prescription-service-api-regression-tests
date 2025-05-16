# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.search_results_too_many import SearchResultsTooManyPage


@then('the details section shows first name "{first}"')
def verify_first_name(context, first):
    page = SearchResultsTooManyPage(context.page)
    expect(page.details_list).to_contain_text(f"First name: {first}")


@then('the details section shows last name "{last}"')
def verify_last_name(context, last):
    page = SearchResultsTooManyPage(context.page)
    expect(page.details_list).to_contain_text(f"Last name: {last}")


@then('the details section shows date of birth "{dob}"')
def verify_dob(context, dob):
    page = SearchResultsTooManyPage(context.page)
    expect(page.details_list).to_contain_text(f"Date of birth: {dob}")


@then('the details section shows postcode "{postcode}"')
def verify_postcode(context, postcode):
    page = SearchResultsTooManyPage(context.page)
    expect(page.details_list).to_contain_text(f"Postcode: {postcode}")
