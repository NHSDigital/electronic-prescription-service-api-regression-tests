from playwright.sync_api import Page


class Home:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.footer = "[id='eps_footer']"
