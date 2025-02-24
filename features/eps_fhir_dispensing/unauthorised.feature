@eps_fhir_prescribing @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can not call api when unauthorised

  @skip-sandbox
  Scenario: I can not call prepare endpoint when using api key
    Given I am an authorised "api user" with EPS-FHIR-DISPENSING app
    When I try to prepare a nominated prescription
    Then the response indicates unauthorised

  @skip-sandbox
  Scenario: I can not call release endpoint when using api key
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a nominated prescription
    Given I am an authorised "api user" with EPS-FHIR-DISPENSING app
    When I try to release then prescription
    Then the response indicates unauthorised
