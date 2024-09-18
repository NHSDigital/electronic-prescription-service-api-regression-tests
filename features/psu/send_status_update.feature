@psu @regression
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
Feature: I can send an update to PSU

  @blocker @smoke
  Scenario: I can send an update to PSU
    Given I am authorised to send prescription updates
    When I send an Collected update with a terminal status of completed
    Then the response indicates a record was created

  @e2e
  Scenario: I can send and confirm an update to a prescription
    Given a prescription has been created and released
    When I am authorised to send prescription updates
    And I send an Collected update with a terminal status of completed
    Then The prescription item has a status of Collected with a terminal status of completed
