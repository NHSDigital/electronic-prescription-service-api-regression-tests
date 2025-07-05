@cpts_ui @patient_detail_banner @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5061
Feature: The site has a patient detail banner
    
    Background:
        Given a nominated acute prescription has been created
        And I am logged in as a user with a single access role

    Scenario: Before I search for a prescription, the patient details banner is not visible
        Then the patient details banner is not visible

    Scenario: When I search for a prescription, and go back, the patient details banner is not visible
        When I search for the prescription by prescription ID
        And I click the Go Back link on the prescription not found page
        Then The patient details banner is not visible

    Scenario: When I search for a prescription with incomplete data, the patient detail banner is formatted correctly
        When I click on tab Prescription ID search
        And I search for the prescription by prescription ID
        Then The patient details banner reports incomplete data
