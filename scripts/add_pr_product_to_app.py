#!/usr/bin/env python

import argparse
import os
import json
import pyotp
import requests
from dotenv import load_dotenv

APIGEE_BASE_URL = "https://api.enterprise.apigee.com/v1/organizations/nhsd-nonprod/"
SSO_LOGIN_URL = "https://login.apigee.com/oauth/token"
EPS_FHIR_DISPENSING_APP_ID = "1427007d-7dd3-4153-901a-df027fa6e6d6"
EPS_FHIR_PRESCRIBING_APP_ID = "b6013742-6e0b-42df-b185-f05e7c753fe8"
EPS_FHIR_PRESCRIBING_SHA1_APP_ID = "1122eb42-c783-4748-84b7-47e20446306d"
load_dotenv(override=True)


def get_token():
    assert secret is not None
    totp = pyotp.TOTP(secret)
    mfa_code = totp.now()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json;charset=utf-8",
        "Authorization": "Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
    }
    body = f"username={username}&password={password}&grant_type=password"
    response = requests.post(
        url=f"{SSO_LOGIN_URL}?mfa_token={mfa_code}",
        headers=headers,
        data=body,
    )
    assert (
        response.status_code == 200
    ), f"expected 200, but got {response.status_code}\n{response.text}"
    return response.json()["access_token"], response.json()["refresh_token"]


def add_products_to_apps():
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {access_token}",
    }
    base_apps_url = (
        f"{APIGEE_BASE_URL}companies/c4bd161b-0bc5-4a29-866e-85c81b704bd0/apps/"
    )
    dispensing_url = f"{base_apps_url}REGRESSION_INTERNAL_DEV_EPS_FHIR_DISPENSING/keys/cRG1mUYr6RVwx3ZDKg4pJg3PA9GbVJqH"
    prescribing_url = f"{base_apps_url}REGRESSION_INTERNAL_DEV_EPS_FHIR_PRESCRIBING/keys/XybKJFjIUAwSqi0DApCC8GzGqsTUKjMi"
    prescribing_sha1_url = f"{base_apps_url}REGRESSION_INTERNAL_DEV_EPS_FHIR_PRESCRIBING_SHA1/keys/4KVK1jIGYPESfv4FEW6klwjrbYMCJkqu"

    def add_product_to_prescribing_app():
        print(f"adding product {pr_id} to prescribing")
        body = json.dumps(
            {
                "apiProducts": [
                    f"electronic-prescription-service-api-{pr_id}-prescribing"
                ]
            }
        )

        response = requests.post(
            url=prescribing_sha1_url,
            headers=headers,
            data=body,
        )
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"

        print(f"adding product {pr_id} to prescribing SHA1")
        response = requests.put(
            url=prescribing_url,
            headers=headers,
            data=body,
        )
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"

    def add_product_to_dispensing_app():
        print(f"adding product {pr_id} to dispensing")
        body = json.dumps(
            {"apiProducts": [f"electronic-prescription-service-api-{pr_id}-dispensing"]}
        )

        response = requests.put(
            url=dispensing_url,
            headers=headers,
            data=body,
        )
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"

    add_product_to_dispensing_app()
    add_product_to_prescribing_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--product", required=True, help="product is required")
    parser.add_argument("--pr", required=True, help="Pull request ID required")
    arguments = parser.parse_args()
    username = os.getenv("APIGEE_USER")
    password = os.getenv("APIGEE_PASSWORD")
    secret = os.getenv("APIGEE_MFA_SECRET")
    product = arguments.product
    pr_id = arguments.pr.lower()
    if "pr-" in pr_id:
        pass

    access_token, refresh_token = get_token()
    add_products_to_apps()
    print("Finished!")
