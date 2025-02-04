from playwright.sync_api import Page


class ConfirmRole:
    def __init__(self, page: Page):
        self.page = page

        self.header = page.get_by_test_id("eps_yourSelectedRole_page")
        self.role_label_cell = page.get_by_test_id("role-label")
        self.org_label_cell = page.get_by_test_id("org-label")
        self.org_text_cell = page.get_by_test_id("org-text")
        self.role_text_cell = page.get_by_test_id("role-text")
        self.role_change_role = page.get_by_test_id("role-change-role-cell")
        self.org_change_role = page.get_by_test_id("org-change-role-cell")
        self.confirm_button = page.get_by_test_id("confirm-and-continue")
