from dataclasses import dataclass
import json
from typing import Any
from uuid import uuid4

from messages.eps_fhir.common import create_task


@dataclass
class WithdrawDispenseNotificationIDs:
    practitioner_role = uuid4()
    organization = uuid4()
    medication_request = uuid4()


class WithdrawDispenseNotification:
    def __init__(self, context: Any) -> None:
        ids = WithdrawDispenseNotificationIDs()
        status_reason = {
            "coding": [
                {
                    "system": "https://fhir.nhs.uk/CodeSystem/EPS-task-dispense-withdraw-reason",
                    "code": "MU",
                    "display": "Medication Update",
                }
            ]
        }
        code = {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/CodeSystem/task-code",
                    "code": "abort",
                    "display": "Mark the focal resource as no longer active",
                }
            ]
        }

        body = create_task(
            context.dispense_notification_id,
            ids.practitioner_role,
            ids.organization,
            context.sender_ods_code,
            context.prescription_id,
            context.dispense_notification_id,
            context.nhs_number,
            status_reason,
            code,
            "in-progress",
        )
        self.body = json.dumps(body)
