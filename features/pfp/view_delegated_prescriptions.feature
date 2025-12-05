@pfp_apigee @pfp_aws @regression
Feature: I can see my prescriptions

  @tim @blocker @smoke @e2e @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
  Scenario: I can see a single delegated prescription
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a prescription
    When I am authenticated with PFP-APIGEE app
    And I request prescriptions of the user I have delegated access to
    Then I can see the delegated prescription
