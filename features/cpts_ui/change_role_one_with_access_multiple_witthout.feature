@cpts_ui @change_role @single_access_multiple_without @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4974
Feature: Users are able to change their roles, if they have one role with access and multiple roles without access.

  Background:
    Given I am logged in with a single access role and multiple without access

  ############################################################################
  # Successfully changing role scenarios
  ############################################################################
  Scenario: User can change their role
    When I click a change role role card
    Then I am on the 'your selected role' page

  Scenario: User can see roles with access cards
    Then I see the change role roles with access cards
    And I can see one change role roles with access card

  ############################################################################
  # Expanding/collapsing the summary
  ############################################################################

  Scenario: Change role roles without access table body is not visible by default
    Then the change role roles without access table body is not visible

  Scenario: User can expand the change role 'Roles without access' to see table contents
    When I click on the change role summary expander
    Then I see the change role roles without access table

  Scenario: User can collapse the change role 'Roles without access' to hide table contents
    Given the summary table body is displayed
    When I click on the change role summary expander
    Then The change role roles without access table body is not visible
