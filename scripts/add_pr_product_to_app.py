#!/usr/bin/env python

import argparse
import os

import pyotp
import requests
from dotenv import load_dotenv

APIGEE_BASE_URL = "https://api.apigee.com/organizations/nhsd-nonprod/"
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--product", required=True, help="product is required")
    parser.add_argument("--pr", required=True, help="Pull request ID required")
    arguments = parser.parse_args()
    username = os.getenv("APIGEE_USER")
    password = os.getenv("APIGEE_PASSWORD")
    secret = os.getenv("APIGEE_MFA_SECRET")
    product = arguments.product
    pr_id = arguments.pr

    access_token, refresh_token = get_token()

    print("Finished!")
