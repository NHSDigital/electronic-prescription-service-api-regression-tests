from methods.api.common_api_methods import get, get_headers


def get_prescriptions(context):
    url = f"{context.pfp_base_url}/Bundle"
    additional_headers = {
        "x-nhs-number": context.nhs_number,
        "nhsd-nhslogin-user": "P9:" + context.nhs_number,
    }

    headers = get_headers(context, "oauth2", additional_headers)
    context.response = get(url=url, context=context, headers=headers)
