# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.select_your_role import SelectYourRole


@when("I go to the select_your_role page")
def i_go_to_the_select_your_role_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/selectyourrole.html")


@given("I am on the select_your_role page")
def i_am_on_select_your_role_page(context):
    i_go_to_the_select_your_role_page(context)
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.summary).to_be_visible()


@then("I am on the select_your_role page")
def verify_on_select_your_role_page(context):
    select_your_role_page = SelectYourRole(context.page)
    expect(select_your_role_page.summary).to_be_visible()


@given("I am logged in")
def login(context):
    context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill("555073103100")
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url("**/auth_demo.html")


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
