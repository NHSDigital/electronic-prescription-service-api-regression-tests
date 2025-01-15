# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.header_links import HeaderLinks


@then('I see the "Exit" link')
def i_see_exit_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.exit_link).to_be_visible()


@then('I do not see the "Exit" link')
def dont_see_exit_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.exit_link).not_to_be_visible()


@then('I see the "Logout" link')
def i_see_logout_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.logout_link).to_be_visible()


@then('I do not see the "Logout" link')
def dont_see_logout_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.logout_link).not_to_be_visible()


@then('I see the "Select Your Role" link')
def i_see_select_role_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.select_role_link).to_be_visible()


@then('I do not see the "Select Your Role" link')
def dont_see_select_role_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.select_role_link).not_to_be_visible()


@then('I see the "Change Role" link')
def i_see_change_role_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.change_role_link).to_be_visible()


@then('I do not see the "Change Role" link')
def dont_see_change_role_link(context):
    header_links = HeaderLinks(context.page)
    expect(header_links.change_role_link).not_to_be_visible()
