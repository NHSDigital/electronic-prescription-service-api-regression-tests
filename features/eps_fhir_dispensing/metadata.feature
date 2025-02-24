@eps_fhir_prescribing @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4896
Feature: I can retrieve metadata

  @metadata
  Scenario: I can retrieve metadata specification
    Given I am an authorised "api user" with EPS-FHIR-DISPENSING app
    When I make a request to the "eps_fhir_dispensing" metadata endpoint
    Then the response indicates a success
