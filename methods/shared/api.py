import uuid
from requests import get as api_get_request
from requests import post as api_post_request
from methods.shared import common


def get(context, **kwargs):
    context.response = api_get_request(**kwargs)
    common.attach_api_information(context)
    return context.response


def post(context, **kwargs):
    context.response = api_post_request(**kwargs)
    common.attach_api_information(context)
    return context.response


def get_default_headers():
    return {
        "x-request-id": str(uuid.uuid4()),
        "x-user-org-code": "Auto001",
    }


def request_ping(context, base_url):
    url = f"{base_url}/_ping"
    get(context=context, url=url, headers=get_default_headers())
