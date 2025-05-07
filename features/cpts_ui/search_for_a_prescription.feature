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
    And I click on tab Prescription ID search
    # Search for a prescription ID that DOES NOT return anything
    And I search for a prescription using a valid prescription ID "209E3D-A83008-328F9F"
    Then I am on the prescription not found page with redirect to PrescriptionIdSearch
    
  # TODO: Update this test when the NHS number search is implemented
  # @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  # Scenario: User is redirected correctly when they search for non-existent patient
  #   Given I am logged in as a user with a single access role
  #   When I am on the search for a prescription page
  #   And I click on tab NHS Number search
  #   # Search for a prescription ID that DOES NOT return anything
  #   And I search for a patient using a valid NHS number "1234567890"
  #   Then I am on the prescription not found page with redirect to NhsNumSearch

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  Scenario: User is redirected correctly when they hit the "Go Back" button after searching for non-existent prescription ID
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab Prescription ID search
    # Search for a prescription ID that DOES NOT return anything
    And I search for a prescription using a valid prescription ID "209E3D-A83008-328F9F"
    And I click the Go Back link on the prescription not found page
    Then I am on tab Prescription ID search

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4783
  @find_prescription
  Scenario: User enters a valid prescription ID and is redirected to results page
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on tab Prescription ID search
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I enter prescription ID "C0C757A83008C2D93O" into the input
    And I click the Find a prescription button
    Then I am redirected to the prescription results page for "C0C757-A83008-C2D93O"

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
      | H0C757-X83008-C2G93O    | I see a validation message saying "The prescription ID number is not recognised"                   |
      # FIXME: This will need to be updated when the search pages are updated to use real data
      | c0c757a83008c2d93o      | I am redirected to the prescription results page for "C0C757-A83008-C2D93O"                        |

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @find_patient
  Scenario: User is redirected correctly when they search for non-existent patient using NHS number
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab NHS Number Search
    And I enter NHS number "0987654321" into the input
    And I click the Find a patient button
    Then I am on the prescription not found page with redirect to NhsNumberSearch

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @find_patient
  Scenario: User is redirected correctly when they search for an existing patient using NHS number
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab NHS Number Search
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I enter NHS number "1234567890" into the input
    And I click the Find a patient button
    Then I am on the prescription list current page with NHS number "1234567890"

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @find_patient
  Scenario: User sees a validation message when NHS number field is left empty
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on tab NHS Number Search
    And I click the Find a patient button
    Then I see a validation error is displayed

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @find_patient
  Scenario Outline: User sees a validation message for invalid NHS number
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page
    When I click on tab NHS Number Search
    And I enter NHS number "<Invalid NHS number>" into the input
    And I click the Find a patient button
    Then I see a validation error is displayed

  Examples:
    | Invalid NHS number |
    | abc                |
    | 123                |
    | 123456789000       |
