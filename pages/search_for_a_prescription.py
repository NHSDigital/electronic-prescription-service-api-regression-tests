from playwright.sync_api import Page


class SearchForAPrescription:

    def __init__(self, page: Page):
        self.page = page
        self.hero_banner = page.get_by_test_id("hero-heading")
        self.prescription_id_search_tab = page.get_by_role(
            "tab", name="Prescription ID search"
        )
        self.nhs_number_search_tab = page.get_by_role("tab", name="NHS number search")
        self.basic_details_search_tab = page.get_by_role(
            "tab", name="Basic details search"
        )
        self.prescription_id_search_header = page.get_by_role(
            "heading", name="Prescription ID Search"
        )
        self.nhs_number_search_header = page.get_by_role(
            "heading", name="NHS Number Search"
        )
        self.basic_details_search_header = page.get_by_role(
            "heading", name="Basic Details Search"
        )
