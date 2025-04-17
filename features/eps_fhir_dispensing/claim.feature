@eps_fhir_dispensing @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can dispense prescriptions

  @claim
  Scenario: I can claim for a prescription
    Given a new prescription has been dispensed using proxygen apis
    When I claim for the prescription
    Then the response indicates a success
    And the response body indicates a successful claim
