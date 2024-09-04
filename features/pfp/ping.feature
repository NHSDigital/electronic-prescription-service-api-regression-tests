@pfp_apigee @pfp_aws @regression
Feature: I can ping the API

  @ping @blocker @smoke @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3822
  Scenario: I can ping the API
    When I make a request to the "pfp_apigee" ping endpoint
    Then the response indicates a success
    And I can see the ping information in the response
