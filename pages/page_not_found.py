from playwright.sync_api import Page


class PageNotFound:
    def __init__(self, page: Page):
        self.page = page

        self.header_text = page.get_by_test_id("eps-404-header")
        self.body1 = page.get_by_test_id("eps-404-body1")
        self.body2 = page.get_by_test_id("eps-404-body2")
        self.body3 = page.get_by_test_id("eps-404-body3")
