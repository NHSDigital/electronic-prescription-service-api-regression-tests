@pfp_apigee @pfp_aws @regression
Feature: I can see my prescriptions

  # @blocker @smoke @e2e @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
  # Scenario: I can see a single prescription
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign a prescription
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I can see my prescription

  # # TODO: for all of the following, test as L9 or app user
  # # Spine defined limit of 25 prescriptions per request
  # Scenario: I can see a maximum of 25 prescriptions
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign '26' nominated acute prescriptions
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I can see '25' of my prescriptions

  # # FLAKY WARNING: We've agreed to rely on NHS random generation to return an NHS number without prescriptions
  # # This may cause flakiness if the random NHS number happens to have prescriptions
  # Scenario: I can see no prescriptions
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign '0' nominated acute prescriptions
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I can see '0' of my prescriptions

  # Scenario: I can not see unreleased prescriptions
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare a nominated acute prescription
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I cannot see my prescription

  # Scenario: I can only request prescriptions via GET method
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign a nominated acute prescription
  #   When I am authenticated with PFP-APIGEE app
  #   And I attempt to request my prescriptions via 'POST' method
  #   Then the response indicates forbidden

  # Scenario: I can not see eRD prescription items
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign a nominated eRD prescription
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I do not see an eRD prescription

  # Scenario: I can see a FHIR compliant response for my prescriptions
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign a nominated acute prescription
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I validate the prescription matches my prepared prescription

  @e2e
  Scenario: I can see prescription item status (multiple statuses, multiple items) - acute, repeat
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign '2' nominated acute prescriptions
    And I am an authorised dispenser with EPS-FHIR-DISPENSING app
    And I release all prescriptions
    When I set the statuses I will update through
      | Status        |
      | With Pharmacy |
    Then I process the status updates for the prescription items and verify they are returned

  # This scenario requires changes to FHIR compliance endpoint to be able to validate PFP responses
  # Scenario: I can see prescription item details in FHIR compliant response
  #   Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
  #   And I successfully prepare and sign a prescription
  #   When I am authenticated with PFP-APIGEE app
  #   And I request my prescriptions
  #   Then I am an authorised prescriber with EPS-FHIR app
  #   And I validate the response for FHIR compliance
  #   And the response indicates a success
