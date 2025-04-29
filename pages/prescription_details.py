from playwright.sync_api import Page


class PrescriptionDetailsPage:

    def __init__(self, page: Page):
        page.wait_for_load_state()
        self.page = page
        self.url = "/prescription-details"

        # Site org cards
        self.dispenser_card = page.get_by_test_id("site-card-dispenser")
        self.nominated_dispenser_card = page.get_by_test_id(
            "site-card-nominated-dispenser"
        )
        self.prescriber_card = page.get_by_test_id("site-card-prescriber")
        self.prescribed_from_field = page.get_by_test_id("site-card-prescribed-from")

        # Prescribed and dispensed items cards
        self.prescribed_items_heading = page.get_by_role(
            "heading", name="Prescribed items"
        )
        self.dispensed_items_heading = page.get_by_role(
            "heading", name="Dispensed items"
        )

        # Cancellation warning
        self.cancellation_warning = page.get_by_test_id("cancellation-warning")

        # Summary details
        self.prescription_summary = page.get_by_test_id("prescription-summary-list")
        self.initial_prescription_details = page.get_by_test_id(
            "initial-prescription-details"
        )
        self.initial_prescription_summary = page.get_by_test_id(
            "initial-prescription-summary-list"
        )

        # EPS status tag
        self.eps_status_tag = page.get_by_test_id("eps-status-tag")

        # Message history card
        self.message_history_timeline = page.get_by_test_id("message-history-timeline")
        self.dispense_notification_dropdown = page.get_by_test_id(
            "message-history-dropdown"
        )
        self.pending_cancellation_message = page.get_by_test_id(
            "pending-cancellation-message"
        )
        self.cancelled_status_message = "Cancelled"
        self.site_name_fallback_message = (
            "Organisation name not available. Try again later."
        )
