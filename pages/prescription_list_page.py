from playwright.sync_api import Page


class PrescriptionListPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "/prescription-results"

        # Locators for elements on the page with updated data-testid attributes
        self.heading = page.locator("[data-testid='prescription-list-heading']")
        self.results_count = page.locator("[data-testid='results-count']")
        self.back_link = page.locator("[data-testid='go-back-link']")
        self.prescription_results_list = page.locator(
            "[data-testid='prescription-results-list']"
        )

        self.page_container = page.locator("[data-testid='prescription-list-page']")
        self.breadcrumb = page.locator("[data-testid='prescription-list-breadcrumb']")
        self.results_heading = page.locator("[data-testid='results-heading']")
        self.results_container = page.locator(
            "[data-testid='prescription-results-container']"
        )
