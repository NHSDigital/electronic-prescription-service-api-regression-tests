from playwright.sync_api import Page


class Logout:
    def __init__(self, page: Page):
        """
        Initialise the Logout page object with locators and text constants.
        """
        page.wait_for_load_state()
        self.page = page

        # The header link should always be visible
        self.logout_modal_header_link = page.get_by_test_id("eps_header_logout")

        # Modal elements
        self.logout_modal_logout_button = page.get_by_role("button", name="Log out")
        self.logout_modal_cancel_button = page.get_by_role("button", name="Cancel")
        self.logout_modal_close_button = page.get_by_label("Close modal")
        self.logout_modal_overlay = page.get_by_test_id("eps-modal-overlay")
        self.logout_modal_content = page.get_by_test_id("eps-modal-content")

        # Logout successful page elements
        self.logout_page_heading = page.get_by_role("heading", name="Logout successful")
        self.logout_page_content = page.get_by_text("You are now logged out of the")
        self.logout_page_login_link = page.get_by_role("link", name="Log in")
