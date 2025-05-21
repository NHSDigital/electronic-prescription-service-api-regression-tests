from playwright.sync_api import Page


class SearchResultsTooManyPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.wait_for_load_state()

        self.results_page = page.get_by_test_id("too-many-results-page")
        self.results_details_list = page.get_by_test_id("too-many-results-details-list")
