from playwright.sync_api import Page


class UnknownErrorMessagePage:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page

        self.heading = page.get_by_test_id("unknown-error-heading")
        self.body_text = page.get_by_test_id("error-intro")
        self.back_link = page.get_by_test_id("go-back-link")
