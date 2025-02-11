@eps_fhir @cancel @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3869
Feature: I can cancel prescriptions

  Scenario: I can cancel a prescription
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare and sign a non-nominated prescription
    When I cancel all line items on the prescription
    Then the response indicates a success
    And the response body indicates a successful cancel action
