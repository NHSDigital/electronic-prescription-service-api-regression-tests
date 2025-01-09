@cpts_ui @select_your_role @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Role selection page renders roles properly when logged in

    Background:
        Given I am logged in

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User is redirected to the select your role page
        Then I am on the select your role page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can see the summary container, but not the table contents by default
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
    Scenario: User can expand the summary table to see the contents. Clicking again hides it
        When I click on the summary expander
        Then I can see the summary table body
        And I can see the table body has a header row
        And I can see the table body has data
        When I click on the summary expander
        Then I can see the summary container
        And I cannot see the summary table body

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
    Scenario: User can see roles with access cards
        Then I can see the roles with access cards

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
    Scenario: User can navigate to the your selected role page
        Then I can navigate to the your selected role page by clicking a card

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4658
    Scenario: User can see the header on the select your role page
        Then I can see the your selected role header

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4658
    Scenario: User can see the subheader on the select your role page
        Then I can see the your selected role subheader
