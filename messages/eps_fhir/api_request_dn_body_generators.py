import uuid


def create_dispense_notification(*entries):
    return {
        "resourceType": "Bundle",
        "type": "message",
        "entry": entries,
        "identifier": {
            "system": "https://tools.ietf.org/html/rfc4122",
            "value": str(uuid.uuid4()),
        },
    }


def create_dn_message_header(receiver_ods_code):
    return {
        "fullUrl": f"urn:uuid:{uuid.uuid4()}",
        "resource": {
            "resourceType": "MessageHeader",
            "eventCoding": {
                "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                "code": "dispense-notification",
                "display": "Dispense Notification",
            },
            "source": {"endpoint": f"urn:nhs-uk:addressing:ods:{receiver_ods_code}"},
            "response": {
                "identifier": str(uuid.uuid4()),
                "code": "ok",
            },
        },
    }


def create_dn_medication_dispense(
    medication_dispense_uuid,
    nhs_number,
    practitioner_role_uuid,
    practitioner_role,
    medication_request_uuid,
    medication_request,
    prescription_item_uuid,
):
    return {
        "fullUrl": f"urn:uuid:{medication_dispense_uuid}",
        "resource": {
            "resourceType": "MedicationDispense",
            "medicationCodeableConcept": {
                "coding": [{"system": "http://snomed.info/sct", "code": "322237000"}]
            },
            "subject": {
                "type": "Patient",
                "identifier": {
                    "system": "https://fhir.nhs.uk/Id/nhs-number",
                    "value": nhs_number,
                },
                "display": "MR DONOTUSE XXTESTPATIENT-TGNP",
            },
            "status": "completed",
            "extension": [
                {
                    "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-TaskBusinessStatus",
                    "valueCoding": {
                        "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-business-status",
                        "code": "0003",
                        "display": "With Dispenser - Active",
                    },
                }
            ],
            "performer": [
                {"actor": {"reference": f"#urn:uuid:{practitioner_role_uuid}"}}
            ],
            "authorizingPrescription": [
                {"reference": f"#urn:uuid:{medication_request_uuid}"}
            ],
            "quantity": {
                "value": 1,
                "unit": "pre-filled disposable injection",
                "system": "http://snomed.info/sct",
                "code": "3318611000001103",
            },
            "contained": [practitioner_role, medication_request],
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/prescription-dispense-item-number",
                    "value": prescription_item_uuid,
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
            "whenHandedOver": "2021-05-07T14:47:29+00:00",
        },
    }


def create_dn_organisation(organisation_uuid, receiver_ods_code):
    return {
        "fullUrl": f"urn:uuid:{organisation_uuid}",
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
                    "value": receiver_ods_code,
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
            "telecom": [{"system": "phone", "use": "work", "value": "0113 3180277"}],
        },
    }


def create_dn_practitioner_role(practitioner_role_uuid, organisation_uuid):
    return {
        "resourceType": "PractitionerRole",
        "id": f"urn:uuid:{practitioner_role_uuid}",
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
        "organization": {"reference": f"urn:uuid:{organisation_uuid}"},
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


def create_dn_medication_request(
    medication_request_uuid,
    prescription_item_uuid,
    patient_uuid,
    prescription_uuid,
    prescription_id,
    practitioner_role_uuid,
):
    return {
        "resourceType": "MedicationRequest",
        "id": f"urn:uuid:{medication_request_uuid}",
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
                "value": prescription_item_uuid,
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
                        "display": "Outpatient",
                    }
                ]
            }
        ],
        "medicationCodeableConcept": {
            "coding": [{"system": "http://snomed.info/sct", "code": "322237000"}]
        },
        "subject": {"reference": f"urn:uuid:{patient_uuid}"},
        "authoredOn": "2021-05-07T14:47:29+00:00",
        "requester": {"reference": f"urn:uuid:{practitioner_role_uuid}"},
        "groupIdentifier": {
            "extension": [
                {
                    "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                    "valueIdentifier": {
                        "system": "https://fhir.nhs.uk/Id/prescription",
                        "value": prescription_uuid,
                    },
                }
            ],
            "system": "https://fhir.nhs.uk/Id/prescription-order-number",
            "value": prescription_id,
        },
        "courseOfTherapyType": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy",
                    "code": "acute",
                    "display": "Short course (acute) therapy",
                }
            ]
        },
        "dosageInstruction": [
            {
                "text": "4 times a day - Oral",
                "timing": {"repeat": {"frequency": 4, "period": 1, "periodUnit": "d"}},
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
    }
