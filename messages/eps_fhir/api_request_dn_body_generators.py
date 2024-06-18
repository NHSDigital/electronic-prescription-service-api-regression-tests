import uuid


def create_dispense_notification(*entries):
    return {"resourceType": "Bundle", "type": "message", "entry": entries}


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
        },
    }


def create_dn_medication_dispense(medication_dispense_uuid, nhs_number):
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
        },
    }


def create_dn_organisation(organisation_uuid):
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
                    "value": "VNE51",
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
