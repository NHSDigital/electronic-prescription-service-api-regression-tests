@cpts_ui @footer @regression @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4814
Feature: Footer

  Background: The footer is visible on the homepage
    Given I am on the privacy notice page
    And I can see the page footer

  Scenario Outline: Footer links are visible
    Then I can see the "<LinkText>" link in the footer

    Examples:
      | LinkText                                |
      | Privacy notice (opens in new tab)       |
      | Terms and conditions                    |
      | Cookie policy                           |

  Scenario: Footer displays the copyright section
    Then I see the footer copyright section

  Scenario Outline: Footer links redirect to correct target
    When I click the "<LinkName>" link in the footer
    Then the current page URL contains <ExpectedURL>

    Examples:
      | LinkName               | ExpectedURL        |
      | privacy notice         | privacy-notice     |
      | terms and conditions   | digital.nhs.uk     |
      | cookie policy          | cookies            |
