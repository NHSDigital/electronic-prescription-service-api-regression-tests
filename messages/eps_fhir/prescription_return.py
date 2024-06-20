import json
from typing import Any
from uuid import uuid4

from features.environment import CIS2_USERS


class Return:
    def __init__(self, context: Any) -> None:
        self.context = context
        body = self.generate_return()
        self.body = json.dumps(body)

    def generate_return(self):
        return {
            "resourceType": "Task",
            "id": f"{uuid4()}",
            "contained": [
                {
                    "resourceType": "PractitionerRole",
                    "id": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                            "value": CIS2_USERS["prescriber"]["role_id"],
                        }
                    ],
                    "practitioner": {
                        "identifier": {
                            "system": "https://fhir.nhs.uk/Id/sds-user-id",
                            "value": CIS2_USERS["prescriber"]["user_id"],
                        },
                        "display": "Jackie Clark",
                    },
                    "organization": {
                        "reference": "#urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"
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
                        {"system": "phone", "use": "work", "value": "02380798431"}
                    ],
                },
                {
                    "resourceType": "Organization",
                    "id": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
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
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                            "value": "RBA",
                        },
                        "display": "TAUNTON AND SOMERSET NHS FOUNDATION TRUST",
                    },
                },
            ],
            "identifier": [
                {
                    "system": "https://tools.ietf.org/html/rfc4122",
                    "value": f"{uuid4()}",
                }
            ],
            "status": "rejected",
            "statusReason": {
                "coding": [
                    {
                        "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-dispense-return-status-reason",
                        "code": "0003",
                        "display": "Patient requested release",
                    }
                ]
            },
            "intent": "order",
            "code": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/CodeSystem/task-code",
                        "code": "fulfill",
                        "display": "Fulfill the focal request",
                    }
                ]
            },
            "groupIdentifier": {
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                "value": self.context.prescription_id,
            },
            "focus": {
                "identifier": {
                    "system": "https://tools.ietf.org/html/rfc4122",
                    "value": f"{uuid4()}",
                }
            },
            "for": {
                "identifier": {
                    "system": "https://fhir.nhs.uk/Id/nhs-number",
                    "value": self.context.nhs_number,
                }
            },
            "authoredOn": "2022-11-21T14:30:00+00:00",
            "requester": {
                "reference": "#urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
            },
            "reasonCode": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "33633005",
                        "display": "Prescription of drug",
                    }
                ]
            },
        }
