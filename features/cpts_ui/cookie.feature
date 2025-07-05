@cpts_ui @cookie @regression @blocker @smoke @ui
Feature: Users interact with the cookie banner

    Background:
        Given I am on the privacy notice page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can see the cookie banner when not logged in
        Then I can see the cookie banner

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can see the cookie banner when logged in
        Given I am logged in as a user with a single access role
        Then I can see the cookie banner

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User has no RUM cookies by default
        Then I do not have RUM cookies

    @skip
    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can accept cookies by pressing the accept button
        When I press the accept button
        Then I see the smaller cookie banner
        And I do have RUM cookies

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can reject cookies by pressing the reject button
        When I press the reject button
        Then I see the smaller cookie banner
        And I do not have RUM cookies

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can click the link to view cookies policy when not logged in
        When I click the cookies policy link
        Then I go to the cookies policy page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can click the link to view cookies policy when logged in
        Given I am logged in as a user with a single access role
        When I click the cookies policy link
        Then I go to the cookies policy page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can click through to cookies policy page from smaller banner
        When I press the accept button
        And I click the small banner cookie policy link
        Then I go to the cookies policy page

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario Outline: User can expand and view the <Table Type> cookies table on the cookies page
        Given I am on the cookies page
        When I expand the <Table Type> cookies details section
        Then I see the table for <Table Type> cookies

        Examples:
          | Table Type |
          | Essential  |
          | Analytics  |

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5315
    Scenario: On the cookie page, user selects use cookies and RUM cookies are stored
        Given I am on the cookies page
        When I click use cookies and save
        Then I do have RUM cookies

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5315
    Scenario: On the cookie page, user selects do not use cookies and RUM cookies are not stored
        Given I am on the cookies page
        When I click "do not use" cookies and save
        Then I do not have RUM cookies


##TODO: create test scenarios for link to privacy notice and cloudwatch rum privacy notice
