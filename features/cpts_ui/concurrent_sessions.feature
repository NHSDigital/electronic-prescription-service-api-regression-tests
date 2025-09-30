@cpts_ui @concurrent @regression @ui
Feature: Concurrent session protections prohibit a second session

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access
  Scenario: User can login with concurrent session and will be blocked
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I switch browser context to "concurrent"
    And I am logged in as a user with a single access role
    Then I should see the session selection page
    And I am not able to navigate away from session selection page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access
  Scenario: Primary session is logged out when concurrent session starts new session
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page

    When I switch browser context to "concurrent" and login again
    Then I should see the session selection page
    And I click the "Start a new session" button
    And I should be redirected to "/site/search-by-prescription-id"

    And the "primary" context should be logged out because of "concurrency" protections
    And I should see the concurrent session title "You have been logged out"

  # @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  # @single_access
  # Scenario: Concurrent session is closed and primary session remains active
  #. Given I am logged in as a user with a single access role
  #   When the "concurrent" session encounters a concurrent session conflict
  #   Then I should be redirected to the session selection page

  #   When I click the "Close this window" button
  #   Then the "concurrent" context should be logged out
  #   And the "primary" context should remain logged in

  # @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  # @single_access
  # Scenario: NHS service desk contact information is displayed for concurrent sessions
  #   Given I switch browser context to "primary"
  #   When the "primary" session encounters a concurrent session conflict
  #   And I switch browser context to "concurrent"
  #   And I click the "Start a new session" button
  #   And I switch browser context to "primary"
  #   Then I should see the concurrent session logged out page
  #   And I should see the NHS service desk email link
  #   And I should see the login link
