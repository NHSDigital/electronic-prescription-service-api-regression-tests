@cpts_ui @patient_detail_banner @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5061
Feature: The site has a patient detail banner
    
    Background:
        Given I am logged in as a user with multiple access roles
        And I have confirmed a role

    Scenario: Before I search for a prescription, the patient details banner is not visible
        When I go to the search for a prescription page
        Then I am on the search for a prescription page
        And the patient details banner is not visible

    Scenario: When I search for a prescription, the patient details appear
        When I search for a prescription
        Then the patient details banner is visible
    
    Scenario: When I search for a prescription, then return to the search page, the patient details are no longer visible
        When I search for a prescription
        And I go to the search for a prescription page
        Then I am on the search for a prescription page
        And the patient details banner is not visible
