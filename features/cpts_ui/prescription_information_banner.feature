@cpts_ui @prescription_information_banner @regression @ui @smoke
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4797
@multiple_access
Feature: The site displays the prescription information banner

  Background:
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role

  Scenario: The prescription information banner is not visible before searching
    When I go to the prescription details page without a prescription ID
    Then The prescription information banner is not visible

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: When I view an Acute prescription, the banner appears
    When I go to the prescription details for prescription ID "C0C757-A83008-C2D93O"
    Then The prescription information banner is visible

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: When I view an eRD prescription, the banner shows repeat and days supply
    When I go to the prescription details for prescription ID "3F885D-A83008-900ACJ"
    Then The prescription information banner displays repeat and days supply data

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: The copy to clipboard button copies the ID
    When I go to the prescription details for prescription ID "C0C757-A83008-C2D93O"
    And I click the copy prescription ID button
    Then The clipboard contains "C0C757-A83008-C2D93O"

  @skip # FIXME: temporary until use of real data in tracker is fixed
  Scenario: The loading message is displayed when prescription data is being fetched
    When I go to the prescription details for prescription ID "209E3D-A83008-327F9F"
    Then The page shows the loading message "Loading full prescription"
