from playwright.sync_api import Page


class YourSelectedRole:
    def __init__(self, page: Page):
        self.page = page

        self.page_loaded_indicator = page.get_by_test_id("eps_yourSelectedRole_page")
