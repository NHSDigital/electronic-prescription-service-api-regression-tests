@eps_fhir @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3847
Feature: I can create prescriptions

  @skip-sandbox
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4941
  Scenario Outline: I can create, sign and release a prescription
    Given I am an authorised prescriber with <App> app
    And I successfully prepare and sign a <Nomination> <Type> prescription
    When I am an authorised dispenser with EPS-FHIR app
    And I release the prescription
    Then the response indicates a success
    And the response body indicates a successful release action
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

  @skip-sandbox
  Scenario: I can create a prescription with sha256
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare a nominated acute prescription
    Then the signing algorithm is RS256

  @skip-sandbox
  Scenario: I can create a prescription with sha1
    Given I am an authorised prescriber with EPS-FHIR-SHA1 app
    And I successfully prepare a nominated acute prescription
    Then the signing algorithm is RS1
