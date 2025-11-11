@pfp_apigee @pfp_aws @regression
Feature: I can see my prescriptions

  @blocker @smoke @e2e @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-4222
  Scenario: I can see a single prescription
    Given I am an authorised prescriber with EPS-FHIR-PRESCRIBING app
    And I successfully prepare and sign a prescription
    When I am authenticated with PFP-APIGEE app
    And I request my prescriptions
    Then I can see my prescription

  Scenario: I can only view my own prescriptions as an app user
    
  # for all of the following, test as L9 or app user
  Scenario: I can see multiple prescriptions

  Scenario: I can see no prescriptions

  Scenario: I can not see unreleased prescriptions

  Scenario: I can see a maximum of 25 prescription items

  Scenario: I can see prescription item details

  Scenario: I can see a FHIR compliant response for my prescriptions
  - Medicicine name
  - SNOMED
  - Dispenser details
  - Dosage instructions
  - Quantity prescribed
  - Formulation
  - Prescription item status
  - Prescription item type (acute, repeat, etc)

  Scenario: I can not see eRD prescription items

  Scenario: I can see prescription item status (multiple statuses, multiple items) - acute, repeat

  Scenario: I can not see prescriptions released by another ODS code

  Scenario: I can only request prescriptions via GET method  
