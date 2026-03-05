import json
import logging
from datetime import UTC, datetime

from messages.psu.prescription_status_update import StatusUpdate
from methods.api.common_api_methods import get, post, get_headers

logger = logging.getLogger(__name__)


def send_status_update(context):
    url = f"{context.psu_base_url}/"

    headers = get_headers(context, "oauth2")
    context.send_update_body = StatusUpdate(context).body
    context.response = post(data=context.send_update_body, url=url, context=context, headers=headers)


def check_status_updates(context, prescription_id=None, nhs_number=None, ods_code=None):
    url = f"{context.psu_base_url}/checkprescriptionstatusupdates"
    params = {}
    if prescription_id:
        params["prescriptionid"] = prescription_id
    if nhs_number:
        params["nhsnumber"] = nhs_number
    if ods_code:
        params["odscode"] = ods_code

    headers = get_headers(context, "oauth2")
    context.response = get(context=context, url=url, params=params, headers=headers)

    # Pretty print response to timestamp file
    if context.response.status_code == 200:
        timestamp = datetime.now(UTC).isoformat().replace(":", "-").replace(".", "-")
        filename = f"{timestamp}.json"
        with open(filename, "w", encoding="UTF-8") as f:
            json.dump(context.response.json(), f, indent=2)

    return context.response


def get_status_updates(context):
    # TODO: refactor to generalise this url
    psu_aws_base_url = "https://psu-pr-2814.dev.eps.national.nhs.uk"
    url = f"{psu_aws_base_url}/get-status-updates"
    logger.debug("Getting status updates from URL: %s", url)

    body = {
        "schemaVersion": 1,
        "prescriptions": [
            {
                "prescriptionID": context.prescription_id,
                "odsCode": context.receiver_ods_code,
            }
        ],
    }

    headers = get_headers(context, "oauth2")
    context.response = post(data=json.dumps(body), url=url, context=context, headers=headers)

    # TODO: remove debugging before merge
    # Pretty print response to timestamp file
    if (
        logger.isEnabledFor(logging.DEBUG)
        and context.response.status_code >= 200
        and context.response.status_code < 300
    ):
        timestamp = datetime.now(UTC).isoformat().replace(":", "-").replace(".", "-")
        filename = f"{timestamp}.json"
        with open(filename, "w", encoding="UTF-8") as f:
            json.dump(context.response.json(), f, indent=2)
        logger.debug("Response saved to file: %s", filename)

    return context.response


CODING_TO_STATUS_MAP = {
    "With Pharmacy": "in-progress",
    "Ready to Collect": "in-progress",
    "Collected": "completed",
}
