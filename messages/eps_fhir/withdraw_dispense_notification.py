import json
from typing import Any
from uuid import uuid4

from messages.eps_fhir.common import create_task


class WithdrawDispenseNotificationIDs:
    def __init__(self, context: Any) -> None:
        self.practitioner_role = uuid4()
        self.organization = uuid4()
        self.medication_request = uuid4()

        self.dispense_notification = context.dispense_notification_id
        self.sender_ods_code = context.sender_ods_code
        self.prescription = context.prescription_id
        self.dispense_notification = context.dispense_notification_id
        self.nhs_number = context.nhs_number


class WithdrawDispenseNotification:
    def __init__(self, context: Any) -> None:
        ids = WithdrawDispenseNotificationIDs(context)
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
            ids.dispense_notification,
            ids.practitioner_role,
            ids.organization,
            ids.sender_ods_code,
            ids.prescription,
            ids.dispense_notification,
            ids.nhs_number,
            status_reason,
            code,
            "in-progress",
        )
        self.body = json.dumps(body)
