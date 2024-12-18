@cpts_ui @home @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4460
Feature: I can visit the Clinical Prescription Tracker Service Website

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4516
  Scenario: User can view the Search For A Prescription Page
    Given I am on the homepage
    # When I click on Find a prescription
    # Then I am on the search for a prescription page
    # And I can see the search for a prescription header


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4518
  Scenario Outline: user can switch between different tabs
    Given I am on the search for a prescription page
    # When I click on tab <Tab Name>
    # Then I am on tab <Tab Name>
    # Examples:
    #   | Tab Name               |
    #   | Prescription ID search |
    #   | NHS Number Search      |
    #   | Basic Details Search   |
