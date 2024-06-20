import json
import uuid

from features.environment import CIS2_USERS


def create_fhir_parameter(*entries):
    fhir_resource = {
        "resourceType": "Parameters",
        "id": str(uuid.uuid4()),
        "parameter": [{"name": "status", "valueCode": "accepted"}],
    }
    fhir_resource["parameter"].extend(entries)
    return json.dumps(fhir_resource)


def generate_provenance(signature, timestamp):
    return {
        "fullUrl": "urn:uuid:28828c55-8fa7-42d7-916f-fcf076e0c10e",
        "resource": {
            "resourceType": "Provenance",
            "target": [{"reference": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6"}],
            "recorded": "2008-02-27T11:38:00+00:00",
            "agent": [
                {
                    "who": {
                        # practitioner-role
                        "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
                    }
                }
            ],
            "signature": [
                {
                    "type": [
                        {
                            "system": "urn:iso-astm:E1762-95:2013",
                            "code": "1.2.840.10065.1.12.1.1",
                        }
                    ],
                    "when": timestamp,
                    "who": {
                        "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
                    },
                    "data": signature,
                }
            ],
        },
    }


def generate_owner(receiver_ods_code):
    return {
        "name": "owner",
        "resource": {
            "resourceType": "Organization",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": receiver_ods_code,
                }
            ],
            "active": True,
            "type": [
                {
                    "coding": [
                        {
                            "system": "https://fhir.nhs.uk/CodeSystem/organisation-role",
                            "code": "123",
                        }
                    ]
                }
            ],
            "name": "SOMERSET BOWEL CANCER SCREENING CENTRE",  # mandatory
            "address": [
                {
                    "use": "work",
                    "line": ["MUSGROVE PARK HOSPITAL"],
                    "city": "TAUNTON",
                    "postalCode": "TA1 5DA",
                }
            ],  # mandatory
            "telecom": [
                {"system": "phone", "value": "01823 333444", "use": "work"}
            ],  # mandatory
        },
    }


def generate_agent():
    return {
        "name": "agent",
        "resource": {
            "resourceType": "PractitionerRole",
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


def generate_group_identifier(prescription_order_number):
    return {
        "name": "group-identifier",
        "valueIdentifier": {
            "system": "https://fhir.nhs.uk/Id/prescription-order-number",
            "value": prescription_order_number,
        },
    }


def generate_return(nhs_number, short_prescription_id):
    return {
        "resourceType": "Task",
        "id": f"{uuid.uuid4()}",
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
                "telecom": [{"system": "phone", "use": "work", "value": "02380798431"}],
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
                "value": f"{uuid.uuid4()}",
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
            "value": short_prescription_id,
        },
        "focus": {
            "identifier": {
                "system": "https://tools.ietf.org/html/rfc4122",
                "value": f"{uuid.uuid4()}",
            }
        },
        "for": {
            "identifier": {
                "system": "https://fhir.nhs.uk/Id/nhs-number",
                "value": nhs_number,
            }
        },
        "authoredOn": "2022-11-21T14:30:00+00:00",
        "requester": {"reference": "#urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"},
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
