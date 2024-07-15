#!/usr/bin/env python

import argparse
import requests
from requests.auth import HTTPBasicAuth

URL = "https://api.github.com/repos/NHSDigital/eps-test-reports/actions/workflows/publish_report.yml/dispatches"


def get_headers():
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_auth_header():
    user_credentials = arguments.user.split(":")
    return HTTPBasicAuth(user_credentials[0], user_credentials[1])


def trigger_run():
    body = {
        "ref": "feature/AEA-3819-generate-reports-in-a-cleaner-way",
        "inputs": {"run_id": run_id},
    }

    response = requests.post(
        url=URL,
        headers=get_headers(),
        auth=get_auth_header(),
        json=body,
    )

    assert (
        response.status_code == 204
    ), f"Failed to trigger test run. Expected 204, got {response.status_code}\nURL: {URL} \nBody: {response.text}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--user", required=True, help="Please provide the user credentials."
    )
    parser.add_argument(
        "--run_id", required=True, help="The ID of the workflow Run is Required"
    )
    arguments = parser.parse_args()
    run_id = arguments.run_id

    trigger_run()
    print("Success!")
