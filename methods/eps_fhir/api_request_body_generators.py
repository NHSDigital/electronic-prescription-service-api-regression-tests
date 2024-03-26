import json
import uuid


def create_fhir_bundle(**kwargs):
    practitioner_role = kwargs["practitioner_role"]
    practitioner = kwargs["practitioner"]
    patient = kwargs["patient"]
    organization = kwargs["organization"]
    medication_request = kwargs["medication_request"]
    bundle_id = uuid.uuid4()
    fhir_bundle = {
        "resourceType": "Bundle",
        "id": "aef77afb-7e3c-427a-8657-2c427f71a271",
        "identifier": {
            "system": "https://tools.ietf.org/html/rfc4122",
            "value": bundle_id,
        },
        "type": "message",
    }
    if practitioner_role:
        fhir_bundle.update(practitioner_role)
    if practitioner:
        fhir_bundle.update(practitioner)
    if patient:
        fhir_bundle.update(patient)
    if organization:
        fhir_bundle.update(organization)
    if medication_request:
        fhir_bundle.update(medication_request)
    return json.dumps(fhir_bundle)


def generate_message_header(**kwargs):
    bundle_id = kwargs["bundle_id"]
    sender_ods_code = kwargs["sender_ods_code"]
    focus = kwargs["focus"]
    destination = kwargs["destination"]
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
    if destination:  # Nominated
        message_header.update(destination)
    if focus:
        message_header.update(focus)


def generate_medication_request(**kwargs):
    short_prescription_id = kwargs["short_prescription_id"]
    long_prescription_id = kwargs["long_prescription_id"]

    medication_request = {
        "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
        "resource": {
            "resourceType": "MedicationRequest",
            "identifier": [
                {
                    "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                    "value": "a9586fe5-b83d-4027-97a6-fe4821608640",  # TODO generate new one
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
                        "valueIdentifier": {
                            "value": long_prescription_id  # long form prescription ID
                        }
                    }
                ],
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
            # TODO generate this field for nominated/non-nominated (performer added if nominated, extension)
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
    return medication_request


def generate_practitioner_role(**kwargs):
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
                    "value": "12A3456B",
                },
            ],
            "organization": {
                "reference": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"
            },
        },
    }
    return practitioner_role


def generate_practitioner(**kwargs):
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


def generate_organization(**kwargs):
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
                }
            },
        },
    }
    return organization


# def prepare_new_prescription_body(**kwargs):
#     managing_organization_ods_code = kwargs["managing_organization_ods_code"]
#     primary_care_ods_id = kwargs["primary_care_ods_id")
#     gp_ods_code = kwargs["gp_ods_code"]
#     destination_ods_code = kwargs["destination_ods_code"]
#     order_item_1_number = uuid.uuid4()
#
#     nhs_number = kwargs.get("nhs_number")
#     prescription_id = generate_short_form_id(prescriber_ods_code=gp_ods_code)
#     data = {
#         "resourceType": "Bundle",
#         "id": "aef77afb-7e3c-427a-8657-2c427f71a271",
#         "identifier": {
#             "system": "https://tools.ietf.org/html/rfc4122",
#             "value": uuid.uuid4(),
#         },
#         "type": "message",
#         "entry": [
#             {
#                 "fullUrl": f"urn:uuid:aef77afb-7e3c-427a-8657-2c427f71a271",
#                 "resource": {
#                     "resourceType": "MessageHeader",
#                     "id": "3599c0e9-9292-413e-9270-9a1ef1ead99c",
#                     "eventCoding": {
#                         "system": "https://fhir.nhs.uk/CodeSystem/message-event",
#                         "code": "prescription-order",
#                         "display": "Prescription Order",
#                     },
#                     "sender": {
#                         "identifier": {
#                             "system": "https://fhir.nhs.uk/Id/ods-organization-code",
#                             "value": managing_organization_ods_code,
#                         },
#                         "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
#                         "display": "RAZIA|ALI",
#                     },
#                     "source": {
#                         "endpoint": f"urn:nhs-uk:addressing:ods:{managing_organization_ods_code}"
#                     },
#                     "destination": [
#                         {
#                             "endpoint": f"urn:nhs-uk:addressing:ods:{primary_care_ods_id}",
#                             "receiver": {
#                                 "identifier": {
#                                     "system": "https://fhir.nhs.uk/Id/ods-organization-code",
#                                     "value": primary_care_ods_id,
#                                 }
#                             },
#                         }
#                     ],
#                     "focus": [
#                         {"reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"},
#                         {"reference": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6"},
#                     ],
#                 },
#             },
#             {
#                 "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
#                 "resource": {
#                     "resourceType": "MedicationRequest",
#                     "id": "a54219b8-f741-4c47-b662-e4f8dfa49ab6",
#                     "extension": [
#                         {
#                             "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionType",
#                             "valueCoding": {
#                                 "system": "https://fhir.nhs.uk/CodeSystem/prescription-type",
#                                 "code": "1001",
#                                 "display": "Outpatient Community Prescriber - Medical Prescriber",
#                             },
#                         }
#                     ],
#                     "identifier": [
#                         {
#                             "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
#                             "value": order_item_1_number,
#                         }
#                     ],
#                     "status": "active",
#                     "intent": "order",
#                     "category": [
#                         {
#                             "coding": [
#                                 {
#                                     "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
#                                     "code": "outpatient",
#                                     "display": "Outpatient",
#                                 }
#                             ]
#                         }
#                     ],
#                     "medicationCodeableConcept": {
#                         "coding": [
#                             {
#                                 "system": "http://snomed.info/sct",
#                                 "code": "15517911000001104",
#                                 "display": "Methotrexate 10mg/0.2ml solution for injection pre-filled syringes",
#                             }
#                         ]
#                     },
#                     "subject": {
#                         "reference": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2"
#                     },
#                     "authoredOn": "2023-09-22T14:47:29+00:00",
#                     "requester": {
#                         "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
#                     },
#                     "groupIdentifier": {
#                         "extension": [
#                             {
#                                 "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
#                                 "valueIdentifier": {
#                                     "system": "https://fhir.nhs.uk/Id/prescription",
#                                     "value": "1dfb1898-70dd-42df-ace4-aa0fd83a501a",
#                                 },
#                             }
#                         ],
#                         "system": "https://fhir.nhs.uk/Id/prescription-order-number",
#                         "value": prescription_id,
#                     },
#                     "courseOfTherapyType": {
#                         "coding": [
#                             {
#                                 "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy",
#                                 "code": "acute",
#                                 "display": "Short course (acute) therapy",
#                             }
#                         ]
#                     },
#                     "dosageInstruction": [
#                         {
#                             "text": "Inject 10 milligram - 5 times a day - Subcutaneous route - for 10 days",
#                             "timing": {
#                                 "repeat": {
#                                     "frequency": 5,
#                                     "period": 1,
#                                     "periodUnit": "d",
#                                     "boundsDuration": {
#                                         "value": 10,
#                                         "unit": "day",
#                                         "system": "http://unitsofmeasure.org",
#                                         "code": "d",
#                                     },
#                                 }
#                             },
#                             "method": {
#                                 "coding": [
#                                     {
#                                         "system": "http://snomed.info/sct",
#                                         "code": "422145002",
#                                         "display": "Inject",
#                                     }
#                                 ]
#                             },
#                             "route": {
#                                 "coding": [
#                                     {
#                                         "system": "http://snomed.info/sct",
#                                         "code": "34206005",
#                                         "display": "Subcutaneous route",
#                                     }
#                                 ]
#                             },
#                             "doseAndRate": [
#                                 {
#                                     "doseQuantity": {
#                                         "value": 10,
#                                         "unit": "milligram",
#                                         "system": "http://unitsofmeasure.org",
#                                         "code": "mg",
#                                     }
#                                 }
#                             ],
#                         }
#                     ],
#                     "dispenseRequest": {
#                         "extension": [
#                             {
#                                 "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
#                                 "valueCoding": {
#                                     "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
#                                     "code": "P1",
#                                 },
#                             }
#                         ],
#                         "quantity": {
#                             "value": 1,
#                             "unit": "pre-filled disposable injection",
#                             "system": "http://snomed.info/sct",
#                             "code": "3318611000001103",
#                         },
#                         "performer": {
#                             "identifier": {
#                                 "system": "https://fhir.nhs.uk/Id/ods-organization-code",
#                                 "value": f"{destination_ods_code}",
#                             }
#                         },
#                     },
#                     "substitution": {"allowedBoolean": False},
#                 },
#             },
#             {
#                 "fullUrl": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2",
#                 "resource": {
#                     "resourceType": "Patient",
#                     "id": "78d3c2eb-009e-4ec8-a358-b042954aa9b2",
#                     "identifier": [
#                         {
#                             "system": "https://fhir.nhs.uk/Id/nhs-number",
#                             "value": f"{nhs_number}",
#                         }
#                     ],
#                     "name": [
#                         {
#                             "use": "usual",
#                             "family": "CORY",
#                             "given": ["ETTA"],
#                             "prefix": ["MISS"],
#                         }
#                     ],
#                     "gender": "female",
#                     "birthDate": "1999-01-04",
#                     "address": [
#                         {
#                             "use": "home",
#                             "line": ["123 Dale Avenue", "Long Eaton", "Nottingham"],
#                             "postalCode": "NG10 1NP",
#                         }
#                     ],
#                     "generalPractitioner": [
#                         {
#                             "identifier": {
#                                 "system": "https://fhir.nhs.uk/Id/ods-organization-code",
#                                 "value": gp_ods_code,
#                             }
#                         }
#                     ],
#                 },
#             },
#             {
#                 "fullUrl": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a",
#                 "resource": {
#                     "resourceType": "Practitioner",
#                     "id": "a8c85454-f8cb-498d-9629-78e2cb5fa47a",
#                     "identifier": [
#                         {
#                             "system": "https://fhir.nhs.uk/Id/sds-user-id",
#                             "value": "656005750108",
#                         },
#                         {
#                             "system": "https://fhir.hl7.org.uk/Id/nmc-number",
#                             "value": "12A3456B",
#                         },
#                     ],
#                     "name": [
#                         {"family": "Userq", "given": ["Random"], "prefix": ["MR"]}
#                     ],
#                 },
#             },
#             {
#                 "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
#                 "resource": {
#                     "resourceType": "PractitionerRole",
#                     "id": "56166769-c1c4-4d07-afa8-132b5dfca666",
#                     "identifier": [
#                         {
#                             "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
#                             "value": "100102238986",
#                         },
#                         {
#                             "system": "https://fhir.hl7.org.uk/Id/nhsbsa-spurious-code",
#                             "value": "12A3456B",
#                         },
#                     ],
#                     "practitioner": {
#                         "reference": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a"
#                     },
#                     "organization": {
#                         "reference": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"
#                     },
#                     "code": [
#                         {
#                             "coding": [
#                                 {
#                                     "system": "https://fhir.nhs.uk/CodeSystem/NHSDigital-SDS-JobRoleCode",
#                                     "code": "S8001:G8001:R8001",
#                                     "display": "Nurse Access Role",
#                                 }
#                             ]
#                         }
#                     ],
#                     "telecom": [
#                         {"system": "phone", "value": "01234567890", "use": "work"}
#                     ],
#                 },
#             },
#             {
#                 "fullUrl": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
#                 "resource": {
#                     "resourceType": "Organization",
#                     "id": "3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
#                     "identifier": [
#                         {
#                             "system": "https://fhir.nhs.uk/Id/ods-organization-code",
#                             "value": primary_care_ods_id,
#                         }
#                     ],
#                     "name": "SOMERSET BOWEL CANCER SCREENING CENTRE",
#                     "address": [
#                         {
#                             "use": "work",
#                             "line": ["MUSGROVE PARK HOSPITAL"],
#                             "city": "TAUNTON",
#                             "postalCode": "TA1 5DA",
#                         }
#                     ],
#                     "telecom": [
#                         {"system": "phone", "value": "01823 333444", "use": "work"}
#                     ],
#                     "partOf": {
#                         "identifier": {
#                             "system": "https://fhir.nhs.uk/Id/ods-organization-code",
#                             "value": managing_organization_ods_code,
#                         },
#                         "display": "TAUNTON AND SOMERSET NHS FOUNDATION TRUST",
#                     },
#                 },
#             },
#         ],
#     }
#     return data

if __name__ == "__main__":
    medication_request = generate_medication_request()
    print(create_fhir_bundle(medication_request=medication_request))
