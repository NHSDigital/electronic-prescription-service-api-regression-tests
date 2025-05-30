# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.search_results_too_many import SearchResultsTooManyMessage


@then("I am on the too many results page")
def i_am_on_too_many_results_page(context):
    page = SearchResultsTooManyMessage(context.page)
    expect(page.results_page).to_be_visible()


@then("the details section shows")
def verify_patient_details(context):
    page = SearchResultsTooManyMessage(context.page)
    details = {
        "First name": "First name: ",
        "Last name": "Last name: ",
        "DOB": "Date of birth: ",
        "Postcode": "Postcode: ",
    }
    for row in context.table:
        label = row["Heading"]
        expected_value = row["Value"]
        assert label in details, f"Unknown detail heading: {label}"
        expect(page.results_details_list).to_contain_text(
            f"{details[label]}{expected_value}"
        )
