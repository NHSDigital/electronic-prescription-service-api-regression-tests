@cpts_fhir @smoke @regression @blocker
Feature: Users are able to get patients from CPTS-FHIR

    @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4754
    @search_for_patients
    Scenario Outline: I can search for a list of patients
        Given I am an authorised prescriber with CPTS-FHIR app
        When I request the list of patients using the <Identifier>
        Then the response indicates a success
        And I can see the list of patients
