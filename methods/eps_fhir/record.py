import uuid


message_header = {
    "resource": {
        "resourceType": "MessageHeader",
        "eventCoding": {
            "system": "https://fhir.nhs.uk/CodeSystem/message-event",
            "code": "prescription-order",
            "display": "Prescription Order",
        },
        "sender": {
            "identifier": {
                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                "value": "RBA",
            },
            "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",  # practitioner_role id
            "source": {"endpoint": "urn:nhs-uk:addressing:ods:RBA"},
        },
    }
}

medication_request = {
    "resource": {
        "resourceType": "MedicationRequest",
        "identifier": [
            {
                "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                "value": "{{order_item_1_number}}",
            }
        ],
        "status": "active",
        "intent": "order",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                        "code": "outpatient",
                    }
                ]
            }
        ],
        "medicationCodeableConcept": {
            "coding": [
                {"system": "http://snomed.info/sct", "code": "15517911000001104"}
            ]
        },
        "subject": {"reference": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2"},
        "requester": {
            "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"  # practitioner_role id
        },
        "groupIdentifier": {
            "extension": [
                {"valueIdentifier": {"value": "1dfb1898-70dd-42df-ace4-aa0fd83a501a"}}
            ],
            "value": "{{prescription_id}}",
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
                "text": "Inject 10 milligram - 5 times a day - Subcutaneous route - for 10 days",
                "timing": {
                    "repeat": {
                        "frequency": 5,
                        "period": 1,
                        "periodUnit": "d",
                        "boundsDuration": {
                            "value": 10,
                            "unit": "day",
                            "system": "http://unitsofmeasure.org",
                            "code": "d",
                        },
                    }
                },
                "route": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "34206005",
                            "display": "Subcutaneous route",
                        }
                    ]
                },
                "doseAndRate": [
                    {
                        "doseQuantity": {
                            "value": 10,
                            "unit": "milligram",
                            "system": "http://unitsofmeasure.org",
                            "code": "mg",
                        }
                    }
                ],
            }
        ],
        "dispenseRequest": {
            "quantity": {
                "value": 1,
                "unit": "pre-filled disposable injection",
                "system": "http://snomed.info/sct",
                "code": "3318611000001103",
            },
        },
        "substitution": {"allowedBoolean": False},
    }
}

patient = {
    "resource": {
        "resourceType": "Patient",
        "identifier": [
            {"system": "https://fhir.nhs.uk/Id/nhs-number", "value": "{{nhs_number}}"}
        ],
        "name": [
            {"use": "usual", "family": "CORY", "given": ["ETTA"], "prefix": ["MISS"]}
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
                    "value": "B81001",
                }
            }
        ],
    }
}

practitioner = {
    "fullUrl": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a",
    "resource": {
        "resourceType": "Practitioner",
        "id": "a8c85454-f8cb-498d-9629-78e2cb5fa47a",
        "identifier": [
            {"system": "https://fhir.nhs.uk/Id/sds-user-id", "value": "{{user_id}}"},
            {"system": "https://fhir.hl7.org.uk/Id/nmc-number", "value": "12A3456B"},
        ],
        "name": [{"family": "Userq", "given": ["Random"], "prefix": ["MR"]}],
    },
}

practitioner_role = {
    "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",  # practitioner_role id
    "resource": {
        "resourceType": "PractitionerRole",
        "id": "56166769-c1c4-4d07-afa8-132b5dfca666",  # practitioner_role id
        "identifier": [
            {
                "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                "value": "100102238986",
            },
            {
                "system": "https://fhir.hl7.org.uk/Id/nhsbsa-spurious-code",
                "value": "12A3456B",
            },
        ],
        # "practitioner": {
        #     "reference": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a" #practitioner id
        # },
        "organization": {"reference": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"},
        "code": [
            {
                "coding": [
                    {
                        "system": "https://fhir.nhs.uk/CodeSystem/NHSDigital-SDS-JobRoleCode",
                        "code": "S8001:G8001:R8001",
                    }
                ]
            }
        ],
        "telecom": [{"value": "01234567890", "use": "work"}],
    },
}

organisation = {
    "resource": {
        "resourceType": "Organization",
        "identifier": [
            {
                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                "value": "A99968",
            }
        ],
        "partOf": {
            "identifier": {
                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                "value": "RBA",
            }
        },
    }
}

data = {
    "resourceType": "Bundle",
    "identifier": {
        "system": "https://tools.ietf.org/html/rfc4122",
        "value": uuid.uuid4(),
    },
    "type": "message",
    "entry": [
        {
            message_header,  # pyright: ignore [reportUnhashable]
            medication_request,  # pyright: ignore [reportUnhashable]
            patient,  # pyright: ignore [reportUnhashable]
            practitioner,  # pyright: ignore [reportUnhashable]
            practitioner_role,  # pyright: ignore [reportUnhashable]
            organisation,  # pyright: ignore [reportUnhashable]
        }
    ],
}
