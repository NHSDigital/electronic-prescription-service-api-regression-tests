@cpts_ui @select_your_role @regression @blocker @smoke @ui
Feature: Role selection page renders roles properly when logged in

  @rbac_banner
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4656
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
  @multiple_access
  Scenario: I am redirected to the select your role page when I log in
    When I log in as a user with multiple access roles
    Then I can not see the RBAC banner
    And I can see the roles with access cards
    And I can see the summary container
    And I cannot see the summary table body

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5061
  @multiple_access
  Scenario: I am redirected to the select your role page if I have no role selected
    When I log in as a user with multiple access roles
    And the login has finished
    And I go to the search for a prescription page
    Then I can see the summary container

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4653
  @multiple_access
  Scenario: I can show the available role information
    Given I am logged in as a user with multiple access roles
    When I click on the summary expander
    Then I can see the available role information

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
  @multiple_roles_no_access
  Scenario: I can show the inaccessible role information
    Given I am logged in as a user with only roles that do not have access
    When I click on the summary expander
    Then I can see the inaccessible role information

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4651
  @multiple_access
  Scenario: User can navigate to the your selected role page
    When I log in as a user with multiple access roles
    Then I can navigate to the your selected role page by clicking a card

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4655
  @multiple_roles_no_access
  Scenario: User without access can see the header on the select your role page
    When I log in as a user with only roles that do not have access
    Then I cannot see the your selected role subheader
    And I can see the no access header
    And I can see the no access message
    And I can see the summary container
    And I cannot see the summary table body

  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4645
  @multiple_access_pre_selected
  Scenario: User with a pre selected role sees their pre selected role
    Given I am logged in as a user with a pre selected role
    Then I can see the role that has been pre selected
  
  ############################################################################
  # Security Regression Tests
  ############################################################################
  @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5407
  @security_regression
  @multiple_access
  Scenario: URL navigation bypass blocked when no role selected
      Given I am logged in as a user with multiple access roles
      When I directly navigate to "/site/prescription-list-current?prescriptionId=0266F7-D81015-145C7P"
      Then I should be redirected to "/site/select-your-role"
