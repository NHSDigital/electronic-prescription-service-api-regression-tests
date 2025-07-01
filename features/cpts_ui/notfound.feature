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
    Scenario: The user isn't redirect if their path is not under /site or /page
        When I navigate outside the react app route with an incorrect two-segment path
        Then I am not redirected anywhere

    @deployed_only
    Scenario: The user isn't redirect if their path is not under /site or /page, while logged in
        Given I am logged in as a user with multiple access roles
        And I have selected a role
        When I navigate outside the react app route with an incorrect two-segment path
        Then I am not redirected anywhere

    @deployed_only
    Scenario: The user is redirected to the site, if their path is / or /page
        When I navigate to the 'search by prescription' app page outside of the site path
        Then I am redirected correctly to the site and sent to the login page

    @deployed_only
    Scenario: The user is redirected to the site, if their path is / or /page, while logged in
        Given I am logged in as a user with multiple access roles
        And I have selected a role
        When I navigate to the 'search by basic details' app page outside of the site path
        Then I am redirected correctly to the site, with URI of 'search by basic details' correctly forwarded

    @deployed_only
    Scenario: The user sees an error page when they navigate to a url that doesn't match and is missing site path while logged in
        Given I am logged in as a user with multiple access roles
        And I have selected a role
        When I navigate to the 'spamandeggs' app page outside of the site path
        Then I am redirected correctly to the site, with URI of 'spamandeggs' correctly forwarded
        And I am on the logged in Page Not Found page
