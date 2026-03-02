@cpts_ui @header_links @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-XXXX
Feature: Header

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4513
  # FIXME: Address this when the SPA is fixed!
  # The menu is broken and needs to be fixed. This test will not pass until it's fixed
  # @fixme
  # bug ticket: AEA-4996
  @multiple_access
  Scenario: user sees a menu with links when the screen size is small
    Given I am logged in as a user with multiple access roles
    When I have a screen size of 650 pixels wide
#    Then I can see the header links in a dropdown menu



  ############################################################################
  # LOGOUT
  ############################################################################
  @multiple_access
  Scenario: Logout link is shown for a logged in user
    Given I am logged in as a user with multiple access roles
    Then I see the "Logout" link

  Scenario: Logout link is not shown if user is not logged in
    When I go to the home page
    Then I do not see the "Logout" link

  ############################################################################
  # SELECT YOUR ROLE
  ############################################################################
  @multiple_access
  Scenario: Select Your Role link is not shown if I go to the select your role page
    Given I am logged in as a user with multiple access roles
    When I go to the select your role page
    Then I do not see the "Select Your Role" link

  @multiple_access_pre_selected
  Scenario: Select Your Role link is not shown if I already have a selected role
    Given I am logged in as a user with a pre selected role
    When I go to the home page
    Then I do not see the "Select Your Role" link

  ############################################################################
  # CHANGE ROLE
  ############################################################################
  @multiple_access
  Scenario: Change Role link is shown if the user has selected and confirmed the role
    Given I am logged in as a user with multiple access roles
    And I have confirmed a role
    When I go to the home page
    Then I see the "Change Role" link

  @multiple_access
  Scenario: Change Role link is shown if the user has selected but not confirmed the role
    Given I am logged in as a user with multiple access roles
    And I have selected a role
    Then I see the 'your selected role' page
    When I go to the home page
    Then I see the "Change Role" link

  # FIXME: Address this when the SPA is fixed!
  # Since the SPA is broken, there's actually no reliable way to navigate to the SYR page
  # once you've selected a role!
  # @fixme
  # Scenario: Change Role link is not shown if I go to the select your role page
  #   Given I am logged in
  #   When I have selected a role
  #   And I go to the select your role page
  #   Then I do not see the "Change Role" link

  @multiple_access
  Scenario: Change Role link is not shown if I am on the change role page
    Given I am logged in as a user with multiple access roles
    And I have selected a role
    When I go to change my role
    Then I do not see the "Change Role" link

  ############################################################################
  # FEEDBACK LINK
  ############################################################################
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4814
  @multiple_access_pre_selected
  Scenario: Feedback link is always visible in the header
    Given I am logged in as a user with a pre selected role
    When I go to the home page
    Then I see the "Give feedback" link

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4814
  @multiple_access_pre_selected
  Scenario: Feedback link opens in a new tab
    Given I am logged in as a user with a pre selected role
    When I go to the home page
    Then the "Give feedback" link opens the feedback form in a new tab
