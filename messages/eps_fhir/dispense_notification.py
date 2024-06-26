from datetime import date, datetime, UTC, timedelta
import json
from typing import Any
from uuid import uuid4


class DispenseNotificationIDs:
    def __init__(self, context: Any) -> None:
        self.practitioner_role = uuid4()
        self.organization = uuid4()
        self.medication_request = uuid4()

        self.dispense_notification = str(uuid4())
        context.dispense_notification_id = self.dispense_notification

        self.prescription_item = context.prescription_item_id
        self.long_prescription = context.long_prescription_id
        self.prescription = context.prescription_id

        self.nhs_number = context.nhs_number
        self.receiver_ods_code = context.receiver_ods_code


class DispenseNotification:
    def __init__(self, context: Any) -> None:
        self.ids = DispenseNotificationIDs(context)
        practitioner_role = self.practitioner_role()
        medication_request = self.medication_request()
        medication_dispense = self.medication_dispense(
            practitioner_role, medication_request
        )

        message_header = self.message_header()
        organization = self.organization()

        dispense_notification = self.dispense_notification(
            message_header, medication_dispense, organization
        )

        self.body = json.dumps(dispense_notification)

    def practitioner_role(self):
        return {
            "resourceType": "PractitionerRole",
            "id": f"urn:uuid:{self.ids.practitioner_role}",
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
            "organization": {"reference": f"urn:uuid:{self.ids.organization}"},
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

    def medication_request(self):
        return {
            "resourceType": "MedicationRequest",
            "id": f"urn:uuid:{self.ids.medication_request}",
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
                    "value": self.ids.prescription_item,
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
            "requester": {"reference": f"urn:uuid:{self.ids.practitioner_role}"},
            "groupIdentifier": {
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                        "valueIdentifier": {
                            "system": "https://fhir.nhs.uk/Id/prescription",
                            "value": self.ids.long_prescription,
                        },
                    }
                ],
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                "value": self.ids.prescription,
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
        practitioner_role,
        medication_request,
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
                        "value": self.ids.nhs_number,
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
                    {"actor": {"reference": f"#urn:uuid:{self.ids.practitioner_role}"}}
                ],
                "authorizingPrescription": [
                    {"reference": f"#urn:uuid:{self.ids.medication_request}"}
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
                        "value": self.ids.prescription_item,
                    }
                ],
                "type": {
                    "coding": [
                        {
                            "system": "https://fhir.nhs.uk/CodeSystem/medicationdispense-type",
                            "code": "0001",
                            "display": "Item fully dispensed",
                        }
                    ]
                },
                "dosageInstruction": [{"text": "4 times a day - Oral"}],
                "whenHandedOver": datetime.now(UTC).isoformat(),
            },
        }

    def message_header(self):
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
                    "endpoint": f"urn:nhs-uk:addressing:ods:{self.ids.receiver_ods_code}"
                },
                "response": {
                    "identifier": str(uuid4()),
                    "code": "ok",
                },
            },
        }

    def organization(self):
        return {
            "fullUrl": f"urn:uuid:{self.ids.organization}",
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
                        "value": self.ids.receiver_ods_code,
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
                "value": self.ids.dispense_notification,
            },
        }
