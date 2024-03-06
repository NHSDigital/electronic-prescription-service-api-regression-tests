@eps_fhir
@smoke @regression @ping @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3563
Feature: I can ping the EPS FHIR API

  Scenario: I can ping the API
    When I make a request to the "eps_fhir" ping endpoint
    Then I get a 200 response code
    And I can see the ping information in the response
