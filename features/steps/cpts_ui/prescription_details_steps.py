from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_details import PrescriptionDetailsPage


@when('I go to the prescription details for prescription ID "{prescription_id}"')
def i_go_to_prescription_details_for_prescription_id(context, prescription_id):
    context.prescription_id = prescription_id
    context.execute_steps(
        f"""
    When I search for a prescription using a valid prescription ID "{prescription_id}"
    And I click through to the prescription details page
    """
    )


@when("I click through to the prescription details page")
def i_click_to_prescription_details_page(context):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )
    prescription_id = context.prescription_id
    full_test_id = f"view-prescription-link-{prescription_id}"

    context.page.wait_for_selector(f'[data-testid="{full_test_id}"]')
    context.page.get_by_test_id(full_test_id).click()


@then("The {org} site card is {visibility}")
def site_card_visibility_check(context, org, visibility):
    page = PrescriptionDetailsPage(context.page)
    context.page.wait_for_selector(
        '[data-testid="patient-details-banner"]', timeout=3000
    )

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
