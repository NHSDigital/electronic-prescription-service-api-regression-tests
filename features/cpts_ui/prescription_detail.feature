@cpts_ui @prescription_details @regression @ui
@multiple_access_pre_selected
Feature: Prescription Detail Page in the Clinical Prescription Tracker Service

  Background:
    Given I am logged in as a user with a pre selected role
    When I click the confirm and continue button on the your selected role page

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees all the organisation cards when they should
    Given a nominated acute prescription has been created and released
    When I go to the prescription details
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees only the prescriber organisation card when they should
    Given a non-nominated acute prescription has been created
    When I go to the prescription details
    Then The prescriber site card is visible
    And The dispenser site card is not visible
    And The nominated dispenser site card is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees only the prescriber and dispenser organisation cards when they should
    Given a non-nominated acute prescription has been created and released to FA565
    When I go to the prescription details
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is not visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4802
  Scenario: User sees the all the organisation cards when one of them is missing site data
    Given a nominated acute prescription has been created and released to INVALID
    When I go to the prescription details
    Then The prescriber site card is visible
    And The dispenser site card is visible
    And The nominated dispenser site card is visible

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: User sees EPS status tag on item card
    Given a nominated acute prescription has been created
    When I go to the prescription details
    Then An item card shows an EPS status tag

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: User sees only prescribed items with cancellation warning
    Given a nominated acute prescription has been created and released
    And the prescription has been cancelled
    When I go to the prescription details
    Then An item card shows a cancellation warning

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4799
  Scenario: Item cards do not show pharmacy status when it is missing
    Given a new prescription has been dispensed
    When I go to the prescription details
    Then No pharmacy status label is shown in the item card

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees message history with dispense notification dropdown
    Given a new prescription has been dispensed
    When I go to the prescription details
    Then The message history timeline is visible
    And A dispense notification information dropdown is shown

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees message history with pending cancellation
    Given a nominated acute prescription has been created and released
    And the prescription has been cancelled
    When I go to the prescription details
    Then The message history timeline is visible
    And A pending cancellation message is shown

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees message history for a cancelled prescription
    Given a nominated acute prescription has been created
    And the prescription has been cancelled
    When I go to the prescription details
    Then The message history timeline is visible
    And A cancelled status message is shown

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4801
  Scenario: User sees fallback text for missing site names in message history
    Given a nominated acute prescription has been created and released to INVALID
    When I go to the prescription details
    Then The message history timeline is visible
    And The timeline shows fallback text for missing site names
