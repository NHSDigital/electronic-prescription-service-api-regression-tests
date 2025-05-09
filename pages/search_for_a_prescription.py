from playwright.sync_api import Page


class SearchForAPrescription:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.temp_text = (
            page.locator("div").filter(has_text="Search for a prescription").nth(2)
        )
        self.hero_banner = page.get_by_test_id("hero-heading")
        self.prescription_id_search_tab = page.get_by_role(
            "tab", name="Prescription ID search"
        )
        self.nhs_number_search_tab = page.get_by_role("tab", name="NHS number search")
        self.basic_details_search_tab = page.get_by_role(
            "tab", name="Basic details search"
        )
        self.prescription_id_search_header = page.get_by_test_id(
            "prescription-id-search-heading"
        )
        self.nhs_number_search_header = page.get_by_test_id("nhs-number-search-heading")
        self.basic_details_search_header = page.get_by_test_id(
            "basic-details-search-heading"
        )
        self.nhs_number_input = page.get_by_test_id("nhs-number-input")
        self.find_patient_button = page.get_by_test_id("find-patient-button")
        self.prescription_id_input = page.get_by_test_id("prescription-id-input")
        self.find_prescription_button = page.get_by_test_id("find-prescription-button")
        self.error_summary = page.get_by_test_id("error-summary")
