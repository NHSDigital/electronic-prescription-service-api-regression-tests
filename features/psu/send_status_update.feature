@psu @regression
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
Feature: I can send an update to PSU

  @blocker @smoke
  Scenario: I can send an update to PSU
    Given I am authorised to send prescription updates
    When I send a Ready to Collect update
    Then the response indicates a record was created
    And the prescription item has a status of Ready to Collect with a terminal status of in-progress
    When I send a Collected update with a terminal status of completed
    Then the response indicates a record was created
    And the prescription item has a status of Collected with a terminal status of completed

  @skip @e2e
  Scenario: I can send and confirm an update to a prescription
    Given a prescription has been created and released using apim apis
    When I am authorised to send prescription updates
    And I send a Collected update with a terminal status of completed
    Then The prescription item has a status of Collected with a terminal status of completed
