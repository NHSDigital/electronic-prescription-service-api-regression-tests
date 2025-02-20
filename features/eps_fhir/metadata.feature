@eps_fhir @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4896
Feature: I can retrieve metadata

  @metadata
  Scenario: I can retrieve metadata specification
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a request to the "eps_fhir" metadata endpoint
    Then the response indicates a success
