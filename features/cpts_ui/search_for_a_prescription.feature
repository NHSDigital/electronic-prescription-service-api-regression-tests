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
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: User is redirected correctly when they search for non-existent prescriptions
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab Prescription ID search
    # Search for a prescription ID that DOES NOT return anything
    And I search for a prescription using a valid prescription ID "5B1112-A83008-EBCB2O"
    Then I am on the prescription not found page with redirect to PrescriptionIdSearch

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: User is redirected correctly when they search for non-existent patient
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab NHS Number search
    # Search for a prescription ID that DOES NOT return anything
    And I search for a patient using a valid NHS number "1234567899"
    Then I am on the prescription not found page with redirect to NhsNumSearch

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: User is redirected correctly when they hit the "Go Back" button after searching for non-existent prescription ID
    Given I am logged in as a user with a single access role
    When I am on the search for a prescription page
    And I click on tab Prescription ID search
    # Search for a prescription ID that DOES NOT return anything
    And I search for a prescription using a valid prescription ID "5B1112-A83008-EBCB2O"
    And I click the Go Back link on the prescription not found page
    Then I am on tab Prescription ID search

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4783
  @find_prescription
  Scenario: User enters a valid prescription ID and is redirected to results page
    Given I am logged in as a user with a single access role
    When I click on tab Prescription ID search
    # FIXME: This will need to be updated when the search pages are updated to use real data
    And I enter prescription ID "C0C757A83008C2D93O" into the input
    And I click the Find a prescription button
    Then I am redirected to the prescription results page for "C0C757-A83008-C2D93O"

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5304
  @find_prescription
  Scenario Outline: User sees validation error for incorrect prescription ID
    Given I am logged in as a user with a single access role
    When I click on tab Prescription ID search
    And I enter prescription ID "<Invalid ID>" into the input
    And I click the Find a prescription button
    Then I see a prescription ID validation error is displayed
    Examples:
      | Invalid ID              |
      | <empty>                 |
      | C0C757A83008C2D9        |
      | 12345678901234!@#       |
      | 12345678901234567!      |
      | H0C757-X83008-C2G93O    |
      | C0C757-A83008-C2D93X    |

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4787
  @find_patient
  @skip # FIXME: temporary until use of real data in tracker is fixed
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

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario: User sees validation errors when submitting empty Basic Details Search form
    Given I am logged in as a user with a single access role
    When I click on tab Basic Details Search
    And I click the Find a patient button
    Then I see a validation error is displayed

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario Outline: User sees validation errors and correct focus for invalid basic details
    Given I am logged in as a user with a single access role
    When I search using basic details: "<First>" "<Last>" "<Day>" "<Month>" "<Year>" "<Postcode>"
    Then I see a validation error is displayed
    And I click the first error summary link
    And the focus should be on the "<FocusField>" input
    Examples:
      | First  | Last        | Day | Month | Year | Postcode | FocusField    |
      | J@m!s  | Smith       | 15  | 10    | 2013 | LS1 1AB  | first-name    |
      | James  | Sm!th@123   | 15  | 07    | 2024 | LS1 1AB  | last-name     |
      | James  | Smith       | 45  | 89    | 2014 | LS1 1AB  | dob-day       |
      | James  | Smith       | 00  | 00    | 0000 | LS1 1AB  | dob-day       |
      | James  | Smith       | 28  | ab    | 2025 | LS1 1AB  | dob-month     |
      | James  | Smith       |  5  | 10    | 3211 | LS1 1AB  | dob-year      |
      | James  | Smith       | 12  | 08    | 2020 | LS!      | postcode-only |

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario: User is redirected to the current prescriptions page for a single match
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search using basic details: "James" "Smith" "02" "04" "2006" "LS1 1AB"
    Then I am on the prescription list current page with NHS number "1234567890"

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario: User is redirected to the too many results page for ambiguous patient match
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search using basic details: "<empty>" "Jones" "16" "07" "1985" "<empty>"
    Then I am on the too many results page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario: User is redirected to the patient search results page for multiple matches
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search using basic details: "<empty>" "Wolderton-Rodriguez" "06" "05" "2013" "<empty>"
    Then I am on the basic details search results page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5360
  @basic_details_search
  Scenario: User is redirected to the patient not found page for no matches
    Given I am logged in as a user with a single access role
    When I search using basic details: "<empty>" "SpecialNotFound" "01" "01" "1990" "<empty>"
    Then I am on the patient not found page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario: User sees all DOB fields highlighted and day focused for an invalid calendar date
    Given I am logged in as a user with a single access role
    When I search using basic details: "<empty>" "Smith" "31" "11" "2015" "<empty>"
    And I see a validation error is displayed
    And I click the first error summary link
    Then the focus should be on the "dob-day" input

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4785
  @basic_details_search
  Scenario: User sees DOB field error styling persist after correcting values until resubmission
    Given I am logged in as a user with a single access role
    When I search using basic details: "<empty>" "Smith" "!" "!" "!" "<empty>"
    And I see a validation error is displayed
    And I update the basic details DOB fields to "25" "12" "2010"
    Then the DOB inputs should have error styling

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5360
  @basic_details_search
  Scenario: User sees their search data preserved when going back from patient not found page
    Given I am logged in as a user with a single access role
    When I search using basic details: "<empty>" "SpecialNotFound" "01" "01" "1990" "<empty>"
    And I am on the patient not found page
    And I click on the "Go back" link
    Then the search form should be pre-filled with:
      | Field      | Value          |
      | Last name  | SpecialNotFound|
      | Day        | 01             |
      | Month      | 01             |
      | Year       | 1990           |

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5360
  @basic_details_search
  Scenario: User sees their search data preserved when going back from too many results page
    Given I am logged in as a user with a single access role
    # FIXME: This will need to be updated when the search pages are updated to use real data
    When I search using basic details: "<empty>" "Jones" "16" "07" "1985" "<empty>"
    And I am on the too many results page
    And I click on the "Go back" link
    Then the search form should be pre-filled with:
      | Field      | Value   |
      | Last name  | Jones   |
      | Day        | 16      |
      | Month      | 07      |
      | Year       | 1985    |
  
