@cpts_ui @change_role @no_access @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Users are able to change their roles, if they have no role with access.

  Background:
    Given I am on the change role page with no role with access

  ############################################################################
  # Unable to change role
  ############################################################################
  Scenario: User sees the 'No role with access' warning
    Then I see the change role page 'no role with access' warning message

  ############################################################################
  # Expanding/collapsing the summary
  ############################################################################
  Scenario: User can expand the change role 'Roles without access' to see table contents
    When I click on the change role 'Roles without access' expander
    Then I see the summary table body with a header row and data

  Scenario: User can collapse the change role 'Roles without access' to hide table contents
    Given the change role 'Roles without access' table body is displayed
    When I click on the change role 'Roles without access' expander
    Then the change role 'Roles without access' table body is not visible
