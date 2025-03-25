@cpts_ui @search_for_a_prescription @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4460
Feature: I can visit the Clinical Prescription Tracker Service Website

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4656
  Scenario: User is redirected to the Search For A Prescription Page
    When I log in as a user with a single access role
    Then I am on the search for a prescription page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4516
  Scenario: User can view the Search For A Prescription Page
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    Then I can see the search for a prescription header


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4518
  Scenario Outline: user can switch between different tabs
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab <Tab Name>
    Then I am on tab <Tab Name>
    Examples:
      | Tab Name               |
      | Prescription ID search |
      | NHS Number Search      |
      | Basic Details Search   |

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4535
  @rbac_banner
  Scenario: User can see their RBAC banner when a role is selected
    Given I am logged in as a user with multiple access roles
    When I select a role
    And I click the confirm and continue button on the your selected role page
    Then I can see the RBAC banner

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  Scenario: User is redirected correctly when they search for non-existent prescriptions
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab <Tab Name>
    # Search for a prescription ID that does NOT return anything
    And I search for a prescription using a valid prescription ID "209E3D-A83008-327F9F"
    Then I am on the prescription not found page with redirect to <Tab ID>
    Examples:
      | Tab Name               | Tab ID                 |
      | Prescription ID search | PrescriptionIdSearch   |
      | NHS Number Search      | NhsNumSearch           |
      | Basic Details Search   | BasicDetailsSearch     |
