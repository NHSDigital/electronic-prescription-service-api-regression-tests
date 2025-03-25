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

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4783
  @find_prescription
  Scenario: User enters a valid prescription ID and is redirected to results page
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on tab Prescription ID search
    And I enter prescription ID "C0C757A83008C2D93O" into the input
    And I click the Find a prescription button
    Then I am redirected to the prescription results page for "C0C757-A83008-C2D93O"


  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4783
  @find_prescription
  Scenario: User enters an invalid prescription ID and sees not found page
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on tab Prescription ID search
    And I enter prescription ID "111111-222222-333333" into the input
    And I click the Find a prescription button
    Then I am redirected to the prescription not found page

  
 @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4783
  @find_prescription
  Scenario Outline: User sees validation error for incorrect prescription ID
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on tab Prescription ID search
    And I enter prescription ID "<Invalid ID>" into the input
    And I click the Find a prescription button
    Then the outcome should be: <Outcome>

    Examples:
      | Invalid ID              | Outcome                                                                                            |
      | C0C757A83008C2D9        | I see a validation message saying "must contain 18 characters"                                     |
      | C0C757A83008C2D93OOOOO  | I see a validation message saying "must contain 18 characters"                                     |
      | C0C757A83008C2D9#O      | I see a validation message saying "must contain only letters, numbers, dashes or the + character"  |
      | C0C757A83008C2D93-      | I see a validation message saying "must contain 18 characters"                                     |
      | c0c757a83008c2d93o      | I am redirected to the prescription results page for "C0C757-A83008-C2D93O"                        |
