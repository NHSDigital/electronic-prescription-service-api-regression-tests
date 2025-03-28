@eps_fhir @dispense @regression @blocker @smoke
Feature: I can dispense prescriptions

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3865
  Scenario: I can dispense a prescription
    Given a prescription has been created and released using apim apis
    When I dispense the prescription
    Then the response indicates a success
    And the response body indicates a successful dispense action

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3868
  Scenario: I can amend a single dispense notification
    Given a new prescription has been dispensed using apim apis
    When I amend the dispense notification
    Then the response indicates a success
    And the response body indicates a successful amend dispense action

  @withdraw
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3867
  Scenario: I can withdraw a dispense notification
    Given a new prescription has been dispensed using apim apis
    When I withdraw the dispense notification
    Then the response indicates a success
    And the response body indicates a successful dispense withdrawal action
