@pfp_apigee @smoke @regression @bundle @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
Feature: I can see my prescriptions

  Scenario: I can see a single prescription
    Given I am an authorised prescriber
    And I successfully prepare and sign a prescription
    When I am authenticated
    And I request my prescriptions
    Then I can see my prescription
