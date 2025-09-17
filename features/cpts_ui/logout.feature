@cpts_ui @logout @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4809
@multiple_access
Feature: The user is able to logout of the application

    Background:
        Given I am logged in as a user with multiple access roles

    ############################################################################
    # Logging out
    ############################################################################
    Scenario: Display logout modal when user clicks logout
        When I click the logout button
        Then I see the logout confirmation modal

    @rbac_banner
    Scenario: User confirms logout
        Given the logout confirmation modal is displayed
        When I confirm the logout
        Then I see the logout successful page
        And I can not see the RBAC banner

    @rbac_banner
    Scenario: User can log back in from the logout successful page
        Given I am on the logout successful page
        When I click the "log back in" button
        Then I am on the login page
        And I can not see the RBAC banner


    ############################################################################
    # Security Regression Tests
    ############################################################################
    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5314
    @security_regression
    Scenario: Browser back button blocked after logout
        Given I have confirmed a role
        And I am on the search for a prescription page
        And I am on the logout successful page
        When I navigate back using browser history
        Then I should be redirected to the login page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5314
    @security_regression
    Scenario: Direct navigation to protected routes blocked after logout
        Given I have confirmed a role
        Given I am on the logout successful page
        When I directly navigate to "/site/search-by-prescription-id"
        Then I should be redirected to the login page

    ############################################################################
    # Closing the logout modal
    ############################################################################
    Scenario: Close the modal with the cross icon
        Given the logout confirmation modal is displayed
        When I close the modal with the cross
        Then the logout confirmation modal is not displayed

    Scenario: Close the modal with the cancel button
        Given the logout confirmation modal is displayed
        When I close the modal with the cancel button
        Then the logout confirmation modal is not displayed

    Scenario: Close the modal by clicking outside the modal
        Given the logout confirmation modal is displayed
        When I close the modal by clicking outside the modal
        Then the logout confirmation modal is not displayed

    Scenario: Close the modal by pressing the escape key
        Given the logout confirmation modal is displayed
        When I close the modal by hitting escape
        Then the logout confirmation modal is not displayed
