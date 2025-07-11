@eps_fhir_prescribing @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4941
Feature: I can create prescriptions

  Scenario Outline: I can create, sign and release a prescription
    Given I am an authorised prescriber with <App> app
    And I successfully prepare and sign a <Nomination> <Type> prescription
    When I am an authorised dispenser with EPS-FHIR-DISPENSING app
    And I release the prescription
    Then the response indicates a success
    And the response body indicates a successful release action
    Examples:
      | App                       | Nomination    | Type   |
      | EPS-FHIR-PRESCRIBING      | nominated     | acute  |
      | EPS-FHIR-PRESCRIBING      | non-nominated | acute  |
      | EPS-FHIR-PRESCRIBING      | nominated     | repeat |
      | EPS-FHIR-PRESCRIBING      | non-nominated | repeat |
      | EPS-FHIR-PRESCRIBING      | nominated     | eRD |
      | EPS-FHIR-PRESCRIBING      | non-nominated | eRD |
      | EPS-FHIR-PRESCRIBING-SHA1 | nominated     | acute  |
      | EPS-FHIR-PRESCRIBING-SHA1 | non-nominated | acute  |
      | EPS-FHIR-PRESCRIBING-SHA1 | nominated     | repeat |
      | EPS-FHIR-PRESCRIBING-SHA1 | non-nominated | repeat |
      | EPS-FHIR-PRESCRIBING-SHA1 | nominated     | eRD |
      | EPS-FHIR-PRESCRIBING-SHA1 | non-nominated | eRD |


  @skip-sandbox
  Scenario: I can create a prescription with sha256
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare a nominated acute prescription
    Then the signing algorithm is RS256

  @skip-sandbox
  Scenario: I can create a prescription with sha1
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING-SHA1 app
    And I successfully prepare a nominated acute prescription
    Then the signing algorithm is RS1
