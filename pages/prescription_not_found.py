from playwright.sync_api import Page


class PrescriptionNotFound:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page

        self.header = page.get_by_test_id("presc-not-found-header")
        self.body1 = page.get_by_test_id("presc-not-found-body1")
        self.back_link = page.get_by_test_id("go-back-link")
