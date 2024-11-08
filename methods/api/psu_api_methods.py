from messages.psu.prescription_status_update import StatusUpdate
from methods.api.common_api_methods import post, get_headers


def send_status_update(context):
    url = f"{context.psu_base_url}/"

    headers = get_headers(context)
    context.send_update_body = StatusUpdate(context).body
    context.response = post(
        data=context.send_update_body, url=url, context=context, headers=headers
    )
