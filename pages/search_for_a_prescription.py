from playwright.sync_api import Page


class SearchForAPrescription:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
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
        self.error_summary = page.get_by_test_id("error-summary")

        self.prescription_id_error = page.get_by_test_id("prescription-id-error")
        self.prescription_id_input = page.get_by_test_id("prescription-id-input")
        self.find_prescription_button = page.get_by_test_id("find-prescription-button")

        self.nhs_number_input = page.get_by_test_id("nhs-number-input")
        self.find_patient_button = page.get_by_test_id("find-patient-button")

        self.basic_details_first_name = page.get_by_test_id("first-name-input")
        self.basic_details_last_name = page.get_by_test_id("last-name-input")
        self.basic_details_dob_day = page.get_by_test_id("dob-day-input")
        self.basic_details_dob_month = page.get_by_test_id("dob-month-input")
        self.basic_details_dob_year = page.get_by_test_id("dob-year-input")
        self.basic_details_postcode = page.get_by_test_id("postcode-input")
