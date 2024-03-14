@eps_fhir
@smoke @regression @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3847
Feature: I can can create prescriptions using the EPS FHIR API

  Scenario: I can prepare a nominated prescription
    Given I am authenticated
    When I make a request to the "eps_fhir" ping endpoint
    Then I get a 200 response code
    And I can see the ping information in the response
