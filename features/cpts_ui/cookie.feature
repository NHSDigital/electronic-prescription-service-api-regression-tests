@cpts_ui @cookie @regression @blocker @smoke @ui
Feature: Users interact with the cookie banner

    Background:
        Given I am logged in as a user with a single access role
        And I am on the search for a prescription page


    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can see the cookie banner
        Then I can see the cookie banner

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario Outline: User can accept or reject cookies by pressing the relevant button
        When I press the <Button Name> button
        Then I see the smaller cookie banner
        Examples:
          | Button Name |
          | accept      |
          | reject      |

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario: User can click the link to view cookies policy
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

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5182
    Scenario Outline: User can choose use/do not use my cookies on the policy page
        Given I am on the cookies page
        When I click "<option>" cookies and save
        Then I go to the cookies selected page
        Examples:
            | option     |
            | use        |
            | do not use |

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5315
    Scenario: User selects use cookies and RUM cookies are stored
        Given I am on the cookies page
        When I click use cookies and save
        Then I do have RUM cookies

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5315
    Scenario: User selects do not use cookies and RUM cookies are not stored
        Given I am on the cookies page
        When I click "do not use" cookies and save
        Then I do not have RUM cookies

##TODO: create test scenarios for link to privacy policy and cloudwatch rum privacy policy
