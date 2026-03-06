@eps_fhir_dispensing @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4432
Feature: I can dispense prescriptions

  @dispense
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4941
  Scenario Outline: I can dispense a prescription
    Given a <Nomination> <Type> prescription has been created and released using proxygen apis
    When I dispense the prescription
    Then the response indicates a success
    And the response body indicates a successful dispense action
    Examples:
      | Nomination    | Type   |
      | nominated     | acute  |
      | non-nominated | acute  |
      | nominated     | repeat |
      | non-nominated | repeat |
      | nominated     | eRD    |
      | non-nominated | eRD    |

  @dispense @application-restricted
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-6097
  Scenario: I can release a prescription using application-restricted signed JWT session
    # Just the one is suffucicient to confirn that JWT is working, I reckon
    Given a nominated acute prescription has been created using proxygen apis
    And I am an authorised dispenser with EPS-FHIR-DISPENSING-JWT app
    When I release the prescription
    Then the response indicates a success
    And the response body indicates a successful release action

  @amend
  Scenario: I can amend a single dispense notification
    Given a new prescription has been dispensed using proxygen apis
    When I amend the dispense notification
    Then the response indicates a success
    And the response body indicates a successful amend dispense action

  @withdraw
  Scenario: I can withdraw a dispense notification
    Given a new prescription has been dispensed using proxygen apis
    When I withdraw the dispense notification
    Then the response indicates a success
    And the response body indicates a successful dispense withdrawal action
