from playwright.sync_api import Page
import re


class RBACBannerPage:
    def __init__(self, page: Page):
        self.page = page

        self.banner_text = re.compile(
            r"^CONFIDENTIAL: PERSONAL PATIENT DATA accessed by (.{1,255}), "
            r"(.{1,255}) - (.{1,255}) - (.{1,255}) \(ODS: (.{3,8})\)$"
        )

        self.rbac_banner = page.get_by_test_id("rbac-banner-div")
        self.rbac_content = page.get_by_test_id("rbac-banner-text")
