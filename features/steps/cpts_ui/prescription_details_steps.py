from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.prescription_details import PrescriptionDetailsPage

# FIXME: Remove references to the dev link when we can navigate properly to the prescription details
from pages.prescription_list_page import PrescriptionListPage


@given('I go to the prescription details for prescription ID "{prescription_id}"')
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


@then("The prescriber site card is {visibility}")
def the_prescriber_site_card_is_visible(context, visibility):
    page = PrescriptionDetailsPage(context.page)

    if visibility == "visible":
        expect(page.prescriber_card).to_be_visible()
        expect(page.prescribed_from_field).to_be_visible()
    elif visibility == "not visible":
        expect(page.prescriber_card).not_to_be_visible()
        expect(page.prescribed_from_field).not_to_be_visible()
    else:
        raise ValueError(f"Unrecognised visibility definition: {visibility}")


@then("The dispenser site card is {visibility}")
def the_dispenser_site_card_is_visible(context, visibility):
    page = PrescriptionDetailsPage(context.page)

    if visibility == "visible":
        expect(page.dispenser_card).to_be_visible()
    elif visibility == "not visible":
        expect(page.dispenser_card).not_to_be_visible()
    else:
        raise ValueError(f"Unrecognised visibility definition: {visibility}")


@then("The nominated dispenser site card is {visibility}")
def the_nominated_dispenser_site_card_is_visible(context, visibility):
    page = PrescriptionDetailsPage(context.page)

    if visibility == "visible":
        expect(page.nominated_dispenser_card).to_be_visible()
    elif visibility == "not visible":
        expect(page.nominated_dispenser_card).not_to_be_visible()
    else:
        raise ValueError(f"Unrecognised visibility definition: {visibility}")
