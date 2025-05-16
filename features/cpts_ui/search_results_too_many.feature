@cpts_ui @search_results_too_many @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
Feature: Too many results warning is displayed when multiple patients are found

  Background:
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search using basic details: "John" "Smith" "01" "01" "2000" "LS6 1JL"
    Then I am on the too many results page

  Scenario: User-submitted patient details are displayed
    # FIXME: This will need to be updated when the search pages are updated to use real data
    Then the details section shows:
      | Heading     | Value        |
      | First name  | John         |
      | Last name   | Smith        |
      | DOB         | 01-Jan-2000  |
      | Postcode    | LS6 1JL      |
