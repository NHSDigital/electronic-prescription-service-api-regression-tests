@cpts_ui @change_role @single_access @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
Feature: Users are able to change their roles, if they have one role with access.

  Background:
    Given I am logged in with a single access role

  
  Scenario: User is automatically redirected to the 'search for a prescription' page
    When I navigate to the change your role page
    Then I am on the search for a prescription page

  Scenario: User does not have the change role link in the header
    Then I do not see the change role page header link
