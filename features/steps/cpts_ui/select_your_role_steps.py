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
    context.page.goto(context.cpts_ui_base_url + "site/login")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill("555073103100")
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url("**/login.html")


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
    try:
        expect(select_your_role_page.first_role_card).to_be_visible(timeout=5000)
        print("Verified that at least one role card is displayed.")
    except Exception as e:
        print("Error verifying roles with access cards:", str(e))
        print("Page content during error:")
        print(context.page.content())
        raise


@then("I can navigate to the your_selected_role page by clicking a card")
def i_can_navigate_to_the_your_selected_role_page(context):
    select_your_role_page = SelectYourRole(context.page)
    try:
        expect(select_your_role_page.first_role_card).to_be_visible(timeout=5000)
        select_your_role_page.first_role_card.click()
        context.page.wait_for_url(select_your_role_page.selected_role_url)
        print(
            "Navigation to your_selected_role page successful. Current URL:",
            context.page.url,
        )
    except Exception as e:
        print("Error navigating to your_selected_role page:", str(e))
        print("Page content during error:")
        print(context.page.content())
        raise
