import json
from typing import Any

from utils.signing import get_signature


class SignedPrescription:
    def __init__(self, context: Any) -> None:
        context.signature = get_signature(context.digest, context.algorithm)
        self.context = context
        prescription = json.loads(context.prepare_body)
        provenance = self.generate_provenance()
        prescription["entry"].append(provenance)
        self.body = json.dumps(prescription)

    def generate_provenance(self):
        return {
            "fullUrl": "urn:uuid:28828c55-8fa7-42d7-916f-fcf076e0c10e",
            "resource": {
                "resourceType": "Provenance",
                "target": [{"reference": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6"}],
                "recorded": "2008-02-27T11:38:00+00:00",
                "agent": [{"who": {"reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"}}],
                "signature": [
                    {
                        "type": [
                            {
                                "system": "urn:iso-astm:E1762-95:2013",
                                "code": "1.2.840.10065.1.12.1.1",
                            }
                        ],
                        "when": self.context.timestamp,
                        "who": {"reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"},
                        "data": self.context.signature,
                    }
                ],
            },
        }
