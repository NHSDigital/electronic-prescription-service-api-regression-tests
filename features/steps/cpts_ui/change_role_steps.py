# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.change_role import ChangeRole


############################################################################
# GIVEN STEPS
############################################################################


@given("I am on the select your role page")
def given_i_am_on_the_change_role_page(context):
    context.execute_step("when I go to the change role page")
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.summary).to_be_visible()


@given("the summary table body is displayed")
def given_the_summary_table_body_is_displayed(context):
    change_role_page = ChangeRole(context.page)

    # Expand the summary if it's not visible yet
    if not change_role_page.roles_without_access_table_body.is_visible():
        change_role_page.summary.click()
    expect(change_role_page.roles_without_access_table_body).to_be_visible()


@given("I am on the 'your selected role' page")
def given_i_am_on_your_selected_role_page(context):
    change_role_page = ChangeRole(context.page)
    context.execute_step("given I am on the select your role page")
    context.execute_step("when I click a role card")
    expect(change_role_page.select_role_header).to_be_visible()


############################################################################
# WHEN STEPS
############################################################################


@when("I go to the change role page")
def when_i_go_to_the_change_role_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/changerole.html")


@when("I click on the summary expander")
def when_i_click_on_the_summary_expander(context):
    change_role_page = ChangeRole(context.page)
    change_role_page.summary.click()


@when("I click a role card")
def when_i_click_a_role_card(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.first_role_card).to_be_visible()
    change_role_page.first_role_card.click()
    # Wait for the page or route change
    context.page.wait_for_url(change_role_page.selected_role_url)


############################################################################
# THEN STEPS
############################################################################


@then("I see the summary container")
def then_i_see_the_summary_container(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.summary).to_be_visible()


@then("the summary table body is not visible")
def then_summary_table_body_is_not_visible(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.roles_without_access_table_body).to_be_visible(
        visible=False
    )


@then("I see the summary table body with a header row and data")
def then_i_see_the_summary_table_body_with_header_and_data(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.roles_without_access_table_body).to_be_visible()

    # Check header row
    expect(change_role_page.organisation_column_header).to_be_visible()
    expect(change_role_page.role_column_header).to_be_visible()

    # Check data
    expect(change_role_page.first_row_org_name).to_be_visible()
    expect(change_role_page.first_row_role_name).to_be_visible()


@then("I see the roles with access cards")
def then_i_see_the_roles_with_access_cards(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.first_role_card).to_be_visible()


@then("I cannot see any roles with access cards")
def then_i_cant_see_roles_with_access_cards(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.first_role_card).not_to_be_visible()


@then("I am on the 'your selected role' page")
def then_i_am_on_your_selected_role_page(context):
    change_role_page = ChangeRole(context.page)
    # You might also check the URL if that's relevant:
    # expect(context.page).to_have_url(change_role_page.selected_role_url)
    expect(change_role_page.select_role_header).to_be_visible()


@then("I see the 'your selected role' header")
def then_i_see_the_your_selected_role_header(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.select_role_header).to_be_visible()


@then("I see the 'your selected role' subheader")
def then_i_see_the_your_selected_role_subheader(context):
    change_role_page = ChangeRole(context.page)
    expect(change_role_page.select_role_subheader).to_be_visible()
