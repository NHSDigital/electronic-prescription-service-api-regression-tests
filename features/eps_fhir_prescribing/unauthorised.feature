@eps_fhir_prescribing @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can not call api when unauthorised

  @skip-sandbox
  Scenario: I can not call prepare endpoint when using api key
    Given I am an authorised api user with EPS-FHIR-PRESCRIBING app
    When I try to prepare a nominated prescription
    Then the response indicates unauthorised
