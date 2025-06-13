# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect
from cpts_ui.privacy_notice_text import (
    PRIVACY_NOTICE_TEXT,
)  # pylint: disable=import-error


def before_all(context):
    context.base_url = "/site/"


@then("I am on the privacy notice page")
def i_am_on_the_cookies_page(context):
    expected_path = "/site/privacy-notice"
    current_url = context.page.url
    assert (
        expected_path in current_url
    ), f"Expected '{expected_path}' to be in '{current_url}'"


@then("I can read the full privacy notice")
def i_read_privacy_notice(context):
    text = context.page.get_by_test_id("privacy-notice-content")
    expect(text).to_contain_text(PRIVACY_NOTICE_TEXT)
