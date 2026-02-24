from playwright.sync_api import Page


class SessionTimeoutModal:

    def __init__(self, page: Page):
        self.page = page

        # Modal container and elements - matching your React component exactly
        self.modal_container = page.get_by_test_id("session-timeout-modal")
        self.modal_title = page.locator("h2#session-timeout-title")
        self.stay_logged_in_button = page.get_by_test_id("stay-logged-in-button")
        self.logout_button = page.get_by_test_id("logout-button")
        self.countdown_time = page.locator("strong[aria-live='polite']")

        # Alternative selectors in case the main ones don't work
        self.eps_modal_wrapper = page.locator(
            '[data-testid="session-timeout-modal"]'
        ).locator("..")
        self.modal_content_by_text = page.locator("text=For your security")
