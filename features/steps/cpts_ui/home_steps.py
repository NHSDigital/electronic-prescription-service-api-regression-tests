# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.home import Home


@when("I am on the homepage")
def goto_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/")


@given("I am on the homepage")
def i_am_on_the_home_page(context):
    goto_page(context)
    home_page = Home(context.page)
    home_page.page.is_visible(home_page.header)


@then("I am on the homepage")
def verify_on_home_page(context):
    home_page = Home(context.page)
    home_page.page.is_visible(home_page.header)


@then("I can see the footer")
def i_can_see_the_footer(context):
    home_page = Home(context.page)
    home_page.page.is_visible(home_page.footer)


@then("I can see the header")
def i_can_see_the_header(context):
    home_page = Home(context.page)
    home_page.page.is_visible(home_page.header)


@then("I can see the links on the header")
def i_can_see_the_links_on_the_header(context):
    home_page = Home(context.page)
    expect(home_page.confirm_role_link).to_be_visible()
    expect(home_page.find_a_prescription_link).to_be_visible()


@when("I have a screen size of {pixel_width} pixels wide")
def i_have_a_screen_size_of_x_pixels_wide(context, pixel_width):
    context.page.set_viewport_size({"width": int(pixel_width), "height": 1200})


@then("I can see the header links in a dropdown menu")
def i_can_see_the_header_links_in_a_dropdown_menu(context):
    home_page = Home(context.page)
    expect(home_page.menu_button).to_be_visible()
    home_page.menu_button.click()
    expect(home_page.confirm_role_link).to_be_visible()
    expect(home_page.find_a_prescription_link).to_be_visible()
    home_page.menu_button.click()
    expect(home_page.confirm_role_link).to_be_visible(visible=False)
    expect(home_page.find_a_prescription_link).to_be_visible(visible=False)


@when("I click on Find a prescription")
def step_impl(context):
    home_page = Home(context.page)
    home_page.find_a_prescription_link.click()
