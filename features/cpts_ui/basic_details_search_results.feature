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
    And I have searched for patients with the following details:
      | given | family              | gender | dateOfBirth | nhsNumber  | address                                              |
      | Issac | Wolderton-Rodriguez | Male   | 6-May-2013  | 9726919207 | 123 Brundel Close, Headingley, Leeds, West Yorkshire |
      | Steve | Wolderton-Rodriguez | Male   | 6-May-2013  | 9725919207 | 123 Brundel Close, Headingley, Leeds, West Yorkshire |

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: View search results table
    Then I should see a table with the following columns:
      | Name | Gender | Date of Birth | Address | NHS Number |
    And the table should be sorted by first name
    And I should see "2 results found" in the results count text
    And I should not see any restricted patients in the results

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Navigate to prescription list when clicking a patient row
    When I click on the patient row for "Issac Wolderton-Rodriguez"
    Then I should be navigated to the prescription list page
    And the NHS number "972 691 9207" should be included in the URL

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Navigate back to search page
    When I click the "Go back" link
    Then I should be navigated to the basic details search page
    And the search form should be cleared

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: Verify accessibility features
    Then the table should be responsive
    And the main content should have the role "main"
    And the results header should have the id "results-header"
    And the results count text should have the id "results-count" 
    And table cells should have the correct headers attribute
    And the NHS number "972 691 9207" should have visually hidden text
