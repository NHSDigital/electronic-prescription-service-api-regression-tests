from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_details import PrescriptionDetailsPage

# FIXME: Remove references to the dev link when we can navigate properly to the prescription details
from pages.prescription_list_page import PrescriptionListPage


@when('I go to the prescription details for prescription ID "{prescription_id}"')
def i_go_to_prescription_details_for_prescription_id(context, prescription_id):
    context.execute_steps(
        f"""
    When I search for a prescription using a valid prescription ID "{prescription_id}"
    And I click through to the prescription details page
    """
    )


# FIXME: THIS IS FOR DEVELOPMENT ONLY - DELETE IT WHEN WE HAVE A PROPER USER FLOW!!!
@when("I click through to the prescription details page")
def i_click_to_prescription_details_page(context):
    page = PrescriptionListPage(context.page)
    page.dev_link.click()

    context.page.wait_for_load_state()


@then("The {org} site card is {visibility}")
def site_card_visibility_check(context, org, visibility):
    page = PrescriptionDetailsPage(context.page)

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
