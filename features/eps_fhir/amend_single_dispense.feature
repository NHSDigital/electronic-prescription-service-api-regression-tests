@eps_fhir @dispense @regression @blocker @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3868
Feature: I can amend a single dispense notification

Scenario Outline: I can amend a single dispense notification
    Given I am an authorised dispenser
    When I amend a dispense notification
    Then the amended notification is successfully sent. 