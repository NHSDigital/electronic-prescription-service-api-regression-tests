#!/usr/bin/env python

import argparse
import os
import json
import pyotp
import requests
import urllib.parse
from dotenv import load_dotenv

APIGEE_BASE_URL = "https://api.enterprise.apigee.com/v1/organizations/nhsd-nonprod/"
SSO_LOGIN_URL = "https://login.apigee.com/oauth/token"

EPS_FHIR_DISPENSING_APP_ID = "1427007d-7dd3-4153-901a-df027fa6e6d6"
EPS_FHIR_PRESCRIBING_APP_ID = "b6013742-6e0b-42df-b185-f05e7c753fe8"
EPS_FHIR_PRESCRIBING_SHA1_APP_ID = "1122eb42-c783-4748-84b7-47e20446306d"

global DISPENSING_CONSUMER_KEY
global PRESCRIBING_CONSUMER_KEY
global PRESCRIBING_SHA1_CONSUMER_KEY
load_dotenv(override=True)


def get_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {access_token}",
    }


def get_token():
    assert secret is not None
    totp = pyotp.TOTP(secret)
    mfa_code = totp.now()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json;charset=utf-8",
        "Authorization": "Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
    }
    body = f"username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}&grant_type=password"
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
    base_apps_url = (
        f"{APIGEE_BASE_URL}companies/c4bd161b-0bc5-4a29-866e-85c81b704bd0/apps/"
    )
    dispensing_url = f"{base_apps_url}REGRESSION_INTERNAL_DEV_EPS_FHIR_DISPENSING/keys/{DISPENSING_CONSUMER_KEY}"
    prescribing_url = f"{base_apps_url}REGRESSION_INTERNAL_DEV_EPS_FHIR_PRESCRIBING/keys/{PRESCRIBING_CONSUMER_KEY}"
    prescribing_sha1_url = (
        f"{base_apps_url}"
        f"REGRESSION_INTERNAL_DEV_EPS_FHIR_PRESCRIBING_SHA1/keys/{PRESCRIBING_SHA1_CONSUMER_KEY}"
    )
    headers = get_headers()

    def add_product_to_prescribing_app():
        print(f"adding {pr_id} to product prescribing")
        body = json.dumps(
            {
                "apiProducts": [
                    f"fhir-prescribing--internal-dev--fhir-prescribing-{pr_id}--nhs-cis2-aal3"
                ]
            }
        )

        response = requests.put(
            url=prescribing_sha1_url,
            headers=headers,
            data=body,
        )
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"

        print(f"adding {pr_id} to product prescribing SHA1")
        response = requests.put(
            url=prescribing_url,
            headers=headers,
            data=body,
        )
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"

    def add_product_to_dispensing_app():
        print(f"adding {pr_id} to product dispensing")
        body = json.dumps(
            {
                "apiProducts": [
                    f"fhir-dispensing--internal-dev--fhir-dispensing-{pr_id}--nhs-cis2-aal3"
                ]
            }
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


def get_consumer_keys():
    headers = get_headers()
    base_apps_url = f"{APIGEE_BASE_URL}apps/"
    dispensing_url = base_apps_url + EPS_FHIR_DISPENSING_APP_ID
    prescribing_url = base_apps_url + EPS_FHIR_PRESCRIBING_APP_ID
    prescribing_sha1_url = base_apps_url + EPS_FHIR_PRESCRIBING_SHA1_APP_ID

    def get_consumer_key(url):
        response = requests.get(url=url, headers=headers)
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"
        return response.json()["credentials"][0]["consumerKey"]

    global DISPENSING_CONSUMER_KEY
    DISPENSING_CONSUMER_KEY = get_consumer_key(dispensing_url)

    global PRESCRIBING_CONSUMER_KEY
    PRESCRIBING_CONSUMER_KEY = get_consumer_key(prescribing_url)

    global PRESCRIBING_SHA1_CONSUMER_KEY
    PRESCRIBING_SHA1_CONSUMER_KEY = get_consumer_key(prescribing_sha1_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--product", required=True, help="product is required")
    parser.add_argument("--pr", required=True, help="Pull request ID required")
    arguments = parser.parse_args()
    username = os.getenv("APIGEE_USER")
    password = os.getenv("APIGEE_PASSWORD")
    secret = os.getenv("APIGEE_MFA_SECRET")
    product = arguments.product
    if product not in [
        "EPS-FHIR-PRESCRIBING",
        "EPS-FHIR-DISPENSING",
    ]:
        print(f"{product} Not supported. Exiting.")
        exit(0)
    pr_id = arguments.pr.lower()
    if "pr-" not in pr_id:
        print("Not a Pull Request. Exiting.")
        exit(0)

    access_token, refresh_token = get_token()
    get_consumer_keys()
    add_products_to_apps()
    print("Finished!")
