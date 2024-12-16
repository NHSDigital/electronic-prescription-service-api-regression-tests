@cpts_ui @select_your_role @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Role selection page renders roles properly when logged in

    Background:
        Given I am logged in
        And I am on the SLR page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can navigate to the SLR page
        Then I am on the SLR page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can see the summary container, but not the table contents by default
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can expand the summary table to see the contents
        When I click on the summary expander
        Then I can see the summary table body
        And I can see the table body has a header row
        And I can see the table body has data
