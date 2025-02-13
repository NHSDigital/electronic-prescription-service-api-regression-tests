@eps_fhir @smoke @regression @blocker @validator
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4895
@allure.tms:https://jsondiff.tooliverse.io/
Feature: I can call the validator endpoint

  Scenario: I can call the validator endpoint with valid fhir with x-show-validation-warnings set to false
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a valid request to the eps_fhir validator endpoint with show validation set to false
    Then the response indicates a success
    And the validator response has 1 information issue

  Scenario: I can call the validator endpoint with valid fhir with x-show-validation-warnings set to true
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a valid request to the eps_fhir validator endpoint with show validation set to true
    Then the response indicates a bad request
    And the validator response has many information issue
    And the validator response has 0 error issue

  Scenario: I can call the validator endpoint with valid fhir with x-show-validation-warnings set to unset
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a valid request to the eps_fhir validator endpoint with show validation set to unset
    Then the response indicates a success
    And the validator response has 1 information issue

  Scenario: I can call the validator endpoint with invalid fhir
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a invalid request to the eps_fhir validator endpoint with show validation set to false
    Then the response indicates a bad request
    And the validator response has many error issue
    And the validator response has error with diagnostic containing Failed to parse JSON encoded FHIR content

  Scenario: I can call the validator endpoint with missing dosage instructions message
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a request with file missing_dosage_instructions/request.json to the eps_fhir validator endpoint
    Then the response indicates a bad request
    And the validator response matches missing_dosage_instructions/response.json

  Scenario: I can call the validator endpoint with missing dispense request quantity message
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a request with file missing_dispense_request_quantity/request.json to the eps_fhir validator endpoint
    Then the response indicates a bad request
    And the validator response matches missing_dispense_request_quantity/response.json

  Scenario: I can call the validator endpoint with missing medication message
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a request with file missing_medication/request.json to the eps_fhir validator endpoint
    Then the response indicates a bad request
    And the validator response matches missing_medication/response.json

  Scenario: I can call the validator endpoint with too many medication requests message
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a request with file too_many_medication_requests/request.json to the eps_fhir validator endpoint
    Then the response indicates a bad request
    And the validator response matches too_many_medication_requests/response.json

  Scenario: I can call the validator endpoint with unknown endorsement message
    Given I am an authorised prescriber with EPS-FHIR app
    When I make a request with file unknown_endorsement/request.json to the eps_fhir validator endpoint
    Then the response indicates a bad request
    And the validator response matches unknown_endorsement/response.json
