@cpts_ui @logout @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
Feature: The user is able to logout of the application

    Background:
        Given I am logged in
        And I am on the select your role page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
    Scenario: User can logout of the application
        When I click the logout button
        Then I can see the logout modal
        When I click on the logout modal confirm button
        Then I can see the logout successful page
        When I click the log back in button
        Then I am on the login page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
    Scenario: User can close the modal with the cross
        When I click the logout button
        Then I can see the logout modal
        When I close the modal with the cross
        Then I cannot see the logout modal

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
    Scenario: User can close the modal with the cancel button
        When I click the logout button
        Then I can see the logout modal
        When I close the modal with the close button
        Then I cannot see the logout modal

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
    Scenario: User can close the modal by clicking the overlay
        When I click the logout button
        Then I can see the logout modal
        When I close the modal with the overlay
        Then I cannot see the logout modal

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
    Scenario: User can close the modal with the escape key
        When I click the logout button
        Then I can see the logout modal
        When I close the modal by hitting escape
        Then I cannot see the logout modal
