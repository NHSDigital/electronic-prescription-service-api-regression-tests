@cpts_ui @not_found_page @regression @blocker @smoke @ui
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4743
Feature: The site has a 404 not found page

    Scenario: The user is redirected to login when they navigate to an unknown page while not logged in
        When I navigate to a non-existent page
        Then I am on the login page
        
    Scenario: The user sees a "Page not found" error page when they navigate to an unknown page while logged in
        Given I am logged in as a user with multiple access roles
        When I navigate to a non-existent page
        Then I am on the logged in Page Not Found page

    @deployed_only
    Scenario: The user sees a "Page not found" error page when they navigate to a url that is not under /site
        When I navigate outside the react app route
        Then I am on the logged out Page Not Found page
