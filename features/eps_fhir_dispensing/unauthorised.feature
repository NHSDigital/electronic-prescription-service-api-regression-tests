@eps_fhir_dispensing @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can not call api when unauthorised

  @skip-sandbox
  Scenario: I can not call prepare endpoint when using api key
    Given I am an authorised api user with EPS-FHIR-DISPENSING app
    When I try to prepare a nominated acute prescription
    Then the response indicates unauthorised

  @skip-sandbox
  Scenario: I can not call release endpoint when using api key
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a nominated acute prescription
    And I am an authorised api user with EPS-FHIR-DISPENSING app
    When I try to release the prescription
    Then the response indicates unauthorised
