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

    # FIXME: This will need to be updated when the search pages are updated
    Scenario Outline: When I search for a prescription, the patient details appear
        When I go to the search for a prescription page
        And I click on tab <Tab Name>
        And I search for a prescription using a valid prescription ID "209E3D-A83008-327F9F"
        Then the patient details banner is visible
        Examples:
            | Tab Name                  |
            | Prescription ID search    |
            # | NHS Number search         |
            # | Basic Details search      |

    Scenario: When I search for a prescription, and go back, the patient details banner is not visible
        When I go to the search for a prescription page
        And I click on tab Prescription ID search
        And I search for a prescription using a valid prescription ID "209E3D-A83008-327F9F"
        And I click on the "Go back" link
        Then the patient details banner is not visible

    # # TODO: Can we set a prescription with incomplete patient data?
    # Scenario: When I search for a prescription with incomplete data, the patient detail banner is formatted correctly
    #     # FIXME: Placeholder
    #     When I search for a prescription with incomplete data
    #     Then the patient details banner is visible
    #     And the patient details banner reports incomplete data
