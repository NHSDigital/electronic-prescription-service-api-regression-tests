#!/usr/bin/env python

import argparse
import os
import urllib.parse
import json
import pyotp
import requests
from dotenv import load_dotenv

APIGEE_BASE_URL = "https://api.enterprise.apigee.com/v1/organizations/nhsd-nonprod/"
SSO_LOGIN_URL = "https://login.apigee.com/oauth/token"

load_dotenv(override=True)


def get_product_config(pr_id):
    product_config = {
        "EPS-FHIR-PRESCRIBING": {
            "app_id": "b6013742-6e0b-42df-b185-f05e7c753fe8",
            "app_name": "REGRESSION_INTERNAL_DEV_EPS_FHIR_PRESCRIBING",
            "api_product_name": f"fhir-prescribing--internal-dev--fhir-prescribing-{pr_id}--nhs-cis2-aal3",
            "accompanying_product": "EPS-FHIR-PRESCRIBING-SHA1",
        },
        "EPS-FHIR-PRESCRIBING-SHA1": {
            "app_id": "1122eb42-c783-4748-84b7-47e20446306d",
            "app_name": "REGRESSION_INTERNAL_DEV_EPS_FHIR_PRESCRIBING_SHA1",
            "api_product_name": f"fhir-dispensing--internal-dev--fhir-dispensing-{pr_id}--nhs-cis2-aal3",
            "accompanying_product": "EPS-FHIR-PRESCRIBING",
        },
        "EPS-FHIR-DISPENSING": {
            "app_is": "1427007d-7dd3-4153-901a-df027fa6e6d6",
            "app_name": "REGRESSION_INTERNAL_DEV_EPS_FHIR_DISPENSING",
            "api_product_name": f"fhir-dispensing--internal-dev--fhir-dispensing-{pr_id}--nhs-cis2-aal3",
        },
        "PFP-PROXYGEN": {
            "app_id": "fa7eaadb-da69-4c4b-8821-83e21cb649f5",
            "app_name": "REGRESSION_INTERNAL_DEV_PFP",
            "api_product_name": f"prescriptions-for-patients-proxygen--internal-dev--pfp-proxygen-{pr_id}--nhs-login-p9",  # noqa: E501
        },
    }

    return product_config


def get_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {access_token}",
    }


def get_token():
    assert secret is not None
    assert username is not None
    assert password is not None
    totp = pyotp.TOTP(secret)
    mfa_code = totp.now()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json;charset=utf-8",
        "Authorization": "Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
    }
    encoded_username = urllib.parse.quote_plus(username)
    encoded_password = urllib.parse.quote_plus(password)
    body = (
        f"username={encoded_username}&password={encoded_password}&grant_type=password"
    )
    response = requests.post(
        url=f"{SSO_LOGIN_URL}?mfa_token={mfa_code}",
        headers=headers,
        data=body,
    )
    assert (
        response.status_code == 200
    ), f"expected 200, but got {response.status_code}\n{response.text}"
    return response.json()["access_token"], response.json()["refresh_token"]


def slash_join(*args):
    return "/".join(arg.strip("/") for arg in args)


def add_product_to_app(base_url, config, headers):
    body = json.dumps({"apiProducts": [config["api_product_name"]]})

    built_url = slash_join(base_url, config["app_name"], "keys", config["consumer_key"])
    response = requests.put(url=built_url, headers=headers, data=body, timeout=60)
    assert (
        response.status_code == 200
    ), f"expected 200, but got {response.status_code}\n{response.text}"


def add_products_to_apps(pr, product_config, selected_product):
    base_apps_url = (
        f"{APIGEE_BASE_URL}companies/c4bd161b-0bc5-4a29-866e-85c81b704bd0/apps/"
    )
    headers = get_headers()

    print(f"Adding {pr} to {selected_product}")
    add_product_to_app(base_apps_url, product_config[selected_product], headers)


def get_consumer_keys(config, selected_product):
    headers = get_headers()
    base_apps_url = f"{APIGEE_BASE_URL}apps/"

    def get_consumer_key(url):
        response = requests.get(url=url, headers=headers)
        assert (
            response.status_code == 200
        ), f"expected 200, but got {response.status_code}\n{response.text}"
        return response.json()["credentials"][0]["consumerKey"]

    print(f"Requesting consumer keys for {selected_product}")
    url = base_apps_url + config[selected_product]["app_id"]
    config[selected_product]["consumer_key"] = get_consumer_key(url)

    return config


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
    if "pr-" not in pr_id:
        print("Not a Pull Request. Exiting.")
        exit(0)

    product_configs = get_product_config(pr_id)
    if product not in product_configs.keys():
        print(f"{product} Not supported. Exiting.")
        exit(0)

    global access_token
    global refresh_token
    access_token, refresh_token = get_token()

    products_to_run = []
    products_to_run.append(product)

    accompanying_product = product_configs[product].get("accompanying_product")
    if accompanying_product:
        print(f"Adding accompanying product to run for {accompanying_product}")
        products_to_run.append(accompanying_product)

    for product in products_to_run:
        product_configs = get_consumer_keys(product_configs, product)
        add_products_to_apps(pr_id, product_configs, product)
    print("Finished!")
