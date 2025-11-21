@eps_assist_me @regression
Feature: I can call the chatbot

  Background:
    Given I am authenticated with AWS for eps-assist-me

  @blocker @smoke @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5873
  Scenario: Regression test invokes lambda directly
    Given A regression test suite is executed
    When The test invokes the slackbot lambda with a direct invocation event
    Then The lambda returns a structured AI response matching expected format

  @blocker @smoke @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-5873
  Scenario: Regression test validates session continuity
    Given A regression test with multiple related queries
    When Tests are run with session_id continuity
    Then Lambda maintains conversation context across invocations
