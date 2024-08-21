from methods.api.common_api_methods import get, get_headers


def get_prescriptions(context):
    url = f"{context.pfp_apigee_base_url}/Bundle"
    additional_headers = {"x-nhs-number": context.nhs_number}

    headers = get_headers(context, additional_headers)

    context.response = get(url=url, context=context, headers=headers)
