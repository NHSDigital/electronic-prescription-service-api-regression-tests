import json
import uuid

from features.environment import CIS2_USERS


def create_fhir_bundle(*entries):
    resource_id = str(uuid.uuid4())
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


def create_fhir_parameter(*entries):
    fhir_resource = {
        "resourceType": "Parameters",
        "id": str(uuid.uuid4()),
        "parameter": [{"name": "status", "valueCode": "accepted"}],
    }
    fhir_resource["parameter"].extend(entries)
    return json.dumps(fhir_resource)


def generate_message_header(sender_ods_code, receiver_ods_code):
    bundle_id = uuid.uuid4()
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
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": sender_ods_code,
                },
            },
            "source": {"endpoint": f"urn:nhs-uk:addressing:ods:{sender_ods_code}"},
        },
    }

    if receiver_ods_code:  # Nominated
        message_header["resource"].update(
            {
                "destination": [
                    {
                        "endpoint": "https://sandbox.api.service.nhs.uk/electronic-prescriptions/$post-message",
                        "receiver": {
                            "identifier": {
                                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                "value": receiver_ods_code,
                            }
                        },
                    }
                ]
            },
        )
    return message_header


def generate_medication_request(
    short_prescription_id,
    prescription_item_id,
    long_prescription_id,
    receiver_ods_code,
    code,
):
    medication_request = {
        "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
        "resource": {
            "resourceType": "MedicationRequest",
            "extension": [
                # mandatory
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
                    "value": prescription_item_id,
                }
            ],
            "status": "active",  # must be consistent
            "intent": "order",  # must be consistent
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                            "code": ("community"),
                            # primary-care : "community"
                            # but secondary-care: "inpatient"/"outpatient"
                        }  # must be consistent
                    ]
                }
            ],
            "medicationCodeableConcept": {
                "coding": [{"system": "http://snomed.info/sct", "code": "322237000"}]
            },
            "subject": {
                "reference": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2"  # patient
            },
            "requester": {
                "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"  # practitioner_role id
            },
            "groupIdentifier": {
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",  # mandatory value
                        "valueIdentifier": {
                            "system": "https://fhir.nhs.uk/Id/prescription",
                            # mandatory value minimum required = 1, but only found 0
                            "value": long_prescription_id,  # long form prescription ID
                        },
                    }
                ],
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                # also mandatory minimum required = 1, but only found 0
                "value": short_prescription_id,  # short from prescription ID
            },
            "courseOfTherapyType": {
                "coding": [
                    {
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
                                "system": "http://snomed.info/sct",
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
                    "system": "http://unitsofmeasure.org",
                    "code": "d",
                },
                "quantity": {
                    "value": 100,
                    "unit": "tablet",
                    "system": "http://snomed.info/sct",
                    "code": "428673006",
                },
            },
            "substitution": {"allowedBoolean": False},
        },
    }

    if code == "P1":  # Nominated
        medication_request["resource"]["dispenseRequest"].update(
            {
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
                        "valueCoding": {
                            "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
                            "code": code,
                        },
                    }
                ],
                "performer": {
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": receiver_ods_code,
                    }
                },
            }
        )

    if code == "0004":
        medication_request["resource"]["dispenseRequest"].update(
            {
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
                        "valueCoding": {
                            "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
                            "code": code,
                        },
                    }
                ],
            }
        )

    return medication_request


def generate_practitioner_role(sds_role_id):
    return {
        "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
        "resource": {
            "resourceType": "PractitionerRole",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                    "value": sds_role_id,
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


def generate_practitioner(user_id):
    return {
        "fullUrl": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a",
        "resource": {
            "resourceType": "Practitioner",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-user-id",
                    "value": user_id,
                },
                {
                    "system": "https://fhir.hl7.org.uk/Id/nmc-number",
                    "value": "999999",
                },
            ],
            "name": [{"family": "BOIN", "given": ["C"], "prefix": ["DR"]}],
        },
    }


def generate_patient(nhs_number, gp_ods_code):
    return {
        "fullUrl": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2",
        "resource": {
            "resourceType": "Patient",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/nhs-number",
                    "value": nhs_number,
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
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": gp_ods_code,
                    }
                }
            ],
        },
    }


def generate_organization():
    return {
        "fullUrl": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",  # del
        "resource": {
            "resourceType": "Organization",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": "A83008",
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
            "partOf": {  # del
                "identifier": {
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": "RBA",
                },
                "display": "TAUNTON AND SOMERSET NHS FOUNDATION TRUST",  # mandatory
            },
        },
    }


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
