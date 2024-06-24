from dataclasses import dataclass
from datetime import date, datetime, UTC, timedelta
import json
from typing import Any
from uuid import uuid4


@dataclass
class DispenseNotificationIDs:
    practitioner_role = uuid4()
    organization = uuid4()
    medication_request = uuid4()


class DispenseNotification:
    def __init__(self, context: Any) -> None:
        ids = DispenseNotificationIDs()

        practitioner_role = self.practitioner_role(ids)
        medication_request = self.medication_request(ids, context)
        context.type_code = "0001" if context.amend is None else "0002"
        context.type_display = "Item Fully Dispensed" if context.amend is None else "Item Not Dispensed"
        medication_dispense = self.medication_dispense(
            ids, context, practitioner_role, medication_request
        )

        message_header = self.message_header(context) if context.amend is None else self.amended_message_header(context)
        organization = self.organization(ids, context)

        dispense_notification = self.dispense_notification(
            message_header, medication_dispense, organization
        )

        self.body = json.dumps(dispense_notification)

    def practitioner_role(self, ids: DispenseNotificationIDs):
        return {
            "resourceType": "PractitionerRole",
            "id": f"urn:uuid:{ids.practitioner_role}",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                    "value": "555086415105",
                }
            ],
            "practitioner": {
                "identifier": {
                    "system": "https://fhir.nhs.uk/Id/sds-user-id",
                    "value": "3415870201",
                },
                "display": "Jackie Clark",
            },
            "organization": {"reference": f"urn:uuid:{ids.organization}"},
            "code": [
                {
                    "coding": [
                        {
                            "system": "https://fhir.nhs.uk/CodeSystem/NHSDigital-SDS-JobRoleCode",
                            "code": "S8000:G8000:R8000",
                            "display": "Clinical Practitioner Access Role",
                        }
                    ]
                }
            ],
            "telecom": [{"system": "phone", "use": "work", "value": "02380798431"}],
        }

    def medication_request(self, ids: DispenseNotificationIDs, context: Any):
        return {
            "resourceType": "MedicationRequest",
            "id": f"urn:uuid:{ids.medication_request}",
            "extension": [
                {
                    "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionType",
                    "valueCoding": {
                        "system": "https://fhir.nhs.uk/CodeSystem/prescription-type",
                        "code": "1001",
                        "display": "Outpatient Community Prescriber - Medical Prescriber",
                    },
                }
            ],
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                    "value": context.prescription_item_id,
                }
            ],
            "status": "active",
            "intent": "order",
            "category": [
                {
                    "coding": [
                        {
                            "system": "https://terminology.hl7.org/CodeSystem/medicationrequest-category",
                            "code": "outpatient",
                            "display": "Outpatient",
                        }
                    ]
                }
            ],
            "medicationCodeableConcept": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",  # http only
                        "code": "322237000",
                    }
                ]
            },
            "subject": {"reference": f"urn:uuid:{uuid4()}"},
            "authoredOn": datetime.now(UTC).isoformat(),
            "requester": {"reference": f"urn:uuid:{ids.practitioner_role}"},
            "groupIdentifier": {
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                        "valueIdentifier": {
                            "system": "https://fhir.nhs.uk/Id/prescription",
                            "value": context.long_prescription_id,
                        },
                    }
                ],
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                "value": context.prescription_id,
            },
            "courseOfTherapyType": {
                "coding": [
                    {
                        "system": "https://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy",
                        "code": "acute",
                        "display": "Short course (acute) therapy",
                    }
                ]
            },
            "dosageInstruction": [
                {
                    "text": "4 times a day - Oral",
                    "timing": {
                        "repeat": {"frequency": 4, "period": 1, "periodUnit": "d"}
                    },
                    "route": {
                        "coding": [
                            {
                                "system": "https://snomed.info/sct",
                                "code": "26643006",
                                "display": "Oral",
                            }
                        ]
                    },
                }
            ],
            "dispenseRequest": {
                "validityPeriod": {
                    "start": str(date.today()),
                    "end": str(date.today() + timedelta(days=1)),
                },
                "expectedSupplyDuration": {
                    "value": 30,
                    "unit": "day",
                    "system": "http://unitsofmeasure.org",  # http only
                    "code": "d",
                },
                "quantity": {
                    "value": 100,
                    "unit": "tablet",
                    "system": "https://snomed.info/sct",
                    "code": "428673006",
                },
            },
            "substitution": {"allowedBoolean": False},
        }

    def medication_dispense(
        self,
        ids: DispenseNotificationIDs,
        context: Any,
        practitioner_role,
        medication_request
    ):
        return {
            "fullUrl": f"urn:uuid:{uuid4()}",
            "resource": {
                "resourceType": "MedicationDispense",
                "medicationCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",  # http only
                            "code": "322237000",
                        }
                    ]
                },
                "subject": {
                    "type": "Patient",
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": context.nhs_number,
                    },
                    "display": "MR DONOTUSE XXTESTPATIENT-TGNP",
                },
                "status": "completed",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-TaskBusinessStatus",
                        "valueCoding": {
                            "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-business-status",
                            "code": "0006",
                            "display": "Dispensed",
                        },
                    }
                ],
                "performer": [
                    {"actor": {"reference": f"#urn:uuid:{ids.practitioner_role}"}}
                ],
                "authorizingPrescription": [
                    {"reference": f"#urn:uuid:{ids.medication_request}"}
                ],
                "quantity": {
                    "value": 1,
                    "unit": "pre-filled disposable injection",
                    "system": "https://snomed.info/sct",
                    "code": "3318611000001103",
                },
                "contained": [practitioner_role, medication_request],
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/prescription-dispense-item-number",
                        "value": context.prescription_item_id,
                    }
                ],
                "type": {
                    "coding": [
                        {
                            "system": "https://fhir.nhs.uk/CodeSystem/medicationdispense-type",
                            "code": context.type_code,
                            "display": context.type_display,
                        }
                    ]
                },
                "dosageInstruction": [{"text": "4 times a day - Oral"}],
                "whenHandedOver": datetime.now(UTC).isoformat(),
            },
        }

    def message_header(self, context):
        return {
            "fullUrl": f"urn:uuid:{uuid4()}",
            "resource": {
                "resourceType": "MessageHeader",
                "eventCoding": {
                    "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                    "code": "dispense-notification",
                    "display": "Dispense Notification",
                },
                "source": {
                    "endpoint": f"urn:nhs-uk:addressing:ods:{context.receiver_ods_code}"
                },
                "response": {
                    "identifier": self.context.dn_id,
                    "code": "ok",
                },
            },
        }
    
    def amended_message_header(self, context):
        return {
            "fullUrl": f"urn:uuid:{uuid4()}",
            "resource": {
                "resourceType": "MessageHeader",
                "eventCoding": {
                    "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                    "code": "dispense-notification",
                    "display": "Dispense Notification",
                },
                 "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-replacementOf",
                        "valueIdentifier": {
                        "system": "https://tools.ietf.org/html/rfc4122",
                        "value": context.prescription_item_id,
                        }
                    }
                ],
                "source": {
                    "endpoint": f"urn:nhs-uk:addressing:ods:{context.receiver_ods_code}"
                },
                "response": {
                    "identifier": self.context.dn_id,
                    "code": "ok",
                },
            },
        }

    def organization(self, ids: DispenseNotificationIDs, context: Any):
        return {
            "fullUrl": f"urn:uuid:{ids.organization}",
            "resource": {
                "resourceType": "Organization",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-ODS-OrganisationRelationships",
                        "extension": [
                            {
                                "url": "reimbursementAuthority",
                                "valueIdentifier": {
                                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                    "value": "T1450",
                                },
                            }
                        ],
                    }
                ],
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": context.receiver_ods_code,
                    }
                ],
                "address": [
                    {
                        "city": "West Yorkshire",
                        "use": "work",
                        "line": ["17 Austhorpe Road", "Crossgates", "Leeds"],
                        "postalCode": "LS15 8BA",
                    }
                ],
                "active": True,
                "type": [
                    {
                        "coding": [
                            {
                                "system": "https://fhir.nhs.uk/CodeSystem/organisation-role",
                                "code": "182",
                                "display": "PHARMACY",
                            }
                        ]
                    }
                ],
                "name": "The Simple Pharmacy",
                "telecom": [
                    {"system": "phone", "use": "work", "value": "0113 3180277"}
                ],
            },
        }

    def dispense_notification(self, *entries):
        return {
            "resourceType": "Bundle",
            "type": "message",
            "entry": entries,
            "identifier": {
                "system": "https://tools.ietf.org/html/rfc4122",
                "value": str(uuid4()),
            },
        }
