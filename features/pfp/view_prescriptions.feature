@pfp_apigee @pfp_aws @regression
Feature: I can see my prescriptions

  @blocker @smoke @e2e @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
  Scenario: I can see a single prescription
    Given I am an authorised prescriber
    And I successfully prepare and sign a prescription
    When I am authenticated
    And I request my prescriptions
    Then I can see my prescription
