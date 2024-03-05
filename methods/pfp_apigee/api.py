import uuid
import requests
from methods.shared import common


def get_default_headers():
    return {
        "x-request-id": str(uuid.uuid4()),
        "x-user-org-code": "Auto001",
    }


def request_ping(context):
    url = f"{context.pfp_apigee_base_url}/_ping"
    context.response = requests.get(url=url)
    common.attach_api_information(context)
