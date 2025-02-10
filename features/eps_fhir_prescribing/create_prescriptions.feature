@eps_fhir_prescribing @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can create prescriptions

  Scenario Outline: I can create, sign and release a prescription
    Given I am an authorised prescriber on EPS-FHIR-PRESCRIBING
    And I successfully prepare and sign a <Type> prescription
    When I am an authorised dispenser on EPS-FHIR-DISPENSING
    And I release the prescription
    Then the response indicates a success
    And the response body indicates a successful release action
    Examples:
      | Type          |
      | nominated     |
      | non-nominated |
