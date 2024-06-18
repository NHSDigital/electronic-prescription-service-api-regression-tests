@eps_fhir @dispense @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3865
Feature: I can create and then dispense prescriptions

  Scenario: I can create and then dispense a prescription
    Given I am an authorised prescriber
    And I successfully prepare and sign a non-nominated prescription
    When I am an authorised dispenser
    And I release a prescription
    And I dispense a prescription
    Then the response indicates a success
    And the response body indicates a successful dispense action
