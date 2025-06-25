@cpts_ui @not_found_page @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4743
Feature: The site has a 404 not found page

    Scenario: The user is redirected to login when they navigate to an unknown page while not logged in
        When I navigate to a non-existent page
        Then I am on the login page
        
    Scenario: The user sees a "Page not found" error page when they navigate to an unknown page while logged in
        Given I am logged in as a user with multiple access roles
        And I have selected a role
        When I navigate to a non-existent page
        Then I am on the logged in Page Not Found page

    @deployed_only
    Scenario: The user sees a "Page not found" error page when they navigate to a url that is not under /site or /
        When I navigate outside the react app route with an incorrect two-segment path
        Then I am on the logged out Page Not Found page

    @deployed_only
    Scenario: The user sees a "Page not found" error page when they navigate to a url that is not under /site or / while logged in
        Given I am logged in as a user with multiple access roles
        When I navigate outside the react app route with an incorrect two-segment path
        Then I am on the logged in Page Not Found page

    @deployed_only
    Scenario: The user sees a genuine page when they navigate to a url that matches but is missing site path while logged in
        Given I am logged in as a user with multiple access roles
        When I navigate to the <page> app page outside of the site path
        Then I am redirected to the site, with URI of <page> correctly forwarded
        |page|
        |search for a prescription|
        |select your role|

    @deployed_only
    Scenario: The user sees an error page when they navigate to a url that doesn't match and is missing site path while logged in
        Given I am logged in as a user with multiple access roles
        When I navigate to the <page> app page outside of the site path
        Then I am redirected to the site, with URI of <page> correctly forwarded
        And I am on the logged in Page Not Found page
        |page|
        |spamandeggs|
