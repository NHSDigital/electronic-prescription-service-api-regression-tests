from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_details import PrescriptionDetailsPage
from .search_for_a_prescription_steps import i_am_on_the_search_prescription_page
from .prescription_list_steps import (
    search_context_prescription_id,
    click_view_prescriptions_link,
    i_click_on_tab_heading,
)


@when("I go to the prescription details")
def i_go_to_prescription_details(context):
    prescription_id = context.prescription_id
    i_go_to_prescription_details_for_prescription_id(context, prescription_id)


@when("I go to the past prescription details")
def i_go_to_past_prescription_details(context):
    prescription_id = context.prescription_id
    i_go_to_past_prescription_details_for_prescription_id(context, prescription_id)


@when('I go to the prescription details for prescription ID "{prescription_id}"')
def i_go_to_prescription_details_for_prescription_id(context, prescription_id):
    context.prescription_id = prescription_id
    i_am_on_the_search_prescription_page(context)
    search_context_prescription_id(context)
    click_view_prescriptions_link(context)


@when('I go to the past prescription details for prescription ID "{prescription_id}"')
def i_go_to_past_prescription_details_for_prescription_id(context, prescription_id):
    context.prescription_id = prescription_id
    i_am_on_the_search_prescription_page(context)
    search_context_prescription_id(context)
    i_click_on_tab_heading(context, "past")
    click_view_prescriptions_link(context)


@then("The {org} site card is {visibility}")
def site_card_visibility_check(context, org, visibility):
    page = PrescriptionDetailsPage(context.page)
    context.page.wait_for_selector('[data-testid="patient-details-banner"]')

    expect_prescribed_from_field = False
    match org:
        case "prescriber":
            card = page.prescriber_card
            expect_prescribed_from_field = True
        case "dispenser":
            card = page.dispenser_card
        case "nominated dispenser":
            card = page.nominated_dispenser_card
        case _:
            raise ValueError(f"Unrecognised site definition: {org}")

    if visibility == "visible":
        expect(card).to_be_visible()
        if expect_prescribed_from_field:
            expect(page.prescribed_from_field)

    elif visibility == "not visible":
        expect(card).not_to_be_visible()
        if expect_prescribed_from_field:
            expect(page.prescribed_from_field)

    else:
        raise ValueError(f"Unrecognised visibility definition: {visibility}")


@then("An item card shows an EPS status tag")
def item_card_eps_status_tag(context):
    page = PrescriptionDetailsPage(context.page)

    expect(page.eps_status_tag.first).to_be_visible()


@then("An item card shows a cancellation warning")
def item_card_cancellation_warning(context):
    warning = context.page.get_by_text("This item is pending cancellation.").first
    expect(warning).to_be_visible()


@then("No pharmacy status label is shown in the item card")
def no_pharmacy_status_labels(context):
    page = PrescriptionDetailsPage(context.page)

    pharmacy_status_label = page.prescription_summary.locator(
        ".nhsuk-summary-list__key", has_text="Pharmacy status"
    )
    expect(pharmacy_status_label).to_have_count(0)


@then("The message history timeline is visible")
def timeline_visible(context):
    page = PrescriptionDetailsPage(context.page)
    expect(page.message_history_timeline).to_be_visible()


@then("A dispense notification information dropdown is shown")
def dispense_notification_dropdown(context):
    page = PrescriptionDetailsPage(context.page)
    expect(page.dispense_notification_dropdown).to_be_visible()


@then("A pending cancellation message is shown")
def pending_cancellation_message(context):
    page = PrescriptionDetailsPage(context.page)
    expect(page.pending_cancellation_message).to_be_visible()


@then("A cancelled status message is shown")
def cancelled_status_message(context):
    page = PrescriptionDetailsPage(context.page)
    expect(page.cancelled_status_message).to_be_visible()


@then("The timeline shows fallback text for missing site names")
def fallback_site_name_in_timeline(context):
    page = PrescriptionDetailsPage(context.page)
    expect(page.no_organisation_name_message).to_be_visible()
