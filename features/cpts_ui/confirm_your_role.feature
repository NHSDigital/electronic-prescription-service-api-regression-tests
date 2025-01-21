@cpts_ui @confirm_role @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4537
Feature: When the user selects a role, they see a confirmation page

    Background:
        Given I am logged in
    
    Scenario:
        Given I go to the select your role page
        And I have a selected role
        Then I see the 'confirm your role' page
    
    Scenario:
        Given I am on the change your role page
        When I click a change role role card
        Then I see the 'confirm your role' page

    Scenario:
        Given I am on the confirm your role page
        When I click the change link next to the role text
        Then I am on the change role page

    Scenario:
        Given I am on the confirm your role page
        When I click the change link next to the org text
        Then I am on the change role page

    Scenario:
        Given I am on the confirm your role page
        When I click the confirm and continue button on the confirm role page
        Then I am on the search for a prescription page
