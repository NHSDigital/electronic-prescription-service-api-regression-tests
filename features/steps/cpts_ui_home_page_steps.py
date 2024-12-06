# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from pages.home_page import HomePage


@when("I go to the homepage")
def goto_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/")


@given("I am on the homepage")
def verify_on_page(context):
    goto_page(context)
    home_page = HomePage(context.page)
    home_page.verify_header_link()


@then("I am on the homepage")
def verify_on_home_page(context):
    home_page = HomePage(context.page)
    home_page.verify_header_link()


@then("I can see the footer")
def i_can_see_the_footer(context):
    home_page = HomePage(context.page)
    home_page.verify_footer_is_visible()


@then("I can see the header")
def i_can_see_the_header(context):
    home_page = HomePage(context.page)
    home_page.verify_header_is_visible()


@then("I can see the links on the header")
def i_can_see_the_links_on_the_header(context):
    home_page = HomePage(context.page)
    home_page.verify_header_links_large_view()


@when("I have a screen size of {pixel_width} pixels wide")
def i_have_a_screen_size_of_x_pixels_wide(context, pixel_width):
    context.page.set_viewport_size({"width": int(pixel_width), "height": 1200})


@then("I can see the header links in a dropdown menu")
def i_can_see_the_header_links_in_a_dropdown_menu(context):
    home_page = HomePage(context.page)
    home_page.verify_header_links_short_width_view()
