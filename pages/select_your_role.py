from playwright.sync_api import Page


class SelectYourRole:
    def __init__(self, page: Page):
        self.page = page

        self.slr_title = "Select your role"
        self.summary = page.locator("summary")
        self.organisation_column_header = page.get_by_role(
            "columnheader", name="Organisation"
        )
        self.role_column_header = page.get_by_role("columnheader", name="Role")
        self.roles_without_access_table_body = page.get_by_role("group").locator("div")
        self.first_row_org_name = page.get_by_role(
            "cell", name="No Org Name (ODS: X09)"
        ).first
        self.first_row_role_name = page.get_by_role(
            "cell", name="Registration Authority Agent"
        ).first

        self.roles_with_access_cards = page.locator(".nhsuk-card--clickable")
        self.first_role_card = self.roles_with_access_cards.first
        self.role_card_headings = page.locator(".nhsuk-card__heading")
        self.role_card_descriptions = page.locator(".eps-card__roleName")
        self.selected_role_url = "**/site/yourselectedrole"

        self.header = "[id='eps_header']"
        self.footer = "[id='eps_footer']"
