@cpts_ui @search_results_too_many @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5361
Feature: Too many results warning is displayed when multiple patients are found

  Scenario: User sees too many results messages when multiple patients are found
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search using basic details: "<empty>" "Jones" "16" "07" "1985" "<empty>"
    Then I am on the too many results page
    And the too many results page should display all required messages
