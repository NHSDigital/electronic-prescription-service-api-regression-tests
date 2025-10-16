@cpts_ui @concurrent @timedout_session @regression @ui
Feature: Timedout session protections prohibit activity

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access @fake_time
  Scenario: User session timed out and the user is automatically logged out
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When the session expires because of automatic timeout
    And the automatic period check occurs
    Then I should see the timeout session logged out page
