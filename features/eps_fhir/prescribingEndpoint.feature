@eps_fhir @smoke @regression @blocker @eps_prescribing_dispensing @create @prescribing

Feature: I can use the prescribing endpoint
@allure.tms:https://nhsd-jira.digital.nhs.uk/browse/3847
Scenario Outline: I can create, sign and release a prescription
Given I am an authorised prescriber
And I successfully prepare and sign a <Type> prescription using the prescribing endpoint
When I am an authorised dispenser
And I release the prescription
Then the response indicates a success
And the response body indicates a successful release action
Examples:
| Type          |
| nominated     |
| non-nominated |

@cancel @allure.tms:https://nhsd-jira.digital.nhs.uk/browse/AEA-3869
Scenario: I can cancel a prescription
Given I am an authorised prescriber
And I successfully prepare and sign a non-nominated prescription using the prescribing endpoint
When I cancel all line items on the prescription
Then the response indicates a success
And the response body indicates a successful cancel action
