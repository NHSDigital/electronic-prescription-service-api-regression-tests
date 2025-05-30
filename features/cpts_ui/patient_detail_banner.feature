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

    Scenario: When I search for a prescription, and go back, the patient details banner is not visible
        When I go to the search for a prescription page
        And I click on tab Prescription ID search
        # FIXME: This will need to be updated when the search pages are updated to use real data
        And I search for a prescription using a valid prescription ID "F3B7CD-A83008-5AF044"
        And I click the Go Back link on the prescription not found page
        Then The patient details banner is not visible

    Scenario: When I search for a prescription, the patient details appear
        When I go to the search for a prescription page
        And I click on tab Prescription ID search
        # FIXME: This will need to be updated when the search pages are updated to use real data
        And I search for a prescription using a valid prescription ID "C0C757-A83008-C2D93O"
        Then The patient details banner reports complete data

    # TODO: Can we set a prescription with incomplete patient data?
    # Scenario: When I search for a prescription with incomplete data, the patient detail banner is formatted correctly
    #     When I go to the search for a prescription page
    #     And I click on tab Prescription ID search
    #     When I go to the prescription details for prescription ID "209E3D-A83008-327F9F"
    #     Then The patient details banner reports incomplete data
