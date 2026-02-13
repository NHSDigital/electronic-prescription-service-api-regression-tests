import json
from typing import Any
from uuid import uuid4

from eps_test_support.messages.eps_fhir.common import create_withdraw_task


class WithdrawDispenseNotificationValues:
    def __init__(self, context: Any) -> None:
        self.practitioner_role_id = uuid4()
        self.organization_id = uuid4()
        self.medication_request_id = uuid4()

        self.dispense_notification_id = context.dispense_notification_id
        self.sender_ods_code = context.sender_ods_code
        self.prescription_id = context.prescription_id
        self.dispense_notification_id = context.dispense_notification_id
        self.nhs_number = context.nhs_number


class WithdrawDispenseNotification:
    def __init__(self, context: Any) -> None:
        values = WithdrawDispenseNotificationValues(context)
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

        body = create_withdraw_task(
            values.dispense_notification_id,
            values.practitioner_role_id,
            values.organization_id,
            values.sender_ods_code,
            values.prescription_id,
            values.dispense_notification_id,
            values.nhs_number,
            status_reason,
            code,
            "in-progress",
        )
        self.body = json.dumps(body)
