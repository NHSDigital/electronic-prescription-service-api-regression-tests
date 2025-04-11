from playwright.sync_api import Page


class PrescriptionInformationBanner:
    def __init__(self, page: Page):
        self.page = page
        self.banner = page.get_by_test_id("prescription-information-banner")
        self.prescription_id = page.locator("#prescription-id")
        self.issue_date = page.locator("#summary-issue-date")
        self.status = page.locator("#summary-status")
        self.prescription_type = page.locator("#summary-type")
        self.repeat = page.locator("#summary-erd-instance")
        self.days_supply = page.locator("#summary-erd-days")
        self.copy_button = page.locator("#copyButton")
