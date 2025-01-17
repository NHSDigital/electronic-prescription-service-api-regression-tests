@eps_fhir_prescribing @smoke @regression @ping @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4895
Feature: I can call the validator endpoint

  Scenario: I can call the validator endpoint with valid fhir with x-show-validation-warnings set to false
    Given I am an authorised prescriber
    When I make a request to the eps_fhir_prescribing validator endpoint
    Then the response indicates a success
    And the validator response has 1 information issue
