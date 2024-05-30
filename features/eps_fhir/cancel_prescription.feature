@phil
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3869
Feature: I can can create and then cancel prescriptions, using the EPS FHIR API

  Scenario Outline: I can create and then cancel a prescription
    Given I am an authorised prescriber
    And I successfully prepare and sign a <Type> prescription
    When I cancel all line items on the prescription
    Then the response indicates success
    Examples:
      | Type          |
      | non-nominated |
