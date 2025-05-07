@cpts_ui @change_role @regression @blocker @smoke @ui
Feature: Users are able to change their roles, if they have multiple roles with access.


  ############################################################################
  # Successfully changing role scenarios
  ############################################################################
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can change their role
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the change your role page
    When I click a change role role card
    Then I am on the 'your selected role' page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can see roles with access cards
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
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
    And I have confirmed a role
    And I am on the change your role page
    Then the change role roles without access table body is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can expand the change role 'Roles without access' to see table contents
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the change your role page
    When I click on the change role summary expander
    Then I see the change role roles without access table

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: User can collapse the change role 'Roles without access' to hide table contents
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the change your role page
    And the summary table body is displayed
    When I click on the change role summary expander
    Then The change role roles without access table body is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @single_access
  Scenario: User is automatically redirected to the 'search for a prescription' page and sees the expected links
    When I log in as a user with a single access role
    Then I am on the search for a prescription page
    And I do not see the "Change Role" link
    And I do not see the change role page header link

  Scenario: user can change their role, and see a confirmation page
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the change your role page
    When I click a change role role card
    Then I see the 'your selected role' page
    And I can see the RBAC banner

  ############################################################################
  # Successfully changing role scenarios
  ############################################################################

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4974
  Scenario: User can change their role and see the correct message on the change role page
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the change your role page
    And I click a change role role card
    When I click the change link next to the role text
    Then I am on the change role page
    And I can see the role that has been pre selected

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5046
  Scenario: User refreshes the page and retains roles with access
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the change your role page
    When I click a change role role card
    And I click the change link next to the role text
    And I refresh the page
    Then I do not see the change role page header link

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4974
  Scenario: User can see roles with access cards
    Given I am logged in with a single access role and multiple without access
    Then I see the change role roles with access cards
    And I can see one change role roles with access card

  ############################################################################
  # Expanding/collapsing the summary
  ############################################################################
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4974
  Scenario: Change role roles without access table body is not visible by default
    When I log in as a user with multiple access roles
    Then the change role roles without access table body is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4974
  Scenario: User can expand the change role 'Roles without access' to see table contents
    Given I am logged in as a user with multiple access roles
    When I click on the change role summary expander
    Then I see the change role roles without access table

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4974
  Scenario: User can collapse the change role 'Roles without access' to hide table contents
    Given I am logged in as a user with multiple access roles
    And the summary table body is displayed
    When I click on the change role summary expander
    Then The change role roles without access table body is not visible
