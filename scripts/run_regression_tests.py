#!/usr/bin/env python

"""
Script to generate user defined unique ID which can be used to
check the status of the regression test run to be reported to the CI.
"""
import argparse
import time
import requests
from requests.auth import HTTPBasicAuth, AuthBase

# This should be set to a known good version of regression test repo
GITHUB_API_URL = "https://api.github.com/repos/NHSDigital/electronic-prescription-service-api-regression-tests/actions"
GITHUB_RUN_URL = "https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/runs"

ENVIRONMENT_NAMES = {
    "dev": "INTERNAL-DEV",
    "dev-pr": "INTERNAL-DEV",
    "internal-dev": "INTERNAL-DEV",
    "qa": "INTERNAL-QA",
    "internal-qa": "INTERNAL-QA",
    "int": "INT",
    "ref": "REF",
}


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_headers():
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def trigger_test_run(
    env,
    pr_label,
    product,
    auth_header,
    regression_test_repo_tag,
    regression_test_workflow_tag,
):
    body = {
        "ref": regression_test_workflow_tag,
        "inputs": {
            "tags": "@regression",
            "environment": ENVIRONMENT_NAMES[env],
            "pull_request_id": pr_label,
            "product": product,
            "github_tag": regression_test_repo_tag,
        },
    }

    response = requests.post(
        url=f"{GITHUB_API_URL}/workflows/regression_tests.yml/dispatches",
        headers=get_headers(),
        auth=auth_header,
        json=body,
        timeout=120,
    )
    assert (
        response.status_code == 200
    ), f"Failed to trigger test run. Expected 200, got {response.status_code}. Response: {response.text}"
    return response.json()["workflow_run_id"]


def get_auth_header(is_called_from_github, token, user):
    if is_called_from_github:
        return BearerAuth(token)
    else:
        user_credentials = user.split(":")
        return HTTPBasicAuth(user_credentials[0], user_credentials[1])


def get_upload_result_job(auth_header, workflow_id):
    job_request_url = f"{GITHUB_API_URL}/runs/{workflow_id}/jobs"
    job_response = requests.get(
        job_request_url,
        headers=get_headers(),
        auth=auth_header,
        timeout=120,
    )
    jobs = job_response.json()["jobs"]
    upload_result_job = next(
        (job for job in jobs if job["name"] == "upload_results"),
        {"status": "can not find upload results job - tests are likely still running"},
    )
    return upload_result_job


def check_job(auth_header, workflow_id):
    max_attempts = 720  # this is about 2 hours
    current_attempt = 0

    print("Checking job status, please wait...")
    job = get_upload_result_job(auth_header, workflow_id)
    job_status = job["status"]

    while job_status != "completed":
        if current_attempt > max_attempts:
            raise TimeoutError(
                f"Regression test job not completed after {current_attempt} attempts"
            )
        print(
            f"Current upload results job status : {job_status} after {current_attempt} attempts"
        )
        time.sleep(10)
        current_attempt = current_attempt + 1
        job = get_upload_result_job(auth_header, workflow_id)
        job_status = job["status"]

    return job["conclusion"]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pr_label",
        required=False,
        help="Please provide the PR number.",
    )
    parser.add_argument(
        "--env",
        required=True,
        help="Please provide the environment you wish to run in.",
    )
    parser.add_argument(
        "--user", required=False, help="Please provide the user credentials."
    )
    parser.add_argument(
        "--is_called_from_github",
        default=False,
        type=lambda x: (str(x).lower() == "true"),
        help="If this is being called from github actions rather than azure",
    )
    parser.add_argument(
        "--product",
        required=True,
        help="Please provide the product to run the tests for.",
    )
    parser.add_argument(
        "--token", required=False, help="Please provide the authentication token."
    )
    parser.add_argument(
        "--regression_test_repo_tag",
        required=True,
        help="Please provide the tag to run regression tests from.",
    )
    parser.add_argument(
        "--regression_test_workflow_tag",
        required=False,
        default="main",
        help="Please provide the tag to for the run_regression_test workflow.",
    )

    arguments = parser.parse_args()

    print(f"pr_label: {arguments.pr_label}")
    print(f"env: {arguments.env}")
    print(f"is_called_from_github: {arguments.is_called_from_github}")
    print(f"product: {arguments.product}")
    print(f"regression_tests_repo_tag: {arguments.regression_test_repo_tag}")
    print(f"regression_test_workflow_tag: {arguments.regression_test_workflow_tag}")

    auth_header = get_auth_header(
        arguments.is_called_from_github, arguments.token, arguments.user
    )

    pr_label = arguments.pr_label.lower()
    workflow_id = trigger_test_run(
        arguments.env,
        pr_label,
        arguments.product,
        auth_header,
        arguments.regression_test_repo_tag,
        arguments.regression_test_workflow_tag,
    )
    print(f"See {GITHUB_RUN_URL}/{workflow_id}/ for run details")

    job_status = check_job(auth_header, workflow_id)
    if job_status != "success":
        if arguments.pr_label:
            pr_label = arguments.pr_label.lower()
            env = f"PULL-REQUEST/{pr_label}"
        else:
            env = arguments.env.upper()
        print("The regressions test step failed! There are likely test failures.")
        print(
            f"See https://nhsdigital.github.io/eps-test-reports/{arguments.product}/{env}/ for allure report"
        )
        raise SystemError("Regression test failed")

    print("Success!")


if __name__ == "__main__":
    main()
