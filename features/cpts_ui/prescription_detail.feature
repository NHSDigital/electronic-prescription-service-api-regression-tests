@cpts_ui @prescription_details @regression @ui
Feature: Prescription Detail Page in the Clinical Prescription Tracker Service

  Background:
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees all the organisation cards when they should
    Given I go to the prescription details for prescription ID "C0C757-A83008-C2D93O"
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees only the prescriber organisation card when they should
    Given I go to the prescription details for prescription ID "209E3D-A83008-327F9F"
    Then The prescriber site card is visible
    And The dispenser site card is not visible
    And The nominated dispenser site card is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees only the prescriber and dispenser organisation cards when they should
    Given I go to the prescription details for prescription ID "7F1A4B-A83008-91DC2E"
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees the all the organisation cards when one of them is missing site data
    Given I go to the prescription details for prescription ID "4D6F2C-A83008-A3E7D1"
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is visible
