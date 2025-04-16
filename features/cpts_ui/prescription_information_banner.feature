@cpts_ui @prescription_information_banner @regression @ui @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4797
Feature: The site displays the prescription information banner

  Background:
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role

  Scenario: The prescription information banner is not visible before searching
    When I go to the prescription details page without a prescription ID
    Then The prescription information banner is not visible

  # This test uses static mock data. Update once real prescription API integration is in place.
  Scenario: The banner appears with correct data for an Acute prescription
    When I go to the prescription details page with prescription ID "C0C757-A83008-C2D93O"
    Then The prescription information banner shows
      | Prescription ID | C0C757-A83008-C2D93O |
      | Issue Date      | 18-Jan-2024          |
      | Status          | Some items dispensed |
      | Type            | Acute                |

  # This test uses static mock data. Update once real prescription API integration is in place.
  Scenario: The banner shows eRD type with repeat info and days supply
    When I go to the prescription details page with prescription ID "209E3D-A83008-327F9F"
    Then The prescription information banner shows
      | Prescription ID | 209E3D-A83008-327F9F |
      | Issue Date      | 22-Jan-2025          |
      | Status          | All items dispensed  |
      | Type            | eRD 1 of 6           |
      | Days Supply     | 28 days              |

  # This test uses static mock data. Update once real prescription API integration is in place.
  Scenario: The copy to clipboard button copies the ID
    When I go to the prescription details page with prescription ID "C0C757-A83008-C2D93O"
    And I click the copy prescription ID button
    Then The clipboard contains "C0C757-A83008-C2D93O"

  # This test uses static mock data. Update once real prescription API integration is in place.
  Scenario: The loading message is displayed when prescription data is being fetched
    When I go to the prescription details page with prescription ID "209E3D-A83008-327F9F"
    Then The page shows the loading message "Loading full prescription"
