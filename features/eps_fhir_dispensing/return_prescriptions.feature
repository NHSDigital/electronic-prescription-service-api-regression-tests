@eps_fhir_dispensing @smoke @regression @blocker @return
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can return prescriptions

  Scenario: I can return a prescription
    Given a prescription has been created and released using proxygen apis
    When I return the prescription
    Then the response indicates a success
    And the response body indicates a successful return action
