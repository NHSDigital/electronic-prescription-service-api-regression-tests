@eps_fhir @smoke @regression @blocker @return
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3866
Feature: I can return prescriptions

  Scenario: I can return a prescription
    Given a prescription has been created and released
    When I return the prescription
    Then the response indicates a success
    And the response body indicates a successful return action
