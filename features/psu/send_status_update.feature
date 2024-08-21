@psu @regression
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
Feature: I can send an update to PSU

  @blocker @smoke
  Scenario: I can send an update to PSU
    Given I am authorised to send prescription updates
    And I send an update
    Then the response body indicates a successful status update action
