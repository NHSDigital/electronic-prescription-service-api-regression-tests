@eps_fhir @dispense @regression @blocker @smoke
Feature: I can create and then dispense prescriptions

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3865
  Scenario: I can create and then dispense a prescription
    Given a prescription has been created and released
    When I dispense a prescription
    Then the response indicates a success
    And the response body indicates a successful dispense action

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3867
  Scenario: I withdraw a dispense notification
    Given a new prescription has been dispensed
    When I withdraw the dispense notification
    Then the response indicates a success
    And the response body indicates a successful dispense withdrawal action
