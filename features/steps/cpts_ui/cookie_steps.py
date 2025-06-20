# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore
from playwright.sync_api import expect


def before_all(context):
    context.base_url = "/site/"


@given("I am on the cookies page")
def i_am_on_the_cookies_page(context):
    context.page.goto(f"{context.cpts_ui_base_url}site/cookies")


@when("I press the {button_name} button")
def i_press_a_cookie_button(context, button_name):
    button_test_id = f"{button_name}-button"
    button = context.page.get_by_test_id(button_test_id)
    expect(button).to_be_visible()
    button.click()


@when("I click the cookies policy link")
def i_click_the_policy_link(context):
    link = context.page.get_by_test_id("cookieInfoLink")
    link.click()


@given("I see the smaller cookie banner")
@then("I see the smaller cookie banner")
def i_see_smaller_cookie_banner(context):
    small_banner = context.page.get_by_test_id("secondaryCookieBanner")
    expect(small_banner).to_contain_text(
        "You can change your cookie settings at any time using our"
    )


@when("I click the small banner cookie policy link")
def i_click_the_small_banner_policy_link(context):
    page_link = context.page.get_by_test_id("smallCookieBannerLink")
    page_link.click()


@when("I expand the {table_type} cookies details section")
def i_expand_the_cookies_info_table(context, table_type):
    cookies_dropdown_text = f"see-{table_type.lower()}-cookies"
    table_dropdown = context.page.get_by_test_id(cookies_dropdown_text)
    table_dropdown.click()


@when("I click {option} cookies and save")
def i_choose_cookie_option(context, option):
    if option == "use":
        radio_button = context.page.get_by_test_id("accept-analytics-cookies")
    else:
        radio_button = context.page.get_by_test_id("reject-analytics-cookies")
    expect(radio_button).to_be_visible()
    radio_button.click()

    save_button = context.page.get_by_test_id("save-cookie-preferences")
    expect(save_button).to_be_visible()
    save_button.click()


@then("I can see the cookie banner")
def i_can_see_cookie_banner(context):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )
    banner = context.page.get_by_test_id("cookieBanner")
    expect(banner).to_be_visible
    title = context.page.get_by_test_id("cookieTitle")
    expect(title).to_contain_text("Cookies on the Prescription Tracker")


@then("I go to the cookies policy page")
def i_got_to_cookies_policy_page(context):
    expected_path = "/cookies"
    current_url = context.page.url
    assert (
        expected_path in current_url
    ), f"Expected '{expected_path}' to be in '{current_url}'"


@then("I see the table for {table_type} cookies")
def i_see_the_relevant_table(context, table_type):
    table_test_id = f"{table_type.lower()}-cookies-table"
    table = context.page.get_by_test_id(table_test_id)
    expect(table).to_be_visible()


@then("I go to the cookies selected page")
def i_go_to_cookies_selected_page(context):
    expected_path = "/site/cookies-selected"
    current_url = context.page.url
    assert (
        expected_path in current_url
    ), f"Expected '{expected_path}' to be in '{current_url}'"


def get_rum_cookies(cookies):
    rum_cookies = [
        cookie for cookie in cookies if cookie.get("name") in ("cwr_s", "cwr_u")
    ]
    return rum_cookies


@then("I do not have RUM cookies")
def i_do_not_have_rum_cookies(context):
    cookies = context.page.context.cookies()
    rum_cookies = get_rum_cookies(cookies)
    assert len(rum_cookies) == 0


@then("I do have RUM cookies")
def i_do_have_rum_cookies(context):
    cookies = context.page.context.cookies()
    rum_cookies = get_rum_cookies(cookies)
    assert len(rum_cookies) == 2
