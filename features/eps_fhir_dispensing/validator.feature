@eps_fhir_dispensing @smoke @regression @validator
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4895
Feature: I can call the validator endpoint

  Scenario: I can call the validator endpoint with valid fhir with x-show-validation-warnings set to false
    Given I am an authorised dispenser
    When I make a valid request to the eps_fhir validator endpoint with show validation set to false
    Then the response indicates a success
    And the validator response has 1 information issue

  Scenario: I can call the validator endpoint with valid fhir with x-show-validation-warnings set to true
    Given I am an authorised dispenser
    When I make a valid request to the eps_fhir validator endpoint with show validation set to true
    Then the response indicates a success
    And the validator response has many information issue
    And the validator response has 0 error issue

  Scenario: I can call the validator endpoint with invalid fhir
    Given I am an authorised dispenser
    When I make a invalid request to the eps_fhir validator endpoint with show validation set to false
    Then the response indicates a bad request
    And the validator response has many error issue
    And the validator response has error with diagnostic containing "HAPI-1861"
