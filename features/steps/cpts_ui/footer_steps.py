# pylint: disable=no-name-in-module
from behave import given, then, when  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.footer import Footer


@given("I can see the page footer")
def i_can_see_the_footer(context):
    footer = Footer(context.page)
    expect(footer.footer).to_be_visible()


@then('I can see the "{link_text}" link in the footer')
def i_see_footer_link(context, link_text):
    footer = Footer(context.page)
    name = link_text.strip().lower()
    try:
        expect(footer.link_map[name]).to_be_visible()
    except KeyError as exc:
        raise ValueError(f"Unknown footer link text: {link_text}") from exc


@then("I see the footer copyright section")
def i_see_footer_text(context):
    footer = Footer(context.page)
    expect(footer.copyright).to_be_visible()


@when('I click the "{link_name}" link in the footer')
def click_footer_link(context, link_name):
    footer = Footer(context.page)
    footer.click_link(link_name)


@then("the current page URL contains {expected}")
def page_url_contains(context, expected):
    current_url = context.page.url
    assert expected in current_url, f"Expected '{expected}' to be in URL: {current_url}"
