#!/usr/bin/env python

import argparse
import pyotp
import requests

APIGEE_BASE_URL = "https://api.apigee.com/organizations/nhsd-nonprod/"
SSO_LOGIN_URL="https://login.apigee.com/oauth/token"

def get_token():
    mfa_code=pyotp.TOTP(secret).now()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json;charset=utf-8",
        "Authorization": f"Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
    }

    return mfa_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--user", required=True, help="APIGEE Username required"
    )
    parser.add_argument(
        "--password", required=True, help="APIGEE Password required"
    )
    parser.add_argument(
        "--secret", required=True, help="MFA authentication secret required"
    )
    parser.add_argument(
        "--pr", required=True, help="Pull request ID required"
    )
    arguments = parser.parse_args()
    username = arguments.user
    password = arguments.password
    secret = arguments.secret
    pr_id = arguments.pr

    print("Finished!")
