@cpts_ui @change_role @no_access @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Users are able to change their roles, if they have no role with access.

  Background:
    Given I am logged in without access

  ############################################################################
  # Unable to change role
  ############################################################################
  Scenario: User sees the 'No role with access' warning
    Then I see the change role page 'no role with access' warning message
    And I cannot see any change role roles with access cards

  ############################################################################
  # Expanding/collapsing the summary
  ############################################################################
  Scenario: User can expand the change role 'Roles without access' to see table contents
    When I click on the change role summary expander
    Then I see the change role roles without access table

  Scenario: User can collapse the change role 'Roles without access' to hide table contents
    Given the summary table body is displayed
    When I click on the change role summary expander
    Then the change role roles without access table body is not visible
