from playwright.sync_api import Page


class SearchResultsTooManyPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.wait_for_load_state()

        self.details_list = page.get_by_test_id("too-many-results-details-list")
