import os

from methods.api.common_api_methods import get, get_headers


def get_prescriptions(context):
    url = f"{context.pfp_base_url}/Bundle"
    additional_headers = {
        "x-nhs-number": context.nhs_number,
        "nhsd-nhslogin-user": "P9:" + context.nhs_number,
    }

    headers = get_headers(context, "oauth2", additional_headers)
    context.response = get(url=url, context=context, headers=headers)


def get_my_prescriptions(context):
    environment = context.config.userdata["env"].upper()
    product = context.config.userdata["product"].upper()
    pr_id = os.getenv("PULL_REQUEST_ID").lower()
    is_pr = False
    if "pr-" in pr_id:
        is_pr = True
    url = ""

    if product not in ["PFP-APIGEE", "PFP-AWS"]:
        raise Exception(f"Invalid product {product}")
    if environment not in ["INTERNAL-DEV"]:
        raise Exception(f"Invalid environment {environment}")

    if is_pr:
        url = f"{pr_id}.dev.prescriptionsforpatients.national.nhs.uk/getMyPrescriptions"
    else:
        url = "dev-ci.dev.prescriptionsforpatients.national.nhs.uk/getMyPrescriptions"

    additional_headers = {
        "x-nhs-number": context.nhs_number,
        "nhsd-nhslogin-user": "P9:" + context.nhs_number,
    }

    headers = get_headers(context, "oauth2", additional_headers)
    context.response = get(url=url, context=context, headers=headers)
