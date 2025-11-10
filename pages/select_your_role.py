from playwright.sync_api import Page


class SelectYourRole:
    def __init__(self, page: Page):
        """
        Initialise the SelectYourRole page object with locators and text constants.
        """
        page.wait_for_load_state()
        self.page = page

        self.page_loaded_indicator = page.get_by_test_id("eps_roleSelectionComponent")

        # Title and summary locators
        self.summary = page.locator("summary")
        self.organisation_column_header = page.get_by_role(
            "columnheader", name="Organisation"
        )
        self.role_column_header = page.get_by_role("columnheader", name="Role")

        # Roles without access
        self.roles_without_access_table_body = page.get_by_role("group").locator("div")

        self.first_row_org_name = page.get_by_test_id("change-role-name-cell").first
        self.first_row_role_name = page.get_by_test_id("change-role-role-cell").first

        # Role cards - roles with access
        self.roles_with_access_cards = page.get_by_test_id("eps-card")
        self.first_role_card = page.locator(".eps-card__org-focus-area").first
        self.role_card_headings = page.locator(".nhsuk-card__heading")
        self.role_card_descriptions = page.locator(".eps-card__roleName")

        self.select_role_header = page.locator(
            "span[data-testid='eps_header_selectYourRole'] > span.nhsuk-title"
        )
        self.select_role_subheader = page.locator(
            "span.nhsuk-caption-l.nhsuk-caption--bottom"
        )

        self.no_access_header = page.locator(".nhsuk-heading-xl")
        self.no_access_message = page.get_by_text("None of the roles on your")
        self.roles_without_access_header = page.get_by_role(
            "heading", name="Your roles without access"
        )
        self.first_row_org_name_no_access = page.get_by_role(
            "cell", name="NO ORG NAME (ODS: A21464)"
        ).first
        self.first_row_role_name_no_access = page.get_by_role(
            "cell", name="General Medical Practitioner"
        ).first
