# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.patient_details_banner import PatientDetailsBanner


############################################################################
# THEN STEPS
############################################################################


@then("The patient details banner is not visible")
def patient_details_not_visible(context):
    banner = PatientDetailsBanner(context.page)

    expect(banner.patient_details_banner).not_to_be_visible()


@then("The patient details banner reports complete data")
def i_can_not_see_the_rbac_banner(context):
    banner = PatientDetailsBanner(context.page)

    expect(banner.patient_details_banner).to_be_visible()
    expect(banner.patient_details_banner).not_to_have_class(banner.incomplete_class)


@then("The patient details banner reports incomplete data")
def the_patient_details_banner_reports_incomplete_data(context):
    context.page.wait_for_selector(
        '[data-testid="eps-loading-spinner"]', state="hidden", timeout=3000
    )
    banner = PatientDetailsBanner(context.page)

    expect(banner.patient_details_banner).to_be_visible()
    expect(banner.patient_details_banner).to_have_class(banner.incomplete_class)
