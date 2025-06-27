# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.page_not_found import PageNotFound
from pages.header import Header
from methods.shared.common import convert_to_uri


@when("I navigate to a non-existent page")
def i_navigate_to_a_nonexistent_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/spamandeggs")


@when("I navigate outside the react app route with an incorrect two-segment path")
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


@then("I am not redirected anywhere but I see the Page Not Found page")
def i_am_not_redirected_anywhere_but_see_page_not_found(context):
    expected_url = context.cpts_ui_base_url + "foo/spamandeggs"

    context.page.wait_for_url(
        expected_url,
        timeout=5000,
    )

    page = PageNotFound(context.page)

    expect(page.header_text).to_be_visible()
    expect(page.body1).to_be_visible()
    expect(page.body2).to_be_visible()
    expect(page.body3).not_to_be_visible()


@when("I navigate to the '{target}' app page outside of the site path")
def i_navigate_to_an_app_page_outside_of_site_path(context, target):
    uri = convert_to_uri(target)

    context.page.goto(context.cpts_ui_base_url + uri)
    header = Header(context.page)
    header.page.is_visible(header.header)


@then(
    "I am redirected correctly to the site, with URI of '{target}' correctly forwarded"
)
def i_am_redirected_to_site_with_uri_forwarded(context, target):
    uri = convert_to_uri(target)

    context.page.wait_for_url(
        f"{context.cpts_ui_base_url}site/{uri}",
        timeout=5000,
    )
