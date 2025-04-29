@cpts_ui @prescription_details @regression @ui
Feature: Prescription Detail Page in the Clinical Prescription Tracker Service

  Background:
    Given I am logged in as a user with a single access role
    And I am on the search for a prescription page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees all the organisation cards when they should
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "C0C757-A83008-C2D93O"
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees only the prescriber organisation card when they should
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "209E3D-A83008-327F9F"
    Then The prescriber site card is visible
    And The dispenser site card is not visible
    And The nominated dispenser site card is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees only the prescriber and dispenser organisation cards when they should
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "7F1A4B-A83008-91DC2E"
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees the all the organisation cards when one of them is missing site data
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "4D6F2C-A83008-A3E7D1"
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: User sees both prescribed and dispensed item cards
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "C0C757-A83008-C2D93O"
    Then The prescribed items card is visible
    And The dispensed items card is visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: User sees EPS status tag on item card
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "C0C757-A83008-C2D93O"
    Then An item card shows an EPS status tag

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: User sees only prescribed items with cancellation warning
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "7F1A4B-A83008-91DC2E"
    Then The prescribed items card is visible
    And The dispensed items card is not visible
    And A prescribed item card shows a cancellation warning

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: User sees only dispensed item cards, with expandable and status tag
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "B8C9E2-A83008-5F7B3A"
    Then The prescribed items card is not visible
    And The dispensed items card is visible
    And A dispensed item card has expandable initial prescription

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
    # FIXME: Remove references to static data
  Scenario: Dispensed item cards do not show pharmacy status when it is missing
    When I go to the prescription details for prescription ID "4D6F2C-A83008-A3E7D1"
    Then No pharmacy status label is shown in the dispensed item card

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees message history with dispense notification dropdown
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "4D6F2C-A83008-A3E7D1"
    Then The message history timeline is visible
    And A dispense notification information dropdown is shown

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees message history with pending cancellation
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "7F1A4B-A83008-91DC2E"
    Then The message history timeline is visible
    And A pending cancellation message is shown

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees message history for a cancelled prescription
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "3DA34A-A83008-A0B2EV"
    Then The message history timeline is visible
    And A cancelled status message is shown

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  @prescription_details_1
  Scenario: User sees fallback text for missing site names in message history
    # FIXME: Remove references to static data
    When I go to the prescription details for prescription ID "88AAF5-A83008-3D404Q"
    Then The message history timeline is visible
    And The timeline shows fallback text for missing site names
