from playwright.sync_api import Page


class Home:

    def __init__(self, page: Page):
        self.page = page
        self.header = "[id='eps_header']"
        self.footer = "[id='eps_footer']"
        self.confirm_role_link = self.page.get_by_test_id("eps_header_confirmRoleLink")
        self.find_a_prescription_link = self.page.get_by_test_id(
            "eps_header_prescriptionSearchLink"
        )
        self.menu_button = self.page.get_by_role("button", name="Browse Menu")
