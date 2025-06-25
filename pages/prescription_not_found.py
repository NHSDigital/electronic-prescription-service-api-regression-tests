from playwright.sync_api import Page


class PrescriptionNotFound:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page

        self.heading = page.get_by_test_id("presc-not-found-heading")
        self.query_summary = page.get_by_test_id("query-summary")
        self.back_link = page.get_by_test_id("go-back-link")
