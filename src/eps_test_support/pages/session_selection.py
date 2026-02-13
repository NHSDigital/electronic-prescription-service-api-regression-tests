from playwright.sync_api import Page


class SessionSelectionPage:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.url = "/session-selection"  # Adjust URL as needed

        # Main container
        self.main_container = page.get_by_test_id("session-selection-page")

        # Page content elements
        self.title = page.get_by_test_id("title")
        self.description = page.get_by_test_id("description")
        self.instructions = page.get_by_test_id("instructions")

        # Action buttons
        self.new_session_button = page.get_by_role("button", name="Start a new session")
        self.close_window_button = page.get_by_role("button", name="Close this window")
