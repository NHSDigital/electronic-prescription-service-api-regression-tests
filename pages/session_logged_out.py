from playwright.sync_api import Page


class SessionLoggedOutPage:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.url = "/session-logged-out"

        # Main containers for different scenarios
        self.concurrent_session_container = page.get_by_test_id(
            "session-logged-out-concurrent"
        )
        self.timeout_session_container = page.get_by_test_id(
            "session-logged-out-timeout"
        )

        # Concurrent session elements
        self.concurrent_title = page.get_by_test_id("concurrent-title")
        self.concurrent_description = page.get_by_test_id("concurrent-description")
        self.concurrent_contact = page.get_by_test_id("concurrent-contact")
        self.nhs_service_desk_email = page.get_by_test_id("nhs-service-desk-email")
        self.concurrent_login_link = page.get_by_test_id("login-link")

        # Timeout session elements
        self.timeout_title = page.get_by_test_id("timeout-title")
        self.timeout_description = page.get_by_test_id("timeout-description")
        self.timeout_description2 = page.get_by_test_id("timeout-description2")
        self.timeout_login_link = page.get_by_test_id("login-link")

    def is_concurrent_session_displayed(self) -> bool:
        """Check if the concurrent session variant is displayed"""
        return self.concurrent_session_container.is_visible()

    def is_timeout_session_displayed(self) -> bool:
        """Check if the timeout session variant is displayed"""
        return self.timeout_session_container.is_visible()
