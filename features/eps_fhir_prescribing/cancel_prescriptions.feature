@eps_fhir_prescribing @cancel @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can cancel prescriptions

  Scenario Outline: I can cancel a prescription
    Given I am an authorised prescriber with <App> app
    And I successfully prepare and sign a <Nomination> <Type> prescription
    When I cancel all line items on the prescription
    Then the response indicates a success
    And the response body indicates a successful cancel action
    Examples:
      | App                       | Nomination    | Type   |
      | EPS-FHIR-PRESCRIBING      | nominated     | acute  |
      | EPS-FHIR-PRESCRIBING      | non-nominated | acute  |
      | EPS-FHIR-PRESCRIBING      | nominated     | repeat |
      | EPS-FHIR-PRESCRIBING      | non-nominated | repeat |
      | EPS-FHIR-PRESCRIBING-SHA1 | nominated     | acute  |
      | EPS-FHIR-PRESCRIBING-SHA1 | non-nominated | acute  |
      | EPS-FHIR-PRESCRIBING-SHA1 | nominated     | repeat |
      | EPS-FHIR-PRESCRIBING-SHA1 | non-nominated | repeat |
