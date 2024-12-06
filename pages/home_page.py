from playwright.sync_api import Page, expect


class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.header = "NHS LogoClinical prescription"
        self.footer = "[id='eps_footer']"
        self.eps_header_confirmRoleLink = "eps_header_confirmRoleLink"
        self.menu_button = "Browse Menu"
        self.eps_header_prescription_search_link = "eps_header_prescriptionSearchLink"
        self.prescription_id_search_tab = "Prescription ID search"
        self.nhs_number_search_tab = "NHS number search"
        self.basic_details_search_tab = "Basic details search"
        self.prescription_id_search_header = "Prescription ID search"
        self.nhs_number_search_tab_header = "NHS number search"
        self.basic_details_search_tab_header = "Basic details search"

    # expect(page.get_by_test_id("eps_header_prescriptionSearchLink")).to_be_visible()
    # page.get_by_test_id("eps_header_prescriptionSearchLink").click()
    # expect(page.get_by_role("tab", name="Prescription ID search")).to_be_visible()
    # expect(page.get_by_role("tab", name="NHS number search")).to_be_visible()
    # expect(page.get_by_role("tab", name="Basic details search")).to_be_visible()
    # page.get_by_role("tab", name="NHS number search").click()
    # page.get_by_role("tab", name="Basic details search").click()
    # page.get_by_role("tab", name="Prescription ID search").click()
    # expect(page.get_by_role("heading", name="Prescription ID Search")).to_be_visible()
    # page.get_by_role("tab", name="NHS number search").click()
    # expect(page.get_by_role("heading", name="NHS Number Search")).to_be_visible()
    # page.get_by_role("tab", name="Basic details search").click()
    # expect(page.get_by_role("heading", name="Basic Details Search")).to_be_visible()

    def verify_header_link(self):
        expect(
            self.page.get_by_role("link", name="Clinical prescription")
        ).to_be_visible()

    def verify_header_is_visible(self):
        expect(self.page.get_by_text(self.header)).to_be_visible()

    def verify_footer_is_visible(self):
        self.page.is_visible(self.footer)

    def verify_header_links_large_view(self):
        expect(
            self.page.get_by_test_id(self.eps_header_prescription_search_link)
        ).to_be_visible()
        expect(
            self.page.get_by_test_id(self.eps_header_confirmRoleLink)
        ).to_be_visible()

    def verify_header_links_short_width_view(self):
        expect(self.page.get_by_role("button", name=self.menu_button)).to_be_visible()
        self.page.get_by_role("button", name=self.menu_button).click()
        expect(
            self.page.get_by_test_id(self.eps_header_confirmRoleLink)
        ).to_be_visible()
        expect(
            self.page.get_by_test_id(self.eps_header_prescription_search_link)
        ).to_be_visible()
        self.page.get_by_role("button", name=self.menu_button).click()
        expect(self.page.get_by_test_id(self.eps_header_confirmRoleLink)).to_be_visible(
            visible=False
        )
        expect(
            self.page.get_by_test_id(self.eps_header_prescription_search_link)
        ).to_be_visible(visible=False)
