from playwright.sync_api import Page


class SearchResultsTooManyMessage:
    def __init__(self, page: Page):
        self.page = page
        self.page.wait_for_load_state()

        self.results_page = page.get_by_test_id("too-many-results-container")
        self.results_message = page.get_by_test_id("too-many-results-message")
        self.results_count_text = page.get_by_test_id("too-many-results-count-text")
        self.results_alt_options = page.get_by_test_id("too-many-results-alt-options")
