import json
import uuid


def create_fhir_bundle(**kwargs):
    bundle_id = str(uuid.uuid4())
    fhir_bundle = {
        "resourceType": "Bundle",
        "id": "aef77afb-7e3c-427a-8657-2c427f71a271",
        "identifier": {
            "system": "https://tools.ietf.org/html/rfc4122",
            "value": bundle_id,
        },
        "type": "message",
        "entry": [],
    }

    if kwargs.get("message_header"):
        fhir_bundle["entry"].append(kwargs["message_header"])
    if kwargs.get("practitioner_role"):
        fhir_bundle["entry"].append(kwargs["practitioner_role"])
    if kwargs.get("practitioner"):
        fhir_bundle["entry"].append(kwargs["practitioner"])
    if kwargs.get("patient"):
        fhir_bundle["entry"].append(kwargs["patient"])
    if kwargs.get("organization"):
        fhir_bundle["entry"].append(kwargs["organization"])
    if kwargs.get("medication_request"):
        fhir_bundle["entry"].append(kwargs["medication_request"])

    return json.dumps(fhir_bundle)


def generate_message_header(**kwargs):
    bundle_id = kwargs["bundle_id"]
    sender_ods_code = kwargs["sender_ods_code"]
    # focus = kwargs["focus"]
    # destination = kwargs["destination"]
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
                "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
                "display": "RAZIA|ALI",
            },
            "source": {"endpoint": f"urn:nhs-uk:addressing:ods:{sender_ods_code}"},
        },
    }
    # if destination:  # Nominated
    #     message_header.update(destination)
    # if focus:
    #     message_header.update(focus)
    return message_header


def generate_medication_request(**kwargs):
    short_prescription_id = kwargs["short_prescription_id"]
    long_prescription_id = kwargs["long_prescription_id"]
    code = kwargs["code"]
    identifier_value = str(uuid.uuid4())

    medication_request = {
        "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
        "resource": {
            "resourceType": "MedicationRequest",
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
                            "code": "outpatient",
                            # primary-care : "community"
                            # but secondary-care: "inpatient"/"outpatient"
                        }  # must be consistent
                    ]
                }
            ],
            "medicationCodeableConcept": {
                "coding": [
                    {"system": "http://snomed.info/sct", "code": "15517911000001104"}
                ]
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
                        "value": "FH542",
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


def generate_practitioner_role():
    practitioner_role = {
        "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
        "resource": {
            "resourceType": "PractitionerRole",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                    "value": "100102238986",
                },
                {
                    "system": "https://fhir.hl7.org.uk/Id/nhsbsa-spurious-code",
                    "value": "G6123456",  # needs to be of G6NNNNNN or G7NNNNNN
                },
            ],
            "practitioner": {
                "reference": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a"
            },  # mandatory if there is a practitioner
            "organization": {
                "reference": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"
            },
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
                    "value": "555086689106",
                },
                {
                    "system": "https://fhir.hl7.org.uk/Id/nmc-number",
                    "value": "12A3456B",
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
                        "value": "B81001",
                    }
                }
            ],
        },
    }
    return patient


def generate_organization():
    organization = {
        "fullUrl": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
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
                },
                "display": "TAUNTON AND SOMERSET NHS FOUNDATION TRUST",  # mandatory
            },
        },
    }
    return organization


def find_sets(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, set):
                print(f"Found set in {key}")
            elif isinstance(value, (list, tuple)):
                for item in value:
                    find_sets(item)
            elif isinstance(value, dict):
                find_sets(value)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            find_sets(item)


if __name__ == "__main__":
    msg_header = generate_message_header(
        bundle_id="aef77afb-7e3c-427a-8657-2c427f71a271", sender_ods_code="RBA"
    )
    med_request = generate_medication_request(
        short_prescription_id="F9B761-0X2602-9691EI",
        long_prescription_id="a9586fe5-b83d-4027-97a6-fe4821608640",
        code="0004",
    )
    patnt = generate_patient(nhs_number="9282511006")
    org = generate_organization()
    pract_role = generate_practitioner_role()
    pract = generate_practitioner()
    bundle = create_fhir_bundle(
        message_header=msg_header,
        medication_request=med_request,
        organization=org,
        practitioner_role=pract_role,
        practitioner=pract,
        patient=patnt,
    )
    print(bundle)

# TO DO add focus with practitioner role and med red
# compare the example with the bundle to find out what is wrong with system
