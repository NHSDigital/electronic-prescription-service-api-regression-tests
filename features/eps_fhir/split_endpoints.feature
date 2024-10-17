@eps_fhir @smoke @regression @blocker @split_endpoints @create 
Feature: I can use split endpoints for prescribing and dispensing

  @prescribing
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/3847
  Scenario Outline: I can create, sign and release a prescription
    Given I am an authorised prescriber
    And I successfully prepare and sign a <Type> prescription using the prescribing endpoint
    When I am an authorised dispenser
    And I release the prescription
    Then the response indicates a success
    And the response body indicates a successful release action
    Examples:
      | Type          |
      | nominated     |
      | non-nominated |

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3865
  Scenario: I can dispense a prescription
    Given a prescription has been created and released with the prescribing endpoint
    When I dispense the prescription with the dispending endpoint
    Then the response indicates a success
    And the response body indicates a successful dispense action

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3868
  Scenario: I can amend a single dispense notification
    Given a new prescription has been dispensed
    When I amend the dispense notification
    Then the response indicates a success
    And the response body indicates a successful amend dispense action

  @withdraw
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3867
  Scenario: I can withdraw a dispense notification
    Given a new prescription has been dispensed
    When I withdraw the dispense notification
    Then the response indicates a success
    And the response body indicates a successful dispense withdrawal action

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/TICKET-NUMBER
  Scenario: I can still use the legacy endpoint during the transition phase
    Given I am an authorised user
    When I send a request to the legacy EPS FHIR API endpoint
    Then the response indicates a success
    And the response contains both prescribing and dispensing data
