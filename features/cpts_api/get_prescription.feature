@cpts_fhir @smoke @regression @blocker
Feature: Users are able to get prescriptions from CPTS-FHIR

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
  @get_prescription
  Scenario: I can see the prescription details when searching by prescription id
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare and sign a prescription
    And I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details
    Then the response indicates a success
    And I can see the prescription details

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
   @get_prescription
   Scenario: I can see the prescription details of the correct issue when searching by prescription id and issue number
   Given I am an authorised prescriber with EPS-FHIR app
   And I successfully prepare and sign a nominated eRD  prescription
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
