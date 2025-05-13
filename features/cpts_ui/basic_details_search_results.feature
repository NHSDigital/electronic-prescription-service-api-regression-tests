@cpts_ui @basic_details_results @regression @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4790
Feature: Basic Details Search Results Page
  As a healthcare professional
  I want to see a list of patients matching my search criteria
  So that I can select the correct patient to view their prescriptions

# TODO: will need to be updated with different entries (for now they are hard coded)
  Background:
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    And I am on the basic details search results page
    # the restricted user scenario is more so of a mock - we won't be surfacing restricted results to the frontend
    # in the real scenarios to my understanding, but the frontend still handles filtering them out incase.
    And I have searched for patients with the following details:
      | given | family              | gender | dateOfBirth | nhsNumber  | address                                              | restricted |
      | Issac | Wolderton-Rodriguez | Male   | 6-May-2013  | 9726919207 | 123 Brundel Close, Headingley, Leeds, West Yorkshire | false      |
      | Steve | Wolderton-Rodriguez | Male   | 6-May-2013  | 9725919207 | 123 Brundel Close, Headingley, Leeds, West Yorkshire | false      |
      | John  | Smith              | Male   | 1-Jan-2000  | 1234567890 | 456 Test Street, London                             | true       |

  Scenario: View search results table
    Then I should see a table with the following columns:
      | Name | Gender | Date of Birth | Address | NHS Number |
    And the table should be sorted by first name
    And I should see "2 results found" in the results count text
    And I should not see any restricted patients in the results

  Scenario: Navigate to prescription list when clicking a patient row
    When I click on the patient row for "Issac Wolderton-Rodriguez"
    Then I should be navigated to the prescription list page
    And the NHS number "972 691 9207" should be included in the URL

  Scenario: Navigate to prescription list when pressing enter on a patient row
    When I press enter on the patient row for "Steve Wolderton-Rodriguez"
    Then I should be navigated to the prescription list page
    And the NHS number "972 591 9207" should be included in the URL

  Scenario: Navigate back to search page
    When I click the "Go back" link
    Then I should be navigated to the basic details search page
    And the search form should be cleared

  Scenario: Verify accessibility features
    Then each patient row should have the correct aria-label
    And the table should be responsive
    And the main content should have the role "main"
    And the results header should have the id "results-header"
    And the results count text should have the id "results-count" 
