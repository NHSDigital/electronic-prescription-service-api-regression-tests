@cpts_ui @select_your_role @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Role selection page renders roles properly when logged in

  @rbac_banner
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4656
  Scenario: User is redirected to the select your role page
    When I log in as a user with multiple access roles
    Then I am on the 'your selected role' page
    And I can not see the RBAC banner

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  Scenario: User can see the summary container, but not the table contents by default
    Given I am logged in as a user with multiple access roles
    Then I can see the summary container
    And I cannot see the summary table body

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  Scenario: User can expand the summary table to see the contents. Clicking again hides it
    Given I am logged in as a user with multiple access roles
    When I click on the summary expander
    Then I can see the summary table body
    And I can see the table body has a header row
    And I can see the table body has data
    When I click on the summary expander
    Then I can see the summary container
    And I cannot see the summary table body

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
  Scenario: User can see roles with access cards
    When I log in as a user with multiple access roles
    Then I can see the roles with access cards

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
  Scenario: User can navigate to the your selected role page
    When I log in as a user with multiple access roles
    Then I can navigate to the your selected role page by clicking a card

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
  Scenario: User without access can see the header on the select your role page
    When I log in as a user with only roles that do not have access
    Then I cannot see the your selected role subheader
    And I can see the no access header
    And I can see the no access message
    And I can see the summary container
    And I cannot see the summary table body

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
  Scenario: User without access can expand the summary table to see the contents. Clicking again hides it
    Given I am logged in as a user with only roles that do not have access
    When I click on the summary expander
    Then I can see the summary table body
    And I can see the table body has a header row
    And I can see the no access table body has data
    When I click on the summary expander
    Then I can see the summary container
    And I cannot see the summary table body


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4645
  Scenario: User with a pre selected role sees their pre selected role
    Given I am logged in as a user with a pre selected role
    Then I can see the role that has been pre selected
