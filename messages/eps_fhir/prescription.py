import json
from typing import Any
from uuid import uuid4

from features.environment import CIS2_USERS
from utils.prescription_id_generator import generate_short_form_id


class PrescriptionValues:
    def __init__(self, context: Any) -> None:
        self.sender_ods_code = "A83008"
        context.sender_ods_code = self.sender_ods_code
        self.receiver_ods_code = "FA565"
        context.receiver_ods_code = self.receiver_ods_code

        self.long_prescription_id = str(uuid4())
        context.long_prescription_id = self.long_prescription_id
        self.prescription_id = generate_short_form_id(context.sender_ods_code)
        context.prescription_id = self.prescription_id
        self.prescription_item_id = str(uuid4())
        context.prescription_item_id = self.prescription_item_id

        self.nomination_code = context.nomination_code
        self.nhs_number = context.nhs_number

        self.user_id = CIS2_USERS["prescriber"]["user_id"]
        self.sds_role_id = CIS2_USERS["prescriber"]["role_id"]


class Prescription:
    def __init__(self, context: Any) -> None:
        self.values = PrescriptionValues(context)
        self.HTTPS_ODS_ORGANIZATION_CODE = (
            "https://fhir.nhs.uk/Id/ods-organization-code"
        )
        message_header = self.create_message_header()
        medication_request = self.create_medication_request()
        patient = self.create_patient()
        organization = self.create_organization()
        practitioner_role = self.create_practitioner_role()
        practitioner = self.create_practitioner()

        self.body = self.create_fhir_bundle(
            message_header,
            medication_request,
            patient,
            organization,
            practitioner_role,
            practitioner,
        )

    def create_fhir_bundle(self, *entries):
        resource_id = str(uuid4())
        fhir_resource = {
            "resourceType": "Bundle",
            "id": resource_id,
            "identifier": {
                "system": "https://tools.ietf.org/html/rfc4122",
                "value": resource_id,
            },
            "type": "message",
            "entry": [],
        }
        fhir_resource["entry"].extend(entries)
        return json.dumps(fhir_resource)

    def create_message_header(self):
        bundle_id = uuid4()
        message_header = {
            "fullUrl": f"urn:uuid:{bundle_id}",
            "resource": {
                "resourceType": "MessageHeader",
                "id": "3599c0e9-9292-413e-9270-9a1ef1ead99c",
                "eventCoding": {
                    "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                    "code": "prescription-order",
                    "display": "Prescription Order",
                },
                "sender": {
                    "identifier": {
                        "system": self.HTTPS_ODS_ORGANIZATION_CODE,
                        "value": self.values.sender_ods_code,
                    },
                },
                "source": {
                    "endpoint": f"urn:nhs-uk:addressing:ods:{self.values.sender_ods_code}"
                },
            },
        }

        if self.values.receiver_ods_code:
            message_header["resource"].update(
                {
                    "destination": [
                        {
                            "endpoint": "https://sandbox.api.service.nhs.uk/electronic-prescriptions/$post-message",
                            "receiver": {
                                "identifier": {
                                    "system": self.HTTPS_ODS_ORGANIZATION_CODE,
                                    "value": self.values.receiver_ods_code,
                                }
                            },
                        }
                    ]
                },
            )
        return message_header

    def create_medication_request(self):
        medication_request = {
            "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
            "resource": {
                "resourceType": "MedicationRequest",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionType",
                        "valueCoding": {
                            "system": "https://fhir.nhs.uk/CodeSystem/prescription-type",
                            "code": "1001",
                            "display": "Primary Care Prescriber - Medical Prescriber",
                        },
                    }
                ],
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                        "value": self.values.prescription_item_id,
                    }
                ],
                "status": "active",
                "intent": "order",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "https://terminology.hl7.org/CodeSystem/medicationrequest-category",
                                "code": "community",
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
                "subject": {
                    "reference": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2"
                },
                "requester": {
                    "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
                },
                "groupIdentifier": {
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                            "valueIdentifier": {
                                "system": "https://fhir.nhs.uk/Id/prescription",
                                "value": self.values.long_prescription_id,
                            },
                        }
                    ],
                    "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                    "value": self.values.prescription_id,
                },
                "courseOfTherapyType": {
                    "coding": [
                        {
                            # http only
                            "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy",
                            "code": "acute",
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
                    "validityPeriod": {"start": "2024-04-29", "end": "2024-07-28"},
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
            },
        }

        if self.values.nomination_code == "P1":
            medication_request["resource"]["dispenseRequest"].update(
                {
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
                            "valueCoding": {
                                "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
                                "code": self.values.nomination_code,
                            },
                        }
                    ],
                    "performer": {
                        "identifier": {
                            "system": self.HTTPS_ODS_ORGANIZATION_CODE,
                            "value": self.values.receiver_ods_code,
                        }
                    },
                }
            )

        if self.values.nomination_code == "0004":
            medication_request["resource"]["dispenseRequest"].update(
                {
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
                            "valueCoding": {
                                "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
                                "code": self.values.nomination_code,
                            },
                        }
                    ],
                }
            )

        return medication_request

    def create_practitioner_role(self):
        return {
            "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
            "resource": {
                "resourceType": "PractitionerRole",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                        "value": self.values.sds_role_id,
                    }
                ],
                "practitioner": {
                    "reference": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a"
                },
                "organization": {
                    "reference": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"
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
                "telecom": [{"system": "phone", "value": "01234567890", "use": "work"}],
            },
        }

    def create_practitioner(self):
        return {
            "fullUrl": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a",
            "resource": {
                "resourceType": "Practitioner",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/sds-user-id",
                        "value": self.values.user_id,
                    },
                    {
                        "system": "https://fhir.hl7.org.uk/Id/nmc-number",
                        "value": "999999",
                    },
                ],
                "name": [{"family": "BOIN", "given": ["C"], "prefix": ["DR"]}],
            },
        }

    def create_patient(self):
        return {
            "fullUrl": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2",
            "resource": {
                "resourceType": "Patient",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": self.values.nhs_number,
                    }
                ],
                "name": [
                    {
                        "use": "usual",
                        "family": "CORY",
                        "given": ["ETTA"],
                        "prefix": ["MISS"],
                    }
                ],
                "gender": "female",
                "birthDate": "1999-01-04",
                "address": [
                    {
                        "use": "home",
                        "line": ["123 Dale Avenue", "Long Eaton", "Nottingham"],
                        "postalCode": "NG10 1NP",
                    }
                ],
                "generalPractitioner": [
                    {
                        "identifier": {
                            "system": self.HTTPS_ODS_ORGANIZATION_CODE,
                            "value": self.values.sender_ods_code,
                        }
                    }
                ],
            },
        }

    def create_organization(self):
        return {
            "fullUrl": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
            "resource": {
                "resourceType": "Organization",
                "identifier": [
                    {
                        "system": self.HTTPS_ODS_ORGANIZATION_CODE,
                        "value": "A83008",
                    }
                ],
                "name": "SOMERSET BOWEL CANCER SCREENING CENTRE",
                "address": [
                    {
                        "use": "work",
                        "line": ["MUSGROVE PARK HOSPITAL"],
                        "city": "TAUNTON",
                        "postalCode": "TA1 5DA",
                    }
                ],
                "telecom": [
                    {"system": "phone", "value": "01823 333444", "use": "work"}
                ],
                "partOf": {
                    "identifier": {
                        "system": self.HTTPS_ODS_ORGANIZATION_CODE,
                        "value": "RBA",
                    },
                    "display": "TAUNTON AND SOMERSET NHS FOUNDATION TRUST",
                },
            },
        }
