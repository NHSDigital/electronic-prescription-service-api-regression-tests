import json
from typing import Any
from uuid import uuid4


class Cancel:
    def __init__(self, context: Any) -> None:
        self.context = context
        body = self.create_cancel_body()
        self.body = self.replace_ids(body)

    def cancel_medication_request(self, medication_request):
        medication_request["resource"]["status"] = "cancelled"
        medication_request["resource"]["statusReason"] = {
            "coding": [
                {
                    "system": "https://fhir.nhs.uk/CodeSystem/medicationrequest-status-reason",
                    "code": "0001",
                    "display": "Prescribing Error",
                }
            ]
        }

    def create_cancel_body(self):
        cancel_body = json.loads(self.context.prepare_body)

        medication_requests = [
            e
            for e in cancel_body["entry"]
            if e["resource"]["resourceType"] == "MedicationRequest"
        ]
        [self.cancel_medication_request(mr) for mr in medication_requests]

        message_header = [
            e
            for e in cancel_body["entry"]
            if e["resource"]["resourceType"] == "MessageHeader"
        ][0]
        event_coding = message_header["resource"]["eventCoding"]
        event_coding["code"] = "prescription-order-update"
        event_coding["display"] = "Prescription Order Update"

        return json.dumps(cancel_body)

    def replace_ids(self, body: str):
        old_id = json.loads(body)["id"]
        return body.replace(old_id, str(uuid4()))
