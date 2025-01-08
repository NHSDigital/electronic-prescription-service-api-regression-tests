# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.select_your_role import SelectYourRole
from features.environment import MOCK_CIS2_LOGIN_ID_1


@given("I am logged in")
def login(context):
    context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_1)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url("**/selectyourrole.html")


@then("I am on the select your role page")
def i_am_on_the_select_your_role_page(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.summary).to_be_visible()


@then("I can see the summary container")
def i_can_see_the_summary_container(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.summary).to_be_visible()


@then("I cannot see the summary table body")
def i_cannot_see_the_summary_table_body(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.roles_without_access_table_body).to_be_visible(
        visible=False
    )


@then("I can see the summary table body")
def i_can_see_the_summary_table_body(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.roles_without_access_table_body).to_be_visible()


@then("I can see the table body has a header row")
def i_can_see_the_table_body_header(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.organisation_column_header).to_be_visible()
    expect(select_your_role_page.role_column_header).to_be_visible()


@then("I can see the table body has data")
def i_can_see_the_table_body_data(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.first_row_org_name).to_be_visible()
    expect(select_your_role_page.first_row_role_name).to_be_visible()


@when("I click on the summary expander")
def click_on_summary_expander(context):
    select_your_role_page = SelectYourRole(context.page)
    select_your_role_page.summary.click()


@then("I can see the roles with access cards")
def i_can_see_the_roles_with_access_cards(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.first_role_card).to_be_visible()


@then("I can navigate to the your selected role page by clicking a card")
def i_can_navigate_to_the_your_selected_role_page(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.first_role_card).to_be_visible()
    select_your_role_page.first_role_card.click()
    context.page.wait_for_url(select_your_role_page.selected_role_url)


@then("I can see the your selected role header")
def i_can_see_select_your_role_header(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.select_role_header).to_be_visible()


@then("I can see the your selected role subheader")
def i_can_see_select_your_role_subheader(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.select_role_subheader).to_be_visible()
