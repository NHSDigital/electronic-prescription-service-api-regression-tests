@cpts_fhir @smoke @regression @ping @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4945
Feature: I can ping the API

  Scenario: I can ping the API
    When I make a request to the "cpts_fhir" ping endpoint
    Then the response indicates a success
    And I can see the ping information in the response
