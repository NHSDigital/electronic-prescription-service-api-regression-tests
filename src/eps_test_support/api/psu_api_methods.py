from eps_test_support.messages.psu.prescription_status_update import StatusUpdate
from eps_test_support.api.common_api_methods import get, post, get_headers


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

    return context.response


CODING_TO_STATUS_MAP = {
    "With Pharmacy": "in-progress",
    "Ready to Collect": "in-progress",
    "Collected": "completed",
}
