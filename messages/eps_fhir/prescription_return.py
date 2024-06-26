import json
from typing import Any
from uuid import uuid4
from messages.eps_fhir.common import create_task


class ReturnIDs:
    def __init__(self, context: Any) -> None:
        self.practitioner_role = uuid4()
        self.organization = uuid4()
        self.task_id = uuid4()

        self.sender_ods_code = context.sender_ods_code
        self.prescription = context.prescription_id
        self.nhs_number = context.nhs_number


class Return:
    def __init__(self, context: Any) -> None:
        ids = ReturnIDs(context)
        status_reason = {
            "coding": [
                {
                    "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-dispense-return-status-reason",
                    "code": "0003",
                    "display": "Patient requested release",
                }
            ]
        }
        code = {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/CodeSystem/task-code",  # http only
                    "code": "fulfill",
                    "display": "Fulfill the focal request",
                }
            ]
        }

        body = create_task(
            ids.task_id,
            ids.practitioner_role,
            ids.organization,
            ids.sender_ods_code,
            ids.prescription,
            ids.task_id,
            ids.nhs_number,
            status_reason,
            code,
            "rejected",
        )
        self.body = json.dumps(body)
