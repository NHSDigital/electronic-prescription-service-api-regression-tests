# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.select_your_role import SelectYourRole


@when("I go to the SLR page")
def i_go_to_the_slr_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/selectyourrole.html")


@given("I am on the SLR page")
def i_am_on_slr_page(context):
    i_go_to_the_slr_page(context)
    slr_page = SelectYourRole(context.page)
    expect(slr_page.summary).to_be_visible()


@then("I am on the SLR page")
def verify_on_slr_page(context):
    slr_page = SelectYourRole(context.page)
    expect(slr_page.summary).to_be_visible()


@given("I am logged in")
def login(context):
    context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill("555073103100")
    context.page.get_by_role("button", name="Sign In").click()


@then("I can see the summary container")
def i_can_see_the_summary_container(context):
    slr_page = SelectYourRole(context.page)
    expect(slr_page.summary).to_be_visible()


@then("I cannot see the summary table body")
def i_cannot_see_the_summary_table_body(context):
    slr_page = SelectYourRole(context.page)
    expect(slr_page.roles_without_access_table_body).to_be_visible(visible=False)


@then("I can see the summary table body")
def i_can_see_the_summary_table_body(context):
    slr_page = SelectYourRole(context.page)
    expect(slr_page.roles_without_access_table_body).to_be_visible()


@then("I can see the table body has a header row")
def i_can_see_the_table_body_header(context):
    slr_page = SelectYourRole(context.page)
    expect(slr_page.organisation_column_header).to_be_visible()
    expect(slr_page.role_column_header).to_be_visible()


@then("I can see the table body has data")
def i_can_see_the_table_body_data(context):
    slr_page = SelectYourRole(context.page)
    expect(slr_page.first_row_org_name).to_be_visible()
    expect(slr_page.first_row_role_name).to_be_visible()


@when("I click on the summary expander")
def click_on_summary_expander(context):
    slr_page = SelectYourRole(context.page)
    slr_page.summary.click()
