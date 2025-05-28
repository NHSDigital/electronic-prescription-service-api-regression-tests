@pfp_apigee @pfp_aws
Feature: I can see my prescriptions

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3398
  Scenario: I can get my prescriptions
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare and sign a prescription
    When I get my prescriptions
    Then I can see my prescriptions
