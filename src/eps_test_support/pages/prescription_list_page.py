from playwright.sync_api import Page


class PrescriptionListPage:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.url = "/prescription-list"

        # FIXME: DELETEME
        self.dev_link = page.get_by_test_id("prescription-details-link-container")

        # Locators for elements on the page with updated data-testid attributes
        self.heading = page.get_by_test_id("prescription-list-heading")
        self.results_count = page.get_by_test_id("results-count")
        self.back_link = page.get_by_test_id("go-back-link")
        self.prescription_results_list = page.get_by_test_id("prescription-results-list")

        self.page_container = page.get_by_test_id("prescription-list-page")
        self.breadcrumb = page.get_by_test_id("prescription-list-breadcrumb")
        self.results_heading = page.get_by_test_id("results-heading")
        self.results_container = page.get_by_test_id("prescription-results-container")

        self.current_prescriptions_results_tab_heading = page.locator(
            '[data-testid^="eps-tab-heading /prescription-list-current"]'
        )
        self.past_prescriptions_results_tab_heading = page.locator(
            '[data-testid^="eps-tab-heading /prescription-list-past"]'
        )
        self.future_prescriptions_results_tab_heading = page.locator(
            '[data-testid^="eps-tab-heading /prescription-list-future"]'
        )

        self.current_prescriptions_results_tab_table = page.get_by_test_id(
            "prescription-results-list-tab-table current"
        )
        self.past_prescriptions_results_tab_table = page.get_by_test_id("prescription-results-list-tab-table past")
        self.future_prescriptions_results_tab_table = page.get_by_test_id("prescription-results-list-tab-table future")
