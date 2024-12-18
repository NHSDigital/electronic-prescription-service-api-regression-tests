@cpts_ui @home @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4460
Feature: I can visit the Clinical Prescription Tracker Service Website

  Scenario: user can navigate to the Clinical Prescription Tracker Service Website homepage
    When I go to the homepage
    Then I am on the homepage

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4515
  Scenario: user can see the footer
    Given I am on the homepage
    Then I can see the footer

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4513
  Scenario: user can see the header
    Given I am on the homepage
    Then I can see the header
    # And I can see the links on the header

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4513
  Scenario: user sees a menu with links when the screen size is small
    Given I am on the homepage
    When I have a screen size of 690 pixels wide
    # Then I can see the header links in a dropdown menu

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4518
  Scenario: user can visit the search for a prescription page
    Given I am on the homepage
    # When I click on Find a prescription
    # Then I am on the search for a prescription page
