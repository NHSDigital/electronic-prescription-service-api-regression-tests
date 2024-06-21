@eps_fhir @dispense @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3868
Feature: I can amend a single dispense notification

Scenario Outline: I can amend a single dispense notification
    Given a new prescription has dispensed
    When I amend the dispense notification
    Then the response indicates a success
    And the response body indicates a successful amend dispense action