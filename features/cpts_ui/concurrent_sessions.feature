# @cpts_ui @concurrent @regression @blocker @smoke @ui
# Feature: Users are able to open a second session on the UI, but must control their concurrent session

#   @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5519
#   @multiple_access @concurrent
#   Scenario: User can login with second session and be blocked
#     Given a nominated acute prescription has been created
#     And I am logged in as a user with a single access role
#     And I am on the search for a prescription page
#     When I switch browser context to 'browser2'
#     And I am logged in as a user with a single access role
#     Then I am met with the session selection screen on 'browser2'
