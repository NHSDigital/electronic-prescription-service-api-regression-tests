@cpts_ui @privacy_notice @regression @blocker @smoke @ui
Feature: User reads the privacy notice

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4813
    Scenario: User can read privacy notice
        Given I am on the privacy notice page
        And I can see the page footer
        When I click the "privacy notice" link in the footer
        Then I am on the privacy notice page
        And I can read the full privacy notice
