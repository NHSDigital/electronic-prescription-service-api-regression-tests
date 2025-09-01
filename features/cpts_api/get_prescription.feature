@cpts_fhir @smoke @regression @blocker
Feature: Users are able to get prescriptions from CPTS-FHIR

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
  @get_prescription
  Scenario: I can see the prescription details when searching by prescription id
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a prescription
    And I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details
    Then the response indicates a success
    And I can see the prescription details

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
   @get_prescription
   Scenario: I can see the prescription details of the correct issue when searching by prescription id and issue number
   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
   And I successfully prepare and sign a nominated eRD prescription
   And I am an authorised prescriber with CPTS-FHIR app
   When I request the prescription details with an issue number
   Then the response indicates a success
   And I can see the prescription details with the correct issue details

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
  @get_prescription
  Scenario: I can see the prescription not found message when searching for a prescription id that does not exist
    Given I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details with a non-existent prescription id
    Then the response indicates not found resource
    And I can see the prescription not found message

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
  @get_prescription
  Scenario: I can see the missing required path parameter when prescription id is not provided
    Given I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details without a path parameter
    Then the response indicates a bad request
    And I can see the missing required path parameter message

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5616
  @get_prescription
  Scenario: I can see the non-dispensing reason when searching for a prescription that has a non-dispensed line item
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a prescription
    And I release the prescription
    And I non-dispense a line item with a "Clinically unsuitable" reason
    And I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details
    Then the response indicates a success
    And I can see the prescription details with the correct "Clinically unsuitable" non-dispensing reason

@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5616
  @get_prescription
  Scenario: I can see the cancellation reason when searching for a prescription that has a cancelled line item
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a prescription
    And I cancel all line items on the prescription with a "Clinical grounds" reason
    And I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details
    Then the response indicates a success
    And I can see the prescription details with the correct "Clinical grounds" cancellation reason
