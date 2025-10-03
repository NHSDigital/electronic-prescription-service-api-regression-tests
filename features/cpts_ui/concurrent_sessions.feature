@cpts_ui @concurrency @regression @ui
Feature: Concurrent session protections prohibit a second session

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access
  Scenario: User can login with concurrent session and will be blocked
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I switch the browser context to "concurrent"
    And I am logged in as a user with a single access role
    Then I should see the session selection page
    And I am not able to navigate away from session selection page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @multiple_access
  Scenario: Multiple-access user can login with concurrent session and will be blocked
    Given I am logged in as a user with multiple access roles
    And I select a role
    And I click the confirm and continue button on the your selected role page
    And I can see the RBAC banner
    And I am on the search for a prescription page

    When the automatic periodic check occurs
    Then I should see the session selection page
    And I am not able to navigate away from session selection page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access @fake_time
  Scenario: Primary session is logged out when concurrent session starts new session
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page

    When I switch the browser context to "concurrent" and login again
    Then I should see the session selection page
    And I click the "Start a new session" button
    And I am on the search for a prescription page

    And I switch the browser context to "primary"
    And the automatic periodic check occurs
    And I should see the concurrent session logged out page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access @fake_time
  Scenario: Concurrent session is closed and primary session remains active
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page

    When I switch the browser context to "concurrent" and login again
    And I should see the session selection page
    And I click the "Close this window" button
    Then I see the logout successful page

    And I switch the browser context to "primary"
    And I search for the prescription by prescription ID
