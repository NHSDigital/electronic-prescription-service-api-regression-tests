@cpts_ui @change_role @single_access @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Users are able to change their roles, if they have one role with access.

  Background:
    Given I am logged in with a single access role

  ############################################################################
  # Successfully changing role scenarios
  ############################################################################
  Scenario: User is automatically redirected to the 'search for a prescription' page
    When I click the change role header link
    Then I am on the search for a prescription page
