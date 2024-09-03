@psu @regression
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
Feature: I can send an update to PSU

  @blocker @smoke
  Scenario: I can send an update to PSU
    Given I am authorised to send prescription updates
    When I send an Collected update with a terminal status of completed
    Then the response indicates a record was created
