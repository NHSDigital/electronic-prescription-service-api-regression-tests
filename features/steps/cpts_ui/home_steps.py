# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.header import Header
from pages.footer import Footer


@when("I go to the {page} page")
def goto_page(context, page):
    target = ""

    if page == "home":
        target = ""
    elif page == "search for a prescription":
        target = "search"
    elif page == "select your role":
        target = "select-role"

    url = f"{context.cpts_ui_base_url}site/{target}"
    context.page.goto(url)


@given("I am on the homepage")
def i_am_on_the_home_page(context):
    goto_page(context, "home")
    header = Header(context.page)
    header.page.is_visible(header.header)


@then("I am on the homepage")
def verify_on_home_page(context):
    header = Header(context.page)
    header.page.is_visible(header.header)


@then("I can see the footer")
def i_can_see_the_footer(context):
    footer = Footer(context.page)
    footer.page.is_visible(footer.footer)


@then("I can see the header")
def i_can_see_the_header(context):
    header = Header(context.page)
    header.page.is_visible(header.header)


@then("I can see the links on the header")
def i_can_see_the_links_on_the_header(context):
    header = Header(context.page)
    expect(header.change_role_link).to_be_visible()
    expect(header.logout_link).to_be_visible()


@when("I have a screen size of {pixel_width} pixels wide")
def i_have_a_screen_size_of_x_pixels_wide(context, pixel_width):
    context.page.set_viewport_size({"width": int(pixel_width), "height": 1200})


@then("I can see the header links in a dropdown menu")
def i_can_see_the_header_links_in_a_dropdown_menu(context):
    header = Header(context.page)
    expect(header.menu_button).to_be_visible()
    header.menu_button.click()
    expect(header.change_role_link).to_be_visible()
    expect(header.logout_link).to_be_visible()
    header.menu_button.click()
    expect(header.change_role_link).to_be_visible(visible=False)
    expect(header.logout_link).to_be_visible(visible=False)
