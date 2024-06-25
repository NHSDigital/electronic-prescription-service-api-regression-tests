from dataclasses import dataclass
from datetime import UTC, datetime
import json
from typing import Any
from uuid import uuid4

from features.environment import CIS2_USERS


@dataclass
class ReturnIDs:
    practitioner_role = uuid4()
    organization = uuid4()


class Return:
    def __init__(self, context: Any) -> None:
        ids = ReturnIDs()
        body = self.generate_return(ids, context)
        self.body = json.dumps(body)

    def generate_return(self, ids: ReturnIDs, context):
        return {
            "resourceType": "Task",
            "id": f"{uuid4()}",
            "contained": [
                {
                    "resourceType": "PractitionerRole",
                    "id": f"urn:uuid:{ids.practitioner_role}",
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
                    "organization": {"reference": f"#urn:uuid:{ids.organization}"},
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
                    "id": f"urn:uuid:{ids.organization}",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                            "value": context.sender_ods_code,
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
                        "system": "http://hl7.org/fhir/CodeSystem/task-code",  # http only
                        "code": "fulfill",
                        "display": "Fulfill the focal request",
                    }
                ]
            },
            "groupIdentifier": {
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                "value": context.prescription_id,
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
                    "value": context.nhs_number,
                }
            },
            "authoredOn": datetime.now(UTC).isoformat(),
            "requester": {"reference": f"#urn:uuid:{ids.practitioner_role}"},
            "reasonCode": {
                "coding": [
                    {
                        "system": "https://snomed.info/sct",
                        "code": "33633005",
                        "display": "Prescription of drug",
                    }
                ]
            },
        }
