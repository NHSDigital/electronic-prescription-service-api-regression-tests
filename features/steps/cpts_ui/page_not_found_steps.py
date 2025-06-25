# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.page_not_found import PageNotFound


@when("I navigate to a non-existent page")
def i_navigate_to_a_nonexistent_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/spamandeggs")


@when("I navigate outside the react app route with a two-segment path")
def i_navigate_to_a_two_segment_non_app_page(context):
    context.page.goto(context.cpts_ui_base_url + "foo/spamandeggs")


@when("I navigate outside the react app route")
def i_navigate_to_a_non_app_page(context):
    context.page.goto(context.cpts_ui_base_url + "spamandeggs")


@then("I am on the logged out Page Not Found page")
def i_am_on_page_not_found_a(context):
    page = PageNotFound(context.page)

    expect(page.header_text).to_be_visible()
    expect(page.body1).to_be_visible()
    expect(page.body2).to_be_visible()


@then("I am on the logged in Page Not Found page")
def i_am_on_page_not_found_b(context):
    context.execute_steps("then I am on the logged out Page Not Found page")

    page = PageNotFound(context.page)
    expect(page.body3).to_be_visible()


@when("I navigate to the {page} app page outside of the site path")
def i_navigate_to_an_app_page_outside_of_site_path(context, page):
    target = ""
    if page == "search for a prescription":
        target = "search-by-prescription-id"
    elif page == "select your role":
        target = "select-your-role"

    context.page.goto(context.cpts_ui_base_url + target)
    context.page.wait_for_page_load()


@then("I am redirected to the site, with the URI of {page} correctly forwarded")
def i_am_redirected_to_site_with_uri_forwarded(context, page):
    expected_path = f"/site/{page}"

    current_url = context.page.url
    assert (
        expected_path in current_url
    ), f"Expected '{expected_path}' to be in '{current_url}'"
