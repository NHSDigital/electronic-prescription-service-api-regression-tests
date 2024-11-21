from playwright.sync_api import Page, expect


class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.footer = "[id='eps_footer']"

    def verify_header_link(self):
        expect(
            self.page.get_by_role("link", name="Clinical prescription")
        ).to_be_visible()

    def verify_footer_is_visible(self):
        self.page.is_visible(self.footer)
