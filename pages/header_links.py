from playwright.sync_api import Page


class HeaderLinks:
    def __init__(self, page: Page):
        self.page = page

        self.exit_link = page.get_by_test_id("eps_header_exit")
        self.logout_link = page.get_by_test_id("eps_header_logout")
        self.select_role_link = page.get_by_test_id("eps_header_selectYourRoleLink")
        self.change_role_link = page.get_by_test_id("eps_header_changeRoleLink")
