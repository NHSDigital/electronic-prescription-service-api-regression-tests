@pfp_apigee
Feature: I can see my prescriptions

  @pfp_uptime_monitor
  Scenario: I can see a single prescription
    Given I am authenticated with PFP-APIGEE app
    When I request prescriptions for NHS number '3163910432'
    Then I can see my prescription '6988FF-A83008-4CA68P'
