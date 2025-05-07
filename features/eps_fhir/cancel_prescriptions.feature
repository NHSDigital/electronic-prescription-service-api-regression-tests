@eps_fhir @cancel @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3869
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4941
Feature: I can cancel prescriptions

  @skip-sandbox
  Scenario Outline: I can cancel a prescription
    Given I am an authorised prescriber with <App> app
    And I successfully prepare and sign a <Nomination> <Type> prescription
    When I cancel all line items on the prescription
    Then the response indicates a success
    And the response body indicates a successful cancel action
    Examples:
      | App           | Nomination    | Type   |
      | EPS-FHIR      | nominated     | acute  |
      | EPS-FHIR      | non-nominated | acute  |
      | EPS-FHIR      | nominated     | eRD    |
      | EPS-FHIR      | non-nominated | eRD    |
      | EPS-FHIR      | nominated     | repeat |
      | EPS-FHIR      | non-nominated | repeat |
      | EPS-FHIR-SHA1 | nominated     | acute  |
      | EPS-FHIR-SHA1 | non-nominated | acute  |
      | EPS-FHIR-SHA1 | nominated     | eRD    |
      | EPS-FHIR-SHA1 | non-nominated | eRD    |
      | EPS-FHIR-SHA1 | nominated     | repeat |
      | EPS-FHIR-SHA1 | non-nominated | repeat |
