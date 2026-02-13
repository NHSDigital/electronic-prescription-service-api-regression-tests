from playwright.sync_api import Page


class RBACBannerPage:
    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page

        self.rbac_banner = page.get_by_test_id("rbac-banner-div")
        self.rbac_content = page.get_by_test_id("rbac-banner-text")
