@cpts_ui @prescription_information_banner @regression @ui @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4797
Feature: The site displays the prescription information banner

  Background:
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role

  Scenario: The prescription information banner is not visible before searching
    When I go to the prescription details page without a prescription ID
    Then The prescription information banner is not visible

  Scenario: The banner appears with correct data for an Acute prescription
    When I go to the prescription details page with prescription ID "C0C757-A83008-C2D93O"
    Then The prescription information banner shows
      | Prescription ID | C0C757-A83008-C2D93O |
      | Issue Date      | 18-Jan-2024          |
      | Status          | All items dispensed  |
      | Type            | Acute                |

  Scenario: The banner shows eRD repeat and days supply info
    When I go to the prescription details page with prescription ID "EC5ACF-A83008-733FD3"
    Then The prescription information banner shows
      | Prescription ID | EC5ACF-A83008-733FD3 |
      | Issue Date      | 22-Jan-2025          |
      | Status          | All items dispensed  |
      | Type            | eRD                  |
      | Repeat          | 2 of 6               |
      | Days Supply     | 28                   |

  Scenario: The copy to clipboard button copies the ID
    When I go to the prescription details page with prescription ID "C0C757-A83008-C2D93O"
    And I click the copy prescription ID button
    Then The clipboard contains "C0C757-A83008-C2D93O"
