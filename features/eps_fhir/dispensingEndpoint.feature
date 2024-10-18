@eps_fhir @smoke @regression @blocker @eps_prescribing_dispensing @create @dispensing
Feature: I can use the dispensing endpoint

@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3865
Scenario: I can dispense a prescription
Given a prescription has been created and released with the prescribing endpoint
When I dispense the prescription with the dispensing endpoint
Then the response indicates a success
And the response body indicates a successful dispense action
