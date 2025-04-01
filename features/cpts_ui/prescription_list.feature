@cpts_ui @prescription_list @regression @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
Feature: Prescription List Page in the Clinical Prescription Tracker Service

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: User can access the prescription list page
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I search for a prescription using a valid prescription ID "C0C757-A83008-C2D93O"
    Then I am redirected to the prescription list page with prescription ID "C0C757-A83008-C2D93O"
    And I can see the heading "Prescriptions list"
    And I can see the results count message
    
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: Back link navigates to appropriate search tab when accessed from prescription ID search
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    And I have accessed the prescription list page using a prescription ID search
    When I click on the "Go back" link
    Then I am redirected to the prescription ID search tab
    
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4778
  Scenario: Back link navigates to appropriate search tab when accessed from NHS number search
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    And I have accessed the prescription list page using an NHS number search
    When I click on the "Go back" link
    Then I am redirected to the NHS number search tab
