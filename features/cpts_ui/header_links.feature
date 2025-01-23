@cpts_ui @header_links @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-XXXX
Feature: Header links are displayed according to the user's state and the current page

  ############################################################################
  # EXIT
  ############################################################################
  Scenario: Exit link is shown on the logout page once the user signs out
    Given I am logged in
    And The logout confirmation modal is displayed
    When I confirm the logout
    Then I see the "Exit" link

  Scenario: Exit link is shown on the select your role page if the user has no roles with access
    Given I am logged in without access
    Then I see the "Exit" link

  Scenario: Exit link is not shown if user has at least one role with access on the select your role page
    Given I am logged in with a single access role
    Then I do not see the "Exit" link

  ############################################################################
  # LOGOUT
  ############################################################################
  Scenario: Logout link is shown for a logged in user
    Given I am logged in
    Then I see the "Logout" link

  Scenario: Logout link is not shown if user is not logged in
    When I am on the homepage
    Then I do not see the "Logout" link

  ############################################################################
  # SELECT YOUR ROLE
  ############################################################################
  Scenario: Select Your Role link is shown on the homepage, if we dont select a role
    Given I am logged in
    When I am on the homepage
    Then I see the "Select Your Role" link

  Scenario: Select Your Role link is not shown if I go to the select your role page
    Given I am logged in
    When I go to the select your role page
    Then I do not see the "Select Your Role" link

  Scenario: Select Your Role link is not shown if I already have a selected role
    Given I am logged in
    When I have a selected role
    And I am on the homepage
    Then I do not see the "Select Your Role" link

  ############################################################################
  # CHANGE ROLE
  ############################################################################
  Scenario: Change Role link is shown if the user has a selected role
    Given I am logged in
    When I have a selected role
    When I am on the homepage
    Then I see the "Change Role" link

  Scenario: Change Role link is not shown if the user has no selected role
    Given I am logged in
    When I am on the homepage
    Then I do not see the "Change Role" link

  # FIXME: Address this when the SPA is fixed!
  # Since the SPA is broken, there's actually no reliable way to navigate to the SYR page 
  # once you've selected a role!
  # @fixme
  # Scenario: Change Role link is not shown if I go to the select your role page
  #   Given I am logged in
  #   When I have a selected role
  #   And I go to the select your role page
  #   Then I do not see the "Change Role" link

  Scenario: Change Role link is not shown if I am on the change role page
    Given I am logged in
    When I go to change my role
    Then I do not see the "Change Role" link
