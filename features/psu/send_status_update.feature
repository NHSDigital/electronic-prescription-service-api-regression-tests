@psu @regression
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
Feature: I can send an update to PSU

  @blocker @smoke
  Scenario: I can send a 'With Pharmacy' update to PSU
    Given I am authorised to send prescription updates
    When I send a 'With Pharmacy' update
    Then the prescription item has a coding of 'With Pharmacy' with a status of 'in-progress'

  @blocker @smoke
  Scenario: I can send 'With Pharmacy' then 'Ready to Collect' updates to PSU
    Given I am authorised to send prescription updates
    When I send a 'With Pharmacy' update
    And I send a 'Ready to Collect' update
    Then the prescription item has a coding of 'Ready to Collect' with a status of 'in-progress'

  @blocker @smoke
  Scenario: I can send 'With Pharmacy' then 'Collected' updates to PSU
    Given I am authorised to send prescription updates
    When I send a 'With Pharmacy' update
    And I send a 'Collected' update with a status of 'completed'
    Then the prescription item has a coding of 'Collected' with a status of 'completed'

  @blocker @smoke @e2e
  Scenario: I can see a single prescription with its updates
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And a nominated acute prescription has been created and released to FA090
    And status updates are enabled
    And I am authorised to send prescription updates
    When I send a 'Collected' update with a status of 'completed'
    And I am authenticated with PFP-APIGEE app
    And I request my prescriptions
    Then I can see my prescription and it has a status of 'completed'
