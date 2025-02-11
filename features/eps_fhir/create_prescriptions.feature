@eps_fhir @smoke @regression @blocker @create
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3847
Feature: I can create prescriptions

  Scenario Outline: I can create, sign and release a prescription
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare and sign a <Type> prescription
    When I am an authorised dispenser with EPS-FHIR app
    And I release the prescription
    Then the response indicates a success
    And the response body indicates a successful release action
    Examples:
      | Type          |
      | nominated     |
      | non-nominated |

  Scenario: I can create a prescription with sha256
    Given I am an authorised prescriber with EPS-FHIR app
    And I successfully prepare a nominated prescription
    Then the signing algorithm is RS256

  Scenario: I can create a prescription with sha1
    Given I am an authorised prescriber with EPS-FHIR-SHA1 app
    And I successfully prepare a nominated prescription
    Then the signing algorithm is RS1
