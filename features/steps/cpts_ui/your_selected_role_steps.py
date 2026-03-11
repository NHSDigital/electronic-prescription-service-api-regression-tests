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


@given("I have confirmed a role")
def i_have_confirmed_a_role(context):
    context.execute_steps("given I have selected a role")
    context.execute_steps("when I click the confirm and continue button on the your selected role page")


############################################################################
# WHEN STEPS'
############################################################################
@given("I click the confirm and continue button on the your selected role page")
@when("I click the confirm and continue button on the your selected role page")
def i_click_the_confirm_and_continue_button_on_the_your_selected_role_page(context):
    your_selected_role_page = YourSelectedRole(context.active_page)
    your_selected_role_page.confirm_button.click()
    context.active_page.wait_for_load_state()


@when("I click the change link next to the role text")
def i_click_the_change_link_next_to_the_role_text(context):
    your_selected_role_page = YourSelectedRole(context.active_page)
    your_selected_role_page.role_change_role.click()


@when("I click the change link next to the org text")
def i_click_the_change_link_next_to_the_org_text(context):
    your_selected_role_page = YourSelectedRole(context.active_page)
    org_change_link = your_selected_role_page.page.get_by_test_id("org-change-role-cell").locator("a")
    org_change_link.click()


############################################################################
# THEN STEPS
############################################################################


@then("I see the 'your selected role' page")
def i_see_the_confirm_your_role_page(context):
    your_selected_role_page = YourSelectedRole(context.active_page)
    org_change_role_link = your_selected_role_page.page.get_by_test_id("org-change-role-cell").locator("a")

    expect(your_selected_role_page.header).to_be_visible()
    expect(your_selected_role_page.role_label_cell).to_be_visible()
    expect(your_selected_role_page.org_label_cell).to_be_visible()
    expect(your_selected_role_page.org_text_cell).to_be_visible()
    expect(your_selected_role_page.role_text_cell).to_be_visible()
    expect(your_selected_role_page.role_change_role).to_be_visible()
    expect(org_change_role_link).to_be_visible()
