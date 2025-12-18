from playwright.sync_api import Page


class PatientDetailsBanner:
    def __init__(self, page: Page):
        self.page = page

        self.patient_details_banner = page.get_by_test_id("patient-details-banner")
