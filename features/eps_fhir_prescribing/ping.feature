@eps_fhir_prescribing @smoke @regression @ping @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3563
Feature: I can ping the API

  Scenario: I can ping the API
    When I make a request to the "eps_fhir_prescribing" ping endpoint
    Then the response indicates a success
    And I can see the ping information in the response
