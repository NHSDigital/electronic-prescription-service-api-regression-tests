# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from pages.home_page import HomePage


@when("I go to the homepage")
def goto_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/")


@then("I am on the homepage")
def verify_on_page(context):
    home_page = HomePage(context.page)
    home_page.verify_header_link()
