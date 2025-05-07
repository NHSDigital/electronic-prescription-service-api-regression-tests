@cpts_ui @home @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4460
Feature: I can visit the Clinical Prescription Tracker Service Website

  @rbac_banner
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4515
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4513
  Scenario: user can navigate to the Clinical Prescription Tracker Service Website homepage
    When I go to the home page
    Then I am on the homepage
    And I can see the header
    And I can see the footer
    And I can not see the RBAC banner
