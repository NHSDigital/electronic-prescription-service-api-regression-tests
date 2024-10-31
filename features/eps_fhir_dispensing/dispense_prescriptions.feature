@eps_fhir_dispensing @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can dispense prescriptions

  @dispense
  Scenario: I can dispense a prescription
    Given a prescription has been created and released
    When I dispense the prescription
    Then the response indicates a success
    And the response body indicates a successful dispense action

  @amend
  Scenario: I can amend a single dispense notification
    Given a new prescription has been dispensed
    When I amend the dispense notification
    Then the response indicates a success
    And the response body indicates a successful amend dispense action

  @withdraw
  Scenario: I can withdraw a dispense notification
    Given a new prescription has been dispensed
    When I withdraw the dispense notification
    Then the response indicates a success
    And the response body indicates a successful dispense withdrawal action
