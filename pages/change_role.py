from playwright.sync_api import Page


class ChangeRole:
    def __init__(self, page: Page):
        """
        Initialise the ChangeRole page object with locators and text constants.
        """
        self.page = page

        # Title and summary locators
        self.roles_without_access_table = page.locator("summary")
        self.roles_without_access_organisation_column_header = page.get_by_role(
            "columnheader", name="Organisation"
        )
        self.roles_without_access_role_column_header = page.get_by_role(
            "columnheader", name="Role"
        )
        self.roles_without_access_table_body = page.get_by_role("group").locator("div")
        # TODO: This needs to be more generic
        self.first_row_org_name = page.get_by_role(
            "cell", name="No Org Name (ODS: X09)"
        ).first
        # TODO: This needs to be more generic
        self.first_row_role_name = page.get_by_role(
            "cell", name="Registration Authority Agent"
        ).first

        # Role cards - roles with access
        self.roles_with_access_cards = page.locator(".nhsuk-card--clickable")
        self.first_role_card = self.roles_with_access_cards.first
        self.role_card_headings = page.locator(".nhsuk-card__heading")
        self.role_card_descriptions = page.locator(".eps-card__roleName")

        # Header locators
        self.select_role_header = page.locator(
            "span[data-testid='eps_header_selectYourRole'] > span.nhsuk-title"
        )

        # Subheader locators
        self.select_role_subheader = page.locator(
            "span.nhsuk-caption-l.nhsuk-caption--bottom"
        )