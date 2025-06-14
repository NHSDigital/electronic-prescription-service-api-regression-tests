@cpts_ui @prescription_list @regression @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
Feature: Prescription List Page in the Clinical Prescription Tracker Service

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: User can access the prescription list page
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search for a prescription using a valid prescription ID "C0C757-A83008-C2D93O"
    Then I am redirected to the prescription list page with prescription ID "C0C757-A83008-C2D93O"
    And I can see the heading "Prescriptions list"
    And I can see the results count message
    And I can see the appropriate prescription results tab headings

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Back link navigates to appropriate search tab when accessed from prescription ID search
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    And I have accessed the prescription list page using a prescription ID search
    When I click on the "Go back" link
    Then I am redirected to the prescription ID search tab
    
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Back link navigates to appropriate search tab when accessed from NHS number search
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    And I have accessed the prescription list page using an NHS number search
    When I click on the "Go back" link
    Then I am redirected to the NHS number search tab

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4792
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Display current prescriptions results table when clicking the current tab heading
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I am on the prescription list page for prescription ID "C0C757-A83008-C2D93O"
    When I click on the current prescriptions tab heading
    Then I can see the current prescriptions results table
    And I see the table summary text Showing 7 of 7


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4792
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Display future prescriptions results table when clicking the future tab heading
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I am on the prescription list page for prescription ID "C0C757-A83008-C2D93O"
    When I click on the future prescriptions tab heading
    Then I can see the future prescriptions results table
    And I see the table summary text Showing 1 of 1

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4792
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Display past prescriptions results table when clicking the past tab heading
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I am on the prescription list page for prescription ID "C0C757-A83008-C2D93O"
    When I click on the past prescriptions tab heading
    Then I can see the past prescriptions results table
    And I see the table summary text Showing 2 of 2

@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4793
@skip # FIXME: temporary until use of real data in tracker is fixed
Scenario Outline: Sort current prescriptions table by <column> in <direction> order
  Given I am logged in as a user with a single access role
  And I am on the prescription list page for prescription ID "C0C757-A83008-C2D93O"
  When I click on the current prescriptions tab heading
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


@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4793
@skip # FIXME: temporary until use of real data in tracker is fixed
Scenario: View Prescription link navigates correctly 
  Given I am logged in as a user with a single access role
  And I am on the prescription list page for prescription ID "C0C757-A83008-C2D93O"
  When I click on the current prescriptions tab heading
  Then I click on the view prescription link
  And I am taken to the correct prescription page
