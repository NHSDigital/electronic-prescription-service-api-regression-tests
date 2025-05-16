@cpts_ui @search_results_too_many @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
Feature: Too many results warning is displayed when multiple patients are found

  Background:
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab Basic Details Search
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I enter first name "John"
    And I enter last name "Smith"
    And I enter date of birth "01" "01" "2000"
    And I enter postcode "LS6 1JL"
    And I click the Find a patient button
    And I am on the too many results page

  Scenario: I can see the user-submitted patient details
    # FIXME: This will need to be updated when the search pages are updated to use real data
    Then the details section shows first name "John"
    And the details section shows last name "Smith"
    And the details section shows date of birth "01-Jan-2000"
    And the details section shows postcode "LS6 1JL"
