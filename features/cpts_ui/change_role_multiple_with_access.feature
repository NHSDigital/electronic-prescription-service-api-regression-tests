@cpts_ui @change_role @multiple_access @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Users are able to change their roles, if they have multiple roles with access.

  Background:
    Given I am on the change role page with multiple roles with access

  ############################################################################
  # Successfully changing role scenarios
  ############################################################################
  Scenario: User can change their role
    When I click on a new role
    Then I am redirected to the role selected page

  Scenario: Summary table body is not visible by default
    Then the summary table body is not visible

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

  ############################################################################
  # Viewing roles & navigation
  ############################################################################
  Scenario: User can see change role page roles with access cards
    Then I see the roles with access cards on the change role page

  Scenario: User can navigate to the 'your selected role' page by clicking a card
    When I click a role card
    Then I am on the 'your selected role' page
