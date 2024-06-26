import json
from typing import Any
from uuid import uuid4
from features.environment import CIS2_USERS


class ReleaseValues:
    def __init__(self, context: Any) -> None:
        self.prescription_id = context.prescription_id
        self.receiver_ods_code = context.receiver_ods_code


class Release:
    def __init__(self, context: Any) -> None:
        self.values = ReleaseValues(context)
        group_identifier = self.create_group_identifier()
        owner = self.create_owner()
        agent = self.create_agent()
        self.body = self.create_fhir_parameter(group_identifier, owner, agent)

    def create_group_identifier(self):
        return {
            "name": "group-identifier",
            "valueIdentifier": {
                "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                "value": self.values.prescription_id,
            },
        }

    def create_owner(self):
        return {
            "name": "owner",
            "resource": {
                "resourceType": "Organization",
                "identifier": [
                    {
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": self.values.receiver_ods_code,
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
            },
        }

    def create_agent(self):
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

    def create_fhir_parameter(self, *entries):
        fhir_resource = {
            "resourceType": "Parameters",
            "id": str(uuid4()),
            "parameter": [{"name": "status", "valueCode": "accepted"}],
        }
        fhir_resource["parameter"].extend(entries)
        return json.dumps(fhir_resource)
