from datetime import UTC, datetime
from uuid import uuid4
from features.environment import CIS2_USERS


def create_task(
    task_id,
    practitioner_role_id,
    organization_id,
    sender_ods_code,
    prescription_id,
    focus_id,
    nhs_number,
    status_reason,
    code,
    status,
):
    return {
        "resourceType": "Task",
        "id": str(task_id),
        "contained": [
            {
                "resourceType": "PractitionerRole",
                "id": f"{practitioner_role_id}",
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
                "organization": {"reference": f"#{organization_id}"},
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
            },
            {
                "resourceType": "Organization",
                "id": f"{organization_id}",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": sender_ods_code,
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
                "value": str(uuid4()),
            }
        ],
        "status": status,
        "statusReason": status_reason,
        "intent": "order",
        "code": code,
        "groupIdentifier": {
            "system": "https://fhir.nhs.uk/Id/prescription-order-number",
            "value": prescription_id,
        },
        "focus": {
            "identifier": {
                "system": "https://tools.ietf.org/html/rfc4122",
                "value": str(focus_id),
            }
        },
        "for": {
            "identifier": {
                "system": "https://fhir.nhs.uk/Id/nhs-number",
                "value": nhs_number,
            }
        },
        "authoredOn": datetime.now(UTC).isoformat(),
        "requester": {"reference": f"urn:uuid:{practitioner_role_id}"},
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
