@cpts_ui @home @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4658
Feature: I can view the Select Your Role page and view the header on the Clinical Prescription Tracker Service Website

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4658
  Scenario: User can view the header on the Select Your Role page
    Given I am on the homepage
    When I click on the Select Your Role link
    Then I can see the header saying "Select your role"

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4658
  Scenario: User can see their assigned role and location in the header
    Given I am logged in with a role assigned
    When I navigate to the Select Your Role page
    Then I can see the message saying "You are currently logged in at <pharmacy> with <role> access."

  Examples:
  | pharmacy                | role                         |
  | GREENE'S PHARMACY (FG419) | Health Professional Access Role |
  | TOWN HALL PHARMACY (TH123) | Pharmacist Role                 |
