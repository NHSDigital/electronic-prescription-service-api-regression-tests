# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from pages.select_your_role import SelectYourRole


@given("I am on the homepage")
def step_open_homepage(context):
    context.page.goto(context.cpts_ui_base_url + "site/")


@when("I click on the Select Your Role link")
def step_click_select_your_role_link(context):
    homepage = SelectYourRole(context.page)
    homepage.select_your_role_link.click()


@then('I can see the "Select your role - Select the" header')
def step_verify_header(context):
    page_content = SelectYourRole(context.page)
    expect(page_content.main_header).to_be_visible()


@then('I can see the "- Select the role you wish to use to access the service." text')
def step_verify_secondary_text(context):
    page_content = SelectYourRole(context.page)
    expect(page_content.secondary_text).to_have_text(
        "- Select the role you wish to use to access the service."
    )


@given("I am a user with roles assigned to my account")
def step_log_in_with_role(context):
    context.page.goto("http://localhost:3000/site/login")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").click()
    context.page.get_by_label("Username").fill("555073103100")
    context.page.get_by_role("button", name="Sign In").click()


@then(
    'I can see the message saying "You are currently logged in at {pharmacy} with {role} access."'
)
def step_verify_logged_in_message(context, pharmacy, role):
    expect(context.page.get_by_text("You are currently logged in")).to_have_text(
        f"You are currently logged in at {pharmacy} with {role} access.", exact=False
    )
