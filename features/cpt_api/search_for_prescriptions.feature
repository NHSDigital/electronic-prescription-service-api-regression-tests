@cpts_fhir @smoke @regression @blocker
Feature: Users are able to get prescriptions from CPTS-FHIR

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4929
  @search_for_prescriptions
  Scenario Outline: I can search for a list of prescriptions
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare and sign a prescription
    And I am an authorised prescriber with CPTS-API app
    When I request the list of prescriptions using the <Identifier>
    Then the response indicates a success
    And I can see the list of prescriptions
    Examples:
      | Identifier      |
      | NHS Number      |
      | Prescription ID |
