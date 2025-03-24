from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.header = "[id='eps_header']"

        self.menu_button = self.page.get_by_role("button", name="Browse Menu")
        self.exit_link = page.get_by_test_id("eps_header_exit")
        self.logout_link = page.get_by_test_id("eps_header_logout")
        self.select_role_link = page.get_by_test_id("eps_header_selectYourRoleLink")
        self.change_role_link = page.get_by_test_id("eps_header_changeRoleLink")
