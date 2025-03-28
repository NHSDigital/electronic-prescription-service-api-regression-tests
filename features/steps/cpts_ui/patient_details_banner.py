# pylint: disable=no-name-in-module
from behave import then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.patient_details_banner import PatientDetailsBanner


############################################################################
# THEN STEPS
############################################################################


@then("the patient details banner is visible")
def i_can_see_the_rbac_banner(context):
    banner = PatientDetailsBanner(context.page)

    expect(banner.patient_details_banner).to_be_visible()


@then("the patient details banner is not visible")
def i_can_not_see_the_rbac_banner(context):
    banner = PatientDetailsBanner(context.page)

    expect(banner.patient_details_banner).not_to_be_visible()


@then("The patient details banner reports complete data")
def the_patient_details_banner_reports_complete_data(context):
    banner = PatientDetailsBanner(context.page)

    expect(banner.incomplete_patient_details_banner).not_to_be_visible()


@then("The patient details banner reports incomplete data")
def the_patient_details_banner_reports_incomplete_data(context):
    banner = PatientDetailsBanner(context.page)

    expect(banner.incomplete_patient_details_banner).to_be_visible()
