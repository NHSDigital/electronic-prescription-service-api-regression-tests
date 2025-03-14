@cpts_fhir @smoke @regression @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
Feature: Users are able to get prescriptions from CPTS-FHIR

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
  @get_prescription
  Scenario: I can see the prescription details when searching by prescription id
    Given I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details
    Then the response indicates a success
    And I can see the prescription details

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4930
  @get_prescription
  Scenario: I can see the prescription not found message when searching for a prescription id that does not exist
    Given I am an authorised prescriber with CPTS-FHIR app
    When I request the prescription details with a non-existent prescription id
    Then the response indicates not found resource
    And I can see the prescription not found message
