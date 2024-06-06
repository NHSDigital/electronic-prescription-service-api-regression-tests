@eps_fhir
@smoke @regression @blocker
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3847
Feature: I can can create prescriptions using the EPS FHIR API

  Scenario Outline: I can create, sign and release a prescription
    Given I am an authorised prescriber
    And I successfully prepare and sign a <Type> prescription
    When I am an authorised dispenser
    And I release a prescription
    Then the response indicates a success
    Then the response body indicates a successful prescribe action
    Examples:
      | Type          |
      | nominated     |
      | non-nominated |
