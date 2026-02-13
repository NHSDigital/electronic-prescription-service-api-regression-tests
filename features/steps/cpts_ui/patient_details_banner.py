# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from eps_test_support.pages.patient_details_banner import PatientDetailsBanner

############################################################################
# THEN STEPS
############################################################################


@then("The patient details banner is not visible")
def patient_details_not_visible(context):
    banner = PatientDetailsBanner(context.active_page)

    expect(banner.patient_details_banner).not_to_be_visible()


@then("The patient details banner reports complete data")
def i_can_not_see_the_rbac_banner(context):
    banner = PatientDetailsBanner(context.active_page)

    expect(banner.patient_details_banner).to_be_visible()
