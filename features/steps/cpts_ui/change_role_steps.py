# pylint: disable=no-name-in-module
import re
from time import sleep
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.change_role import ChangeRole


selected_role_url_pattern = re.compile(r".*/yourselectedrole(?:/|\.html)?$")
change_role_url_pattern = re.compile(r".*/changerole(?:/|\.html)?$")


############################################################################
# GIVEN STEPS
############################################################################


@given("I am on the change your role page")
def given_i_am_on_the_change_role_page(context):
    context.execute_steps("when I go to change my role")
    context.execute_steps("then I am on the change role page")


@given("the summary table body is displayed")
def given_the_summary_table_body_is_displayed(context):
    change_role_page = ChangeRole(context.page)

    # Expand the summary if it's not visible yet
    if not change_role_page.roles_without_access_table_body.is_visible():
        change_role_page.roles_without_access_table.click()
    expect(change_role_page.roles_without_access_table_body).to_be_visible()


@given("I am on the 'your selected role' page")
def given_i_am_on_your_selected_role_page(context):
    change_role_page = ChangeRole(context.page)
    context.execute_steps("given I am on the change your role page")
    context.execute_steps("when I click a role card")
    expect(change_role_page.select_role_header).to_be_visible()


############################################################################
# WHEN STEPS
############################################################################


@when("I click on the change role summary expander")
def when_i_click_on_the_summary_expander(context):
    change_role_page = ChangeRole(context.page)
    change_role_page.roles_without_access_table.click()


@when("I click a change role role card")
def when_i_click_a_role_card(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.first_role_card).to_be_visible()
    change_role_page.first_role_card.click()

    # Wait for the page or route change
    context.page.wait_for_url(selected_role_url_pattern)


@when("I click the change role header link")
def when_i_click_change_role_header_link(context):
    change_role_page = ChangeRole(context.page)
    change_role_page.page.get_by_test_id("eps_header_changeRoleLink").click()


@when("I go to change my role")
def i_go_to_change_my_role(context):
    context.execute_steps("when I have a selected role")
    change_role_page = ChangeRole(context.page)

    # We need to give the backend time to catch up?
    sleep(1)
    change_role_page.change_role_header.click()
    change_role_page.page.wait_for_url(change_role_url_pattern)


############################################################################
# THEN STEPS
############################################################################


@then("I am on the change role page")
def i_am_on_the_change_role_page(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.change_role_title).to_be_visible(timeout=60000)


@then("I see the change role roles without access table")
def then_i_see_the_roles_without_access_table(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.roles_without_access_table).to_be_visible()

    # Check header row
    expect(
        change_role_page.roles_without_access_organisation_column_header
    ).to_be_visible()
    expect(change_role_page.roles_without_access_role_column_header).to_be_visible()

    # Check data
    expect(change_role_page.first_row_org_name).to_be_visible()
    expect(change_role_page.first_row_role_name).to_be_visible()


@then("the change role roles without access table body is not visible")
def then_roles_without_access_table_body_is_not_visible(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.roles_without_access_table_body).not_to_be_visible()


@then("I see the change role roles with access cards")
def then_i_see_the_roles_with_access_cards(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.first_role_card).to_be_visible()


@then("I can see multiple change role roles with access cards")
def then_i_see_multiple_change_role_roles_with_access_cards(context):
    change_role_page = ChangeRole(context.page)
    assert change_role_page.roles_with_access_cards.count() > 1


@then("I can see one change role roles with access cards")
def then_i_see_one_change_role_roles_with_access_cards(context):
    change_role_page = ChangeRole(context.page)
    assert change_role_page.roles_with_access_cards.count() == 1


@then("I cannot see any change role roles with access cards")
def then_i_cant_see_roles_with_access_cards(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.first_role_card).not_to_be_visible()


@then("I am on the 'your selected role' page")
def then_i_am_on_your_selected_role_page(context):
    context.page.wait_for_url(selected_role_url_pattern)


@then("I do not see the change role page header link")
def then_i_can_not_see_the_change_your_role_page_header_link(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.change_role_header).not_to_be_visible()


@then("I see the change role page 'no role with access' warning message")
def i_see_the_change_role_page_no_role_with_access_warning_message(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.no_access_title).to_be_visible()
    expect(change_role_page.no_access_content).to_be_visible()
