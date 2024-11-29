from playwright.sync_api import Page, expect


class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.header = "NHS LogoClinical prescription"
        self.footer = "[id='eps_footer']"
        self.eps_header_placeholder1 = "eps_header_placeholder1"
        self.eps_header_placeholder2 = "eps_header_placeholder2"
        self.eps_header_placeholder3 = "eps_header_placeholder3"
        self.eps_header_confirmRoleLink = "eps_header_confirmRoleLink"
        self.menu_button = "Browse Menu"

    def verify_header_link(self):
        expect(
            self.page.get_by_role("link", name="Clinical prescription")
        ).to_be_visible()

    def verify_header_is_visible(self):
        expect(self.page.get_by_text(self.header)).to_be_visible()

    def verify_footer_is_visible(self):
        self.page.is_visible(self.footer)

    def verify_header_links_large_view(self):
        expect(self.page.get_by_test_id(self.eps_header_placeholder1)).to_be_visible()
        expect(self.page.get_by_test_id(self.eps_header_placeholder2)).to_be_visible()
        expect(self.page.get_by_test_id(self.eps_header_placeholder3)).to_be_visible()
        expect(
            self.page.get_by_test_id(self.eps_header_confirmRoleLink)
        ).to_be_visible()

    def verify_header_links_900_pixels_wide_view(self):
        expect(self.page.get_by_role("button", name=self.menu_button)).to_be_visible()
        self.page.get_by_role("button", name=self.menu_button).click()
        expect(
            self.page.get_by_test_id(self.eps_header_confirmRoleLink)
        ).to_be_visible()
        expect(self.page.get_by_test_id(self.eps_header_placeholder3)).to_be_visible()
        self.page.get_by_role("button", name=self.menu_button).click()
        expect(self.page.get_by_test_id(self.eps_header_confirmRoleLink)).to_be_visible(
            visible=False
        )
        expect(self.page.get_by_test_id(self.eps_header_placeholder3)).to_be_visible(
            visible=False
        )
