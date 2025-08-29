from datetime import date, datetime, UTC, timedelta
import json
from typing import TypedDict, NotRequired
from uuid import uuid4
from messages.eps_fhir.common_maps import (
    STATUS_MAP,
    LINE_ITEM_STATUS_MAP,
    INTENT_MAP,
    THERAPY_TYPE_MAP,
    NON_DISPENSING_REASON_MAP,
)


class DNProps(TypedDict):
    nhs_number: str
    prescription_id: str
    long_prescription_id: str
    prescription_type: str
    status: str
    line_item_id: str
    line_item_status: str
    quantity: int
    quantity_unit: str
    receiver_ods: str
    is_amendment: bool
    previous_dn_id: NotRequired[str]
    non_dispensing_reason: NotRequired[str]


# TODO: Add support for multiple line items
class DispenseNotification:
    def __init__(self, dn_props: DNProps) -> None:
        self.HTTP_SNOMED_INFO_SCT = "http://snomed.info/sct"

        self.practitioner_role_id = uuid4()
        self.organization_id = uuid4()
        practitioner_role = self.practitioner_role()

        self.medication_request_id = uuid4()
        medication_request = self.medication_request(dn_props)

        medication_dispense = self.medication_dispense(
            dn_props, practitioner_role, medication_request
        )

        message_header = self.message_header(dn_props["receiver_ods"])
        if dn_props["is_amendment"] and "previous_dn_id" in dn_props:
            message_header["resource"]["extension"] = self.replacement_extension(
                dn_props["previous_dn_id"]
            )

        organization = self.organization(dn_props["receiver_ods"])

        self.dispense_notification_id = str(uuid4())
        dispense_notification = self.dispense_notification(
            message_header, medication_dispense, organization
        )

        self.body = json.dumps(dispense_notification)

    def practitioner_role(self):
        return {
            "resourceType": "PractitionerRole",
            "id": f"{self.practitioner_role_id}",
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
            "organization": {"reference": f"urn:uuid:{self.organization_id}"},
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

    def medication_request(self, dn_props: DNProps):
        medication_request = {
            "resourceType": "MedicationRequest",
            "id": f"{self.medication_request_id}",
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
                    "value": dn_props["line_item_id"],
                }
            ],
            "status": "active",
            "intent": INTENT_MAP[dn_props["prescription_type"]],
            "category": [
                {
                    "coding": [
                        {
                            "system": "https://terminology.hl7.org/CodeSystem/medicationrequest-category",
                            "code": "outpatient",
                            "display": "Outpatient",
                        }
                    ]
                }
            ],
            "medicationCodeableConcept": {
                "coding": [
                    {
                        "system": self.HTTP_SNOMED_INFO_SCT,  # http only
                        "code": "322237000",
                    }
                ]
            },
            "subject": {"reference": f"urn:uuid:{uuid4()}"},
            "authoredOn": datetime.now(UTC).isoformat(),
            "requester": {"reference": f"urn:uuid:{self.practitioner_role_id}"},
            "groupIdentifier": {
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                        "valueIdentifier": {
                            "system": "https://fhir.nhs.uk/Id/prescription",
                            "value": dn_props["long_prescription_id"],
                        },
                    }
                ],
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                "value": dn_props["prescription_id"],
            },
            "courseOfTherapyType": {
                "coding": [
                    {
                        "system": "https://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy",
                        "code": THERAPY_TYPE_MAP[dn_props["prescription_type"]]["code"],
                        "display": THERAPY_TYPE_MAP[dn_props["prescription_type"]][
                            "display"
                        ],
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
                                "system": "https://snomed.info/sct",
                                "code": "26643006",
                                "display": "Oral",
                            }
                        ]
                    },
                }
            ],
            "dispenseRequest": {
                "validityPeriod": {
                    "start": str(date.today()),
                    "end": str(date.today() + timedelta(days=1)),
                },
                "expectedSupplyDuration": {
                    "value": 30,
                    "unit": "day",
                    "system": "http://unitsofmeasure.org",  # http only
                    "code": "d",
                },
                "quantity": {
                    "value": 100,
                    "unit": "tablet",
                    "system": "https://snomed.info/sct",
                    "code": "428673006",
                },
            },
            "substitution": {"allowedBoolean": False},
        }

        if dn_props["prescription_type"] == "eRD":
            medication_request["extension"].append(
                {
                    "url": "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-MedicationRepeatInformation",  # noqa: E501
                    "extension": [
                        {
                            "url": "authorisationExpiryDate",
                            "valueDateTime": str(date.today() + timedelta(days=30)),
                        },
                        {
                            "url": "numberOfPrescriptionsIssued",
                            "valueUnsignedInt": 1,
                        },
                    ],
                }
            )

            medication_request["dispenseRequest"]["expectedSupplyDuration"] = {
                "unit": "days",
                "value": 10,
                "system": "http://unitsofmeasure.org",
                "code": "d",
            }

        if dn_props["prescription_type"] != "acute":
            medication_request["dispenseRequest"]["numberOfRepeatsAllowed"] = "6"

            medication_request["basedOn"] = [
                {
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-RepeatInformation",  # noqa: E501
                            "extension": [
                                {
                                    "url": "numberOfRepeatsAllowed",
                                    "valueInteger": 6,
                                },
                                {
                                    "url": "numberOfRepeatsIssued",
                                    "valueInteger": 0,
                                },
                            ],
                        }
                    ],
                }
            ]

        return medication_request

    def medication_dispense(
        self, dn_props: DNProps, practitioner_role, medication_request
    ):
        medication_dispense = {
            "fullUrl": f"urn:uuid:{uuid4()}",
            "resource": {
                "resourceType": "MedicationDispense",
                "medicationCodeableConcept": {
                    "coding": [
                        {
                            "system": self.HTTP_SNOMED_INFO_SCT,
                            "code": "322237000",
                            "display": "Paracetamol 500mg soluble tablet (product)",
                        }
                    ]
                },
                "subject": {
                    "type": "Patient",
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": dn_props["nhs_number"],
                    },
                    "display": "MR DONOTUSE XXTESTPATIENT-TGNP",
                },
                "status": "completed",
                "extension": [
                    {
                        "url": "https://fhir.nhs.uk/StructureDefinition/Extension-EPS-TaskBusinessStatus",
                        "valueCoding": {
                            "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-business-status",
                            "code": STATUS_MAP[dn_props["status"]],
                            "display": dn_props["status"],
                        },
                    }
                ],
                "performer": [
                    {"actor": {"reference": f"#{self.practitioner_role_id}"}}
                ],
                "authorizingPrescription": [
                    {"reference": f"#{self.medication_request_id}"}
                ],
                "quantity": {
                    "value": dn_props["quantity"],
                    "unit": dn_props["quantity_unit"],
                    "system": self.HTTP_SNOMED_INFO_SCT,
                    "code": "3318611000001103",
                },
                "contained": [practitioner_role, medication_request],
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/prescription-dispense-item-number",
                        "value": dn_props["line_item_id"],
                    }
                ],
                "type": {
                    "coding": [
                        {
                            "system": "https://fhir.nhs.uk/CodeSystem/medicationdispense-type",
                            "code": LINE_ITEM_STATUS_MAP[dn_props["line_item_status"]],
                            "display": dn_props["line_item_status"],
                        }
                    ]
                },
                "dosageInstruction": [{"text": "4 times a day - Oral"}],
                "whenHandedOver": datetime.now(UTC).isoformat(),
            },
        }

        if (
            dn_props["line_item_status"] == "Item not dispensed"
            and "non_dispensing_reason" in dn_props
        ):
            medication_dispense["resource"]["statusReasonCodeableConcept"] = {
                "coding": [
                    {
                        "system": "https://fhir.nhs.uk/CodeSystem/medicationdispense-status-reason",
                        "code": NON_DISPENSING_REASON_MAP[
                            dn_props["non_dispensing_reason"]
                        ],
                        "display": dn_props["non_dispensing_reason"],
                    }
                ]
            }

        return medication_dispense

    def message_header(self, receiver_ods):
        return {
            "fullUrl": f"urn:uuid:{uuid4()}",
            "resource": {
                "resourceType": "MessageHeader",
                "eventCoding": {
                    "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                    "code": "dispense-notification",
                    "display": "Dispense Notification",
                },
                "source": {"endpoint": f"urn:nhs-uk:addressing:ods:{receiver_ods}"},
                "response": {
                    "identifier": str(uuid4()),
                    "code": "ok",
                },
            },
        }

    def replacement_extension(self, previous_dn_id):
        return (
            {
                "url": "https://fhir.nhs.uk/StructureDefinition/Extension-replacementOf",
                "valueIdentifier": {
                    "system": "https://tools.ietf.org/html/rfc4122",
                    "value": previous_dn_id,
                },
            },
        )

    def organization(self, receiver_ods):
        return {
            "fullUrl": f"urn:uuid:{self.organization_id}",
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
                        "value": receiver_ods,
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
                "telecom": [
                    {"system": "phone", "use": "work", "value": "0113 3180277"}
                ],
            },
        }

    def dispense_notification(self, *entries):
        return {
            "resourceType": "Bundle",
            "type": "message",
            "entry": entries,
            "identifier": {
                "system": "https://tools.ietf.org/html/rfc4122",
                "value": self.dispense_notification_id,
            },
        }
