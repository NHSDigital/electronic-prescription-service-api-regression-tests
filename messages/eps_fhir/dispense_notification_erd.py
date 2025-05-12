import json
from typing import Any
from uuid import uuid4


class DispenseNotificationERDValues:
    def __init__(self, context: Any, amend: bool) -> None:
        self.practitioner_role_id = uuid4()
        self.organization_id = uuid4()
        self.medication_request_id = uuid4()

        self.medication_dispense_code = "0001"
        self.medication_dispense_display = "Item Fully Dispensed"

        self.dispense_notification_id = str(uuid4())
        context.dispense_notification_id = self.dispense_notification_id

        self.prescription_item_id = context.prescription_item_id
        self.long_prescription_id = context.long_prescription_id
        self.prescription_id = context.prescription_id

        self.nhs_number = context.nhs_number
        self.sender_ods_code = context.sender_ods_code
        self.receiver_ods_code = context.receiver_ods_code


class DispenseNotificationERD:
    def __init__(self, context: Any, amend: bool) -> None:
        self.HTTP_SNOMED_INFO_SCT = "http://snomed.info/sct"
        self.values = DispenseNotificationERDValues(context, amend)

        message_header = self.message_header()
        medication_dispense = self.medication_dispense()
        organization = self.organization()
        patient = self.patient()
        dispense_notification_erd = self.dispense_notification_erd(
            message_header, medication_dispense, organization, patient
        )
        self.body = json.dumps(dispense_notification_erd)
        print(self.body)

    def message_header(self):
        return {
            "fullUrl": "urn:uuid:521218c8-4266-4771-b9a8-d365804f5a5a",
            "resource": {
                "resourceType": "MessageHeader",
                "id": "521218c8-4266-4771-b9a8-d365804f5a5a",
                "destination": [
                    {
                        "endpoint": f"urn:nhs-uk:addressing:ods:{self.values.receiver_ods_code}",
                        "receiver": {
                            "identifier": {
                                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                "value": f"{self.values.receiver_ods_code}",
                            }
                        },
                    }
                ],
                "sender": {
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": f"{self.values.sender_ods_code}",
                    },
                    "display": "NHS Digital Spine",
                },
                "source": {
                    "name": "NHS Spine",
                    "endpoint": "https://int.api.service.nhs.uk/electronic-prescriptions/$process-message",
                },
                "response": {
                    "code": "ok",
                    "identifier": "ffffffff-ffff-4fff-bfff-ffffffffffff",
                },
                "eventCoding": {
                    "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                    "code": "dispense-notification",
                    "display": "Dispense Notification",
                },
                "focus": [
                    {"reference": "urn:uuid:c509973a-3bdd-496e-b58c-c8653fd70a1b"},
                    {"reference": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6"},
                ],
            },
        }

    def medication_dispense(self):
        return {
            "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
            "resource": {
                "resourceType": "MedicationDispense",
                "id": "a54219b8-f741-4c47-b662-e4f8dfa49ab6",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-TaskBusinessStatus",
                        "valueCoding": {
                            "code": "0006",
                            "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-business-status",
                            "display": "Dispensed",
                        },
                    },
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-RepeatInformation",
                        "extension": [
                            {"url": "numberOfRepeatsIssued", "valueInteger": 1},
                            {"url": "numberOfRepeatsAllowed", "valueInteger": 6},
                        ],
                    },
                ],
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/prescription-dispense-item-number",
                        "value": "21538f14-c45e-4791-8119-423b41739259",
                    }
                ],
                "contained": [
                    {
                        "resourceType": "PractitionerRole",
                        "id": "performer",
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
                            "display": "Mr Peter Potion",
                        },
                        "organization": {
                            "reference": "urn:uuid:2bf9f37c-d88b-4f86-ad5f-373c1416e04b"
                        },
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
                        "telecom": [
                            {"system": "phone", "use": "work", "value": "0532567890"}
                        ],
                    },
                    {
                        "resourceType": "MedicationRequest",
                        "id": "m2",
                        "extension": [
                            {
                                "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-ResponsiblePractitioner",
                                "valueReference": {
                                    "reference": "urn:uuid:88c92648-bcf3-4f10-99b2-e6db5d4fee5f"
                                },
                            },
                            {
                                "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionType",
                                "valueCoding": {
                                    "system": "https://fhir.nhs.uk/CodeSystem/prescription-type",
                                    "code": "0101",
                                },
                            },
                            {
                                "url": "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-MedicationRepeatInformation",  # noqa: E501
                                "extension": [
                                    {
                                        "url": "authorisationExpiryDate",
                                        "valueDateTime": "2024-04-07",
                                    },
                                    {
                                        "url": "numberOfPrescriptionsIssued",
                                        "valueUnsignedInt": 1,
                                    },
                                ],
                            },
                        ],
                        "identifier": [
                            {
                                "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                                "value": f"{self.values.prescription_item_id}",
                            }
                        ],
                        "status": "active",
                        "intent": "reflex-order",
                        "medicationCodeableConcept": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "15517911000001104",
                                    "display": "Methotrexate 10mg/0.2ml solution for injection pre-filled syringes",
                                }
                            ]
                        },
                        "subject": {
                            "reference": "urn:uuid:2537dfaa-d066-46e2-b032-5552dd247286"
                        },
                        "authoredOn": "2023-08-25T09:12:39+00:00",
                        "category": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                                        "code": "outpatient",
                                        "display": "Outpatient",
                                    }
                                ]
                            }
                        ],
                        "requester": {
                            "reference": "urn:uuid:88c92648-bcf3-4f10-99b2-e6db5d4fee5f"
                        },
                        "groupIdentifier": {
                            "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                            "value": f"{self.values.prescription_id}",
                            "extension": [
                                {
                                    "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                                    "valueIdentifier": {
                                        "system": "https://fhir.nhs.uk/Id/prescription",
                                        "value": f"{self.values.long_prescription_id}",
                                    },
                                }
                            ],
                        },
                        "courseOfTherapyType": {
                            "coding": [
                                {
                                    "system": "https://fhir.nhs.uk/CodeSystem/medicationrequest-course-of-therapy",
                                    "code": "continuous-repeat-dispensing",
                                    "display": "Continuous long term (repeat dispensing)",
                                }
                            ]
                        },
                        "dosageInstruction": [{"text": "As Directed"}],
                        "dispenseRequest": {
                            "extension": [
                                {
                                    "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
                                    "valueCoding": {
                                        "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
                                        "code": "P1",
                                    },
                                }
                            ],
                            "numberOfRepeatsAllowed": "6",
                            "quantity": {
                                "value": 1,
                                "unit": "pre-filled disposable injection",
                                "system": "http://snomed.info/sct",
                                "code": "3318611000001103",
                            },
                            "validityPeriod": {
                                "start": "2025-03-04",
                                "end": "2025-04-04",
                            },
                            "expectedSupplyDuration": {
                                "unit": "days",
                                "value": 10,
                                "system": "http://unitsofmeasure.org",
                                "code": "d",
                            },
                            "performer": {
                                "identifier": {
                                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                    "value": f"{self.values.receiver_ods_code}",
                                }
                            },
                        },
                        "substitution": {"allowedBoolean": False},
                        "basedOn": [
                            {
                                "reference": "urn:uuid:0c226058-8646-46f5-a3df-6b369b36e20d",
                                "extension": [
                                    {
                                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-RepeatInformation",  # noqa: E501
                                        "extension": [
                                            {
                                                "url": "numberOfRepeatsAllowed",
                                                "valueInteger": 6,
                                            },
                                            {
                                                "url": "numberOfRepeatsIssued",
                                                "valueInteger": 0,
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    },
                ],
                "status": "unknown",
                "medicationCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "15517911000001104",
                            "display": "Methotrexate 10mg/0.2ml solution for injection pre-filled syringes",
                        }
                    ]
                },
                "subject": {
                    "reference": "urn:uuid:c509973a-3bdd-496e-b58c-c8653fd70a1b",
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": f"{self.values.nhs_number}",
                    },
                },
                "performer": [{"actor": {"reference": "#performer"}}],
                "authorizingPrescription": [{"reference": "#m2"}],
                "type": {
                    "coding": [
                        {
                            "code": "0001",
                            "system": "https://fhir.nhs.uk/CodeSystem/medicationdispense-type",
                            "display": "Item fully dispensed",
                        }
                    ]
                },
                "quantity": {
                    "value": 1,
                    "unit": "pre-filled disposable injection",
                    "system": "http://snomed.info/sct",
                    "code": "3318611000001103",
                },
                "daysSupply": {
                    "unit": "days",
                    "value": 10,
                    "system": "http://unitsofmeasure.org",
                    "code": "d",
                },
                "whenHandedOver": "2023-08-29T15:46:00.853Z",
                "dosageInstruction": [{"text": "As Directed"}],
            },
        }

    def patient(self):
        return {
            "fullUrl": "urn:uuid:c509973a-3bdd-496e-b58c-c8653fd70a1b",
            "resource": {
                "resourceType": "Patient",
                "id": "c509973a-3bdd-496e-b58c-c8653fd70a1b",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": f"{self.values.nhs_number}",
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "family": "SNOWDEN",
                        "given": ["FINA", "JAIMIE"],
                        "prefix": ["MRS"],
                    }
                ],
                "gender": "female",
                "birthDate": "1993-10-14",
                "address": [
                    {
                        "use": "home",
                        "line": ["WELLESLEY HOUSE", "HORTON CRESCENT", "EPSOM"],
                        "postalCode": "KT19 8BQ",
                    }
                ],
                "generalPractitioner": [
                    {
                        "identifier": {
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                            "value": "A83008",
                        }
                    }
                ],
            },
        }

    def organization(self):
        return {
            "fullUrl": "urn:uuid:2bf9f37c-d88b-4f86-ad5f-373c1416e04b",
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
                        "value": "FA565",
                    }
                ],
                "id": "2bf9f37c-d88b-4f86-ad5f-373c1416e04b",
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

    def dispense_notification_erd(self, *entries):
        return {
            "resourceType": "Bundle",
            "id": "9adb8956-d132-4185-a1d7-4329670c57b8",
            "type": "message",
            "identifier": {
                "system": "https://tools.ietf.org/html/rfc4122",
                "value": self.values.dispense_notification_id,
            },
            "entry": entries,
        }
