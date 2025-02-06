@cpts_ui @change_role @regression @blocker @smoke @ui
Feature: Users are able to change their roles, if they have multiple roles with access.


  ############################################################################
  # Successfully changing role scenarios
  ############################################################################
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can change their role
    Given I am logged in as a user with multiple access roles
    And I am on the change your role page
    When I click a change role role card
    Then I am on the 'your selected role' page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can see roles with access cards
    Given I am logged in as a user with multiple access roles
    And I am on the change your role page
    Then I see the change role roles with access cards
    And I can see multiple change role roles with access cards

  ############################################################################
  # Expanding/collapsing the summary
  ############################################################################

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: Change role roles without access table body is not visible by default
    Given I am logged in as a user with multiple access roles
    And I am on the change your role page
    Then the change role roles without access table body is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can expand the change role 'Roles without access' to see table contents
    Given I am logged in as a user with multiple access roles
    And I am on the change your role page
    When I click on the change role summary expander
    Then I see the change role roles without access table

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can collapse the change role 'Roles without access' to hide table contents
    Given I am logged in as a user with multiple access roles
    And I am on the change your role page
    And the summary table body is displayed
    When I click on the change role summary expander
    Then The change role roles without access table body is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @single_access
  Scenario: User is automatically redirected to the 'search for a prescription' page
    Given I am logged in as a user with a single access role
    Then I am on the search for a prescription page
    And I do not see the "Change Role" link

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @single_access
  Scenario: User does not have the change role link in the header
    Given I am logged in as a user with a single access role
    Then I do not see the change role page header link

  Scenario: user can change their role, and see a confirmation page
    Given I am logged in as a user with multiple access roles
    And I am on the change your role page
    When I click a change role role card
    Then I see the 'your selected role' page
    And I can see the RBAC banner
