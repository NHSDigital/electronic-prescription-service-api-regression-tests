@eps_fhir @dispense @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3865
Feature: I can create and then dispense prescriptions

  Scenario: I can create and then dispense a prescription
    Given a prescription has been created and released
    When I dispense a prescription
    Then the response indicates a success
    And the response body indicates a successful dispense action


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3868
  Scenario: I can amend a single dispense notification
    Given a new prescription has been dispensed
    When I amend the dispense notification
    Then the response indicates a success
    And the response body indicates a successful amend dispense action