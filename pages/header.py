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
        self.feedback_link = page.get_by_test_id("eps_header_feedbackLink")

    def assert_feedback_link_is_external_and_opens_in_new_tab(self):
        href = self.feedback_link.get_attribute("href")
        target = self.feedback_link.get_attribute("target")

        assert href is not None and "digital.nhs.uk" in href, f"Expected href to contain 'digital.nhs.uk', got: {href}"
        assert target == "_blank", f"Expected target to be '_blank', got: {target}"
