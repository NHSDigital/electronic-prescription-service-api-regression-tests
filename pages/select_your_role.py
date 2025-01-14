from playwright.sync_api import Page


class SelectYourRole:

    def __init__(self, page: Page):
        self.page = page
        self.select_your_role_link = page.get_by_test_id(
            "eps_header_selectYourRoleLink"
        )
        self.main_header = page.get_by_role("main").get_by_text(
            "Select your role - Select the"
        )
        self.secondary_text = page.get_by_text(
            "- Select the role you wish to use to access the service.", exact=True
        )
        self.logged_in_message = page.get_by_text("You are currently logged in")
