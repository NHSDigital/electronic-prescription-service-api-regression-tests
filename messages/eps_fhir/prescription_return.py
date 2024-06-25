from dataclasses import dataclass
import json
from typing import Any
from uuid import uuid4
from messages.eps_fhir.common import create_task


@dataclass
class ReturnIDs:
    practitioner_role = uuid4()
    organization = uuid4()
    task_id = uuid4()


class Return:
    def __init__(self, context: Any) -> None:
        ids = ReturnIDs()
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
            context.sender_ods_code,
            context.prescription_id,
            ids.task_id,
            context.nhs_number,
            status_reason,
            code,
            "rejected",
        )
        self.body = json.dumps(body)
