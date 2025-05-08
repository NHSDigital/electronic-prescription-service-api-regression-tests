# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.header import Header


@when('I click the "Select Your Role" link')
def step_impl(context):
    header = Header(context.page)
    header.select_role_link.click()


@then('I see the "Exit" link')
def i_see_exit_link(context):
    header = Header(context.page)
    expect(header.exit_link).to_be_visible()


@then('I do not see the "Exit" link')
def dont_see_exit_link(context):
    header = Header(context.page)
    expect(header.exit_link).not_to_be_visible()


@then('I see the "Logout" link')
def i_see_logout_link(context):
    header = Header(context.page)
    expect(header.logout_link).to_be_visible()


@then('I do not see the "Logout" link')
def dont_see_logout_link(context):
    header = Header(context.page)
    expect(header.logout_link).not_to_be_visible()


@then('I see the "Select Your Role" link')
def i_see_select_role_link(context):
    header = Header(context.page)
    expect(header.select_role_link).to_be_visible()


@then('I do not see the "Select Your Role" link')
def dont_see_select_role_link(context):
    header = Header(context.page)
    expect(header.select_role_link).not_to_be_visible()


@then('I see the "Change Role" link')
def i_see_change_role_link(context):
    header = Header(context.page)
    expect(header.change_role_link).to_be_visible()


@then('I do not see the "Change Role" link')
def dont_see_change_role_link(context):
    header = Header(context.page)
    expect(header.change_role_link).not_to_be_visible()


@then('I see the "Give feedback" link')
def i_see_feedback_link(context):
    header = Header(context.page)
    expect(header.feedback_link).to_be_visible()
    expect(header.feedback_link).to_have_text("Give feedback (opens in new tab)")


@then('the "Give feedback" link opens the feedback form in a new tab')
def feedback_link_opens_in_new_tab(context):
    header = Header(context.page)
    header.assert_feedback_link_is_external_and_opens_in_new_tab()
