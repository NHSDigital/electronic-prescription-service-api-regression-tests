@eps_fhir @smoke @regression @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3866
Feature: I can return prescriptions

  Scenario: I can return a prescription
    Given a prescription has been created and released
    When I am an authorised dispenser
    And I return the prescription
    Then the response indicates a success
    And I can see an informational operation outcome in the response
