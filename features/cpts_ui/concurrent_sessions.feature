@cpts_ui @concurrent @regression @ui
Feature: Users are able to open a second session on the UI, but must control their concurrent session

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
  @single_access
  Scenario: User can login with concurrent session and will be blocked
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the view prescription link
    Then I am taken to the correct prescription page
    And I switch browser context to "concurrent"
    And I am logged in as a user with a single access role
    # Then I am met with the session selection screen on 'concurrent'
