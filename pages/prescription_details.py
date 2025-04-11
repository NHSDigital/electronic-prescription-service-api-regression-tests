from playwright.sync_api import Page


class PrescriptionDetailsPage:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.url = "/prescription-details"

        # Site org cards
        self.dispenser_card = page.get_by_test_id("site-card-dispenser")
        self.nominated_dispenser_card = page.get_by_test_id(
            "site-card-nominated-dispenser"
        )
        self.prescriber_card = page.get_by_test_id("site-card-prescriber")
        self.prescribed_from_field = page.get_by_test_id("site-card-prescribed-from")
