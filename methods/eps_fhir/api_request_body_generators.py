from datetime import datetime, timedelta, timezone
import json
import uuid

three_months_later = datetime.today() + timedelta(days=3 * 30)

later_date = three_months_later.strftime("%Y-%m-%d")


def create_fhir_resource(resource_type, main_keys, **kwargs):
    resource_id = str(uuid.uuid4())
    fhir_resource = {
        "resourceType": resource_type,
        "id": resource_id,
    }

    if resource_type == "Bundle":
        fhir_resource.update(
            {
                "identifier": {
                    "system": "https://tools.ietf.org/html/rfc4122",
                    "value": resource_id,
                },
                "type": "message",
                "entry": [],
            }
        )
        main_key = "entry"
    if resource_type == "Parameters":
        fhir_resource["parameter"] = [
            {"name": "status", "valueCode": "accepted"},
        ]
        main_key = "parameter"

    for key in main_keys:
        if kwargs.get(key):
            fhir_resource[
                main_key  # pyright: ignore[reportPossiblyUnboundVariable]
            ].append(kwargs[key])
    return json.dumps(fhir_resource)


def create_fhir_bundle(**kwargs):
    return create_fhir_resource(
        "Bundle",
        [
            "message_header",
            "practitioner_role",
            "practitioner",
            "patient",
            "organization",
            "medication_request",
        ],
        **kwargs,
    )


def create_fhir_signed_bundle(**kwargs):
    return create_fhir_resource(
        "Bundle",
        [
            "message_header",
            "practitioner_role",
            "practitioner",
            "patient",
            "organization",
            "medication_request",
            "provenance",
        ],
        **kwargs,
    )


def create_fhir_parameter(**kwargs):
    return create_fhir_resource(
        "Parameters",
        [
            "group_identifier",
            "owner",
            "agent",
        ],
        **kwargs,
    )


def generate_message_header(**kwargs):
    bundle_id = uuid.uuid4()
    sender_ods_code = kwargs["sender_ods_code"]
    receiver_ods_code = kwargs["receiver_ods_code"]
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


def generate_medication_request(**kwargs):
    short_prescription_id = kwargs["short_prescription_id"]
    long_prescription_id = str(uuid.uuid4())
    code = kwargs["code"]
    identifier_value = str(uuid.uuid4())

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
                    "value": identifier_value,
                }
            ],
            "status": "active",  # must be consistent
            "intent": "order",  # must be consistent
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                            "code": "community",
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
                "validityPeriod": {
                    "start": datetime.today().strftime("%Y-%m-%d"),
                    "end": later_date,
                },
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

    # if code == "P1":  # Nominated
    #     medication_request["resource"]["dispenseRequest"].update(
    #         {
    #             "extension": [
    #                 {
    #                     "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
    #                     "valueCoding": {
    #                         "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
    #                         "code": code,
    #                     },
    #                 }
    #             ],
    #             "performer": {
    #                 "identifier": {
    #                     "system": "https://fhir.nhs.uk/Id/ods-organization-code",
    #                     "value": "VNE51",
    #                 }
    #             },
    #         }
    #     )
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


def generate_practitioner_role():
    practitioner_role = {
        "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
        "resource": {
            "resourceType": "PractitionerRole",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                    "value": "555086415105",
                }
            ],
            "practitioner": {
                "reference": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a"
            },  # mandatory if there is a practitioner
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
    return practitioner_role


def generate_practitioner():
    practitioner = {
        "fullUrl": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a",
        "resource": {
            "resourceType": "Practitioner",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-user-id",
                    "value": "3415870201",
                },
                {
                    "system": "https://fhir.hl7.org.uk/Id/nmc-number",
                    "value": "999999",
                },
            ],
            "name": [{"family": "BOIN", "given": ["C"], "prefix": ["DR"]}],
        },
    }
    return practitioner


def generate_patient(**kwargs):
    nhs_number = kwargs["nhs_number"]
    patient = {
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
                        "value": "RBA",
                    }
                }
            ],
        },
    }
    return patient


def generate_organization():
    organization = {
        "fullUrl": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",  # del
        "resource": {
            "resourceType": "Organization",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": "A99968",
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
    return organization


def generate_provenance(**kwargs):
    signature = kwargs["signature"]
    provenance = {
        "fullUrl": "urn:uuid:28828c55-8fa7-42d7-916f-fcf076e0c10e",
        "resource": {
            "resourceType": "Provenance",
            "target": [{"reference": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6"}],
            "recorded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
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
                    "when": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S+00:00"
                    ),
                    "who": {
                        "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
                    },
                    "data": signature,
                }
            ],
        },
    }
    return provenance


def generate_owner():
    owner = {
        "name": "owner",
        "resource": {
            "resourceType": "Organization",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                    "value": "A99968",
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
    return owner


def generate_agent():
    agent = {
        "name": "agent",
        "resource": {
            "resourceType": "PractitionerRole",
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
    return agent


def generate_group_identifier(**kwargs):
    prescription_order_number = kwargs["prescription_order_number"]
    group_identifier = {
        "name": "group-identifier",
        "valueIdentifier": {
            "system": "https://fhir.nhs.uk/Id/prescription-order-number",
            "value": prescription_order_number,
        },
    }
    return group_identifier
