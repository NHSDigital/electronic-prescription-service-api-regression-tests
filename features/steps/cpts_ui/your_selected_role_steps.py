# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.your_selected_role import YourSelectedRole


############################################################################
# GIVEN STEPS
############################################################################


@given("I am on the your selected role page")
def i_am_on_the_confirm_your_role_page(context):
    context.execute_steps("when I have a selected role")
    context.execute_steps("then I see the 'your selected role' page")


############################################################################
# WHEN STEPS
############################################################################


@when("I click the change link next to the role text")
def i_click_the_change_link_next_to_the_role_text(context):
    your_selected_role_page = YourSelectedRole(context.page)
    your_selected_role_page.role_change_role.click()


@when("I click the change link next to the org text")
def i_click_the_change_link_next_to_the_org_text(context):
    your_selected_role_page = YourSelectedRole(context.page)
    your_selected_role_page.org_change_role.click()


@when("I click the confirm and continue button on the your selected role page")
def i_click_the_confirm_and_continue_button_on_the_your_selected_role_page(context):
    your_selected_role_page = YourSelectedRole(context.page)
    your_selected_role_page.confirm_button.click()


############################################################################
# THEN STEPS
############################################################################


@then("I see the 'your selected role' page")
def i_see_the_confirm_your_role_page(context):
    your_selected_role_page = YourSelectedRole(context.page)

    expect(your_selected_role_page.header).to_be_visible()
    expect(your_selected_role_page.role_label_cell).to_be_visible()
    expect(your_selected_role_page.org_label_cell).to_be_visible()
    expect(your_selected_role_page.org_text_cell).to_be_visible()
    expect(your_selected_role_page.role_text_cell).to_be_visible()
    expect(your_selected_role_page.role_change_role).to_be_visible()
    expect(your_selected_role_page.org_change_role).to_be_visible()
