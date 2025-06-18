@cpts_ui @prescription_list @regression @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
Feature: Prescription List Page in the Prescription Tracker

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4793
  Scenario: View Prescription link navigates correctly
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the view prescription link
    Then I am taken to the correct prescription page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: User can access the prescription list page
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    Then I can see the heading "Prescriptions list"
    And I can see the results count message
    And I can see the appropriate prescription results tab headings


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: Back link navigates to appropriate search tab when accessed from prescription ID search
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "Go back" link
    Then I am redirected to the prescription ID search tab

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: Back link navigates to appropriate search tab when accessed from NHS number search
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on the NHS number search tab
    And I search for the prescription by NHS number search
    And I click on the "Go back" link
    Then I am redirected to the NHS number search tab


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4792
  Scenario: Display current prescriptions results table when clicking the current tab heading when current prescriptions are available
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "current" prescriptions tab heading
    Then I can see the "current" prescriptions results table
    And I see the table summary text displaying number of prescriptions


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4792
  Scenario: Display future prescriptions results table when clicking the future tab heading when future dated prescriptions are available
    Given a nominated eRD prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "future" prescriptions tab heading
    Then I can see the "future" prescriptions results table
    And I see the table summary text displaying number of prescriptions

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4792
  Scenario: Display past prescriptions results table when clicking the past tab heading when past prescriptions are available
    Given a nominated acute prescription has been created
    And the prescription has been cancelled
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "past" prescriptions tab heading
    Then I can see the "past" prescriptions results table
    And I see the table summary text displaying number of prescriptions

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario Outline: Should display no prescriptions found messages for past and future prescriptions when there are none available
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "<tab_name>" prescriptions tab heading
    Then I can see the appropriate no prescriptions found message

  Examples:
    | tab_name       |
    | past           | 
    | future         |


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: I can see the no prescriptions found message for current prescriptions when there are none available
    Given a nominated repeat prescription has been created
    And the prescription has been cancelled
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "current" prescriptions tab heading
    Then I can see the appropriate no prescriptions found message

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4793
  Scenario Outline: Sort current prescriptions table by <column> in <direction> order
    Given a nominated acute prescription has been created
    And I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for the prescription by prescription ID
    And I click on the "current" prescriptions tab heading
    And I sort the table by "<column>"
    Then the table is sorted by "<column>" in "<direction>" order
  
  Examples:
    | column               | direction   |
    | Issue date           | ascending   |
    | Prescription type    | ascending   |
    | Prescription type    | descending  |
    | Status               | ascending   |
    | Pending cancellation | ascending   |
    | Prescription ID      | ascending   |
