import json
from datetime import UTC, datetime
import logging
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class StatusUpdatesValues:
    def __init__(self, context: Any) -> None:
        self.prescription_id = context.prescription_id
        self.prescription_item_id = context.prescription_item_id
        self.terminal_status = context.terminal_status
        self.item_status = context.item_status
        self.receiver_ods_code = context.receiver_ods_code
        self.nhs_number = context.nhs_number
        self.post_dated_timestamp = getattr(context, "post_dated_timestamp", None)


class StatusUpdate:
    def __init__(self, context: Any) -> None:
        self.values = StatusUpdatesValues(context)
        task = self.create_task()

        self.body = self.create_fhir_bundle(task)

    def create_fhir_bundle(self, *entries):
        fhir_resource = {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [],
        }

        # If post-dated timestamp is provided, add meta field to denote it but value is _now_
        if self.values.post_dated_timestamp:
            fhir_resource["meta"] = {"lastUpdated": datetime.now(UTC).isoformat()}

        fhir_resource["entry"].extend(entries)
        logger.debug("Created FHIR bundle for status update: %s", json.dumps(fhir_resource, indent=2))
        return json.dumps(fhir_resource)

    def create_task(self):
        task_identifier = uuid4()
        task = {
            "fullUrl": f"urn:uuid:{task_identifier}",
            "resource": {
                "resourceType": "Task",
                "id": f"{task_identifier}",
                "basedOn": [
                    {
                        "identifier": {
                            "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                            "value": f"{self.values.prescription_id}",
                        }
                    }
                ],
                "status": f"{self.values.terminal_status}",
                "businessStatus": {
                    "coding": [
                        {
                            "system": "https://fhir.nhs.uk/CodeSystem/task-businessStatus-nppt",
                            "code": f"{self.values.item_status}",
                        }
                    ]
                },
                "intent": "order",
                "focus": {
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                        "value": f"{self.values.prescription_item_id}",
                    }
                },
                "for": {
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/nhs-number",
                        "value": f"{self.values.nhs_number}",
                    }
                },
                "lastModified": (
                    self.values.post_dated_timestamp
                    if self.values.post_dated_timestamp
                    else datetime.now(UTC).isoformat()
                ),
                "owner": {
                    "identifier": {
                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                        "value": f"{self.values.receiver_ods_code}",
                    }
                },
            },
            "request": {"method": "POST", "url": "Task"},
        }
        return task
