from playwright.sync_api import Page
import re


class PatientDetailsBanner:
    def __init__(self, page: Page):
        self.page = page

        self.patient_details_banner = page.get_by_test_id("patient-details-banner")

        # This has to match the class with regex
        self.incomplete_class = re.compile(".*patient-details-partial-data.*")
