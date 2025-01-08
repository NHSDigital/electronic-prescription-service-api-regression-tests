# pylint: disable=no-name-in-module
from behave import given, when, then  # pyright: ignore [reportAttributeAccessIssue]
from playwright.sync_api import expect

from pages.home import Home
from pages.search_for_a_prescription import SearchForAPrescription
from features.environment import MOCK_CIS2_LOGIN_ID_3


@given("I am logged in with a single access role")
def login_single_role(context):
    context.page.goto(context.cpts_ui_base_url + "site/auth_demo.html")
    context.page.get_by_role("button", name="Log in with mock CIS2").click()
    context.page.get_by_label("Username").fill(MOCK_CIS2_LOGIN_ID_3)
    context.page.get_by_role("button", name="Sign In").click()
    context.page.wait_for_url("**/searchforaprescription")


@when("I go to the search for a prescription page")
def goto_page(context):
    context.page.goto(context.cpts_ui_base_url + "site/")
    home = Home(context.page)
    home.find_a_prescription_link.click()


@given("I am on the search for a prescription page")
def go_to_search_prescription_page(context):
    context.execute_steps("when I go to the search for a prescription page")
    expect(context.page).to_have_title("Search for a prescription")


@then("I am on the search for a prescription page")
def i_am_on_the_search_prescription_page(context):
    search_for_a_prescription = SearchForAPrescription(context.page)
    expect(search_for_a_prescription.temp_text).to_be_visible()


@when("I click on tab {}")
def i_click_on_tab(context, tab_name):
    search_for_a_prescription = SearchForAPrescription(context.page)
    match tab_name.lower():
        case "prescription id search":
            search_for_a_prescription.prescription_id_search_tab.click()
        case "nhs number search":
            search_for_a_prescription.nhs_number_search_tab.click()
        case "basic details search":
            search_for_a_prescription.basic_details_search_tab.click()
        case _:
            raise AssertionError("Unknown tab {}".format(tab_name))


@then("I am on tab {}")
def i_am_on_tab(context, tab_name):
    search_for_a_prescription = SearchForAPrescription(context.page)
    match tab_name.lower():
        case "prescription id search":
            expect(
                search_for_a_prescription.prescription_id_search_header
            ).to_be_visible()
            expect(search_for_a_prescription.nhs_number_search_header).to_be_visible(
                visible=False
            )
            expect(search_for_a_prescription.basic_details_search_header).to_be_visible(
                visible=False
            )
        case "nhs number search":
            expect(
                search_for_a_prescription.prescription_id_search_header
            ).to_be_visible(visible=False)
            expect(search_for_a_prescription.nhs_number_search_header).to_be_visible()
            expect(search_for_a_prescription.basic_details_search_header).to_be_visible(
                visible=False
            )
        case "basic details search":
            expect(
                search_for_a_prescription.prescription_id_search_header
            ).to_be_visible(visible=False)
            expect(search_for_a_prescription.nhs_number_search_header).to_be_visible(
                visible=False
            )
            expect(
                search_for_a_prescription.basic_details_search_header
            ).to_be_visible()
        case _:
            raise AssertionError("Unknown tab {}".format(tab_name))


@then("I can see the search for a prescription header")
def i_can_see_the_search_for_a_prescription_header(context):
    search_for_a_prescription = SearchForAPrescription(context.page)
    expect(search_for_a_prescription.hero_banner).to_be_visible()
