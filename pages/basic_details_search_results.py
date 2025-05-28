from playwright.sync_api import Page, expect


class BasicDetailsSearchResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "/site/patient-search-results"

        # Main elements
        self.main_content = page.locator("main#main-content")
        self.results_header = page.locator("#results-header")
        self.results_count = page.locator("#results-count")
        self.results_table = page.locator("#results-table")
        self.back_link = page.locator("a.nhsuk-back-link__link")

        # Table elements
        self.table_headers = page.locator("th[id^='header-']")
        self.patient_rows = page.locator("tr[id^='patient-row-']")

    def wait_for_page_load(self):
        """Wait for the page to load"""
        expect(self.results_table).to_be_visible()
        expect(self.results_count).to_be_visible()

    def get_table_headers(self):
        """Get all table header texts"""
        return [header.text_content() for header in self.table_headers.all()]

    def get_patient_rows(self):
        """Get all patient rows in the table"""
        return self.patient_rows.all()

    def get_patient_row_by_name(self, name):
        """Get a specific patient row by name"""
        return self.page.locator(f"tr[id^='patient-row-']:has-text('{name}')").first

    def click_patient_row(self, name):
        """Click on a patient row by name"""
        row = self.get_patient_row_by_name(name)
        row.click()

    def press_enter_on_patient_row(self, name):
        """Press enter on a patient row by name"""
        row = self.get_patient_row_by_name(name)
        row.press("Enter")

    def get_results_count_text(self):
        """Get the results count text"""
        return self.results_count.text_content()

    def click_go_back(self):
        """Click the go back link"""
        self.back_link.click()

    def is_restricted_patient_visible(self, name):
        """Check if a restricted patient is visible in the results"""
        try:
            # Get all patient rows
            rows = self.get_patient_rows()
            # Check if any row contains the restricted patient's name
            for row in rows:
                if name in row.text_content():
                    return True
            return False
        except Exception:
            return False

    def get_patient_row_aria_label(self, name):
        """Get the aria-label of a patient row"""
        row = self.get_patient_row_by_name(name)
        return row.get_attribute("aria-label")

    def is_table_responsive(self):
        """Check if the table has responsive class"""
        class_attr = self.results_table.get_attribute("class")
        return class_attr is not None and "nhsuk-table-responsive" in class_attr

    def get_main_content_role(self):
        """Get the role attribute of the main content"""
        return self.main_content.get_attribute("role")

    def get_table_cell_headers(self, cell_text):
        """Get the headers attribute of a table cell"""
        cell = self.page.locator(f"td:has-text('{cell_text}')").last
        return cell.get_attribute("headers")

    def get_visually_hidden_text(self, nhs_number):
        """Get the visually hidden text for a patient's NHS number"""
        return self.page.locator(f"#patient-details-{nhs_number}").text_content()
