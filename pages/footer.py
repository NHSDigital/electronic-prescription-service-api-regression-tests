from playwright.sync_api import Page


class Footer:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.footer = page.get_by_test_id("eps_footer")
        self.copyright = page.get_by_test_id("eps_footer-copyright")
        self.privacy_notice_link = page.get_by_test_id(
            "eps_footer-link-privacy-notice-opens-in-new-tab"
        )
        self.terms_link = page.get_by_test_id("eps_footer-link-terms-and-conditions")
        self.cookie_link = page.get_by_test_id("eps_footer-link-cookie-policy")

        # Map readable names to locators
        self.link_map = {
            "privacy notice (opens in new tab)": self.privacy_notice_link,
            "terms and conditions": self.terms_link,
            "cookie policy": self.cookie_link,
        }

    def click_link(self, name: str):
        name = name.lower().strip()
        if name == "privacy notice":
            # External links normally open in a new tab (target="_blank"),
            # which Playwright can't follow for assertions like checking the new URL.
            # Removing the `target` ensures we stay in the same context for testing.
            self.privacy_notice_link.evaluate(
                "element => element.removeAttribute('target')"
            )
            self.privacy_notice_link.click()
        elif name == "terms and conditions":
            self.terms_link.click()
        elif name == "cookie policy":
            self.cookie_link.click()
        else:
            raise ValueError(f"Unknown link name: {name}")
