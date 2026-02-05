@pfp_proxygen @pfp_aws @regression
Feature: I can see my prescriptions via PFP Proxygen

  @skip we don't have nhs numbers that allow this to work ATM
  @blocker @smoke @e2e @delegated_access
  Scenario: I can see a single prescription using delegated access
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    # whose NHS number is '9912003072'
    And I successfully prepare and sign a prescription on behalf of a patient whose NHS number is '9912003073'
    When I am authenticated with PFP-PROXYGEN app
    And I request prescriptions on behalf of '9912003073'
    Then I can see a prescription for '9912003073'
