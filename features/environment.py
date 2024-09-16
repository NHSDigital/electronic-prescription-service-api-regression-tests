import logging
import os
import shutil
import sys

from behave.model import Scenario
from dotenv import load_dotenv

load_dotenv(override=True)

INTERNAL_QA_BASE_URL = "https://internal-qa.api.service.nhs.uk/"
INTERNAL_DEV_BASE_URL = "https://internal-dev.api.service.nhs.uk/"
PFP_AWS_PR_URL = "https://pfp-{{aws_pull_request_id}}.dev.eps.national.nhs.uk/"
PFP_AWS_SANDBOX_PR_URL = (
    "https://pfp-{{aws_pull_request_id}}-sandbox.dev.eps.national.nhs.uk/"
)
INT_BASE_URL = "https://int.api.service.nhs.uk/"
SANDBOX_DEV_BASE_URL = "https://internal-dev-sandbox.api.service.nhs.uk/"
SANDBOX_INT_BASE_URL = "https://sandbox.api.service.nhs.uk/"
REF_BASE_URL = "https://ref.api.service.nhs.uk/"

ENVS = {
    "INTERNAL-DEV": INTERNAL_DEV_BASE_URL,
    "INTERNAL-QA": INTERNAL_QA_BASE_URL,
    "INT": INT_BASE_URL,
    "REF": REF_BASE_URL,
    "INTERNAL-DEV-SANDBOX": SANDBOX_DEV_BASE_URL,
    "SANDBOX": SANDBOX_INT_BASE_URL,
}

CIS2_USERS = {
    "prescriber": {"user_id": "656005750107", "role_id": "555254242105"},
    "dispenser": {"user_id": "555260695103", "role_id": "555265434108"},
}
LOGIN_USERS = {"user_id": "9449304130"}

REPOS = {
    "EPS-FHIR": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "PFP-APIGEE": "https://github.com/NHSDigital/prescriptions-for-patients",
    "PFP-AWS": "https://github.com/NHSDigital/prescriptionsforpatients",
    "PSU": "https://github.com/NHSDigital/eps-prescription-status-update-api",
}

CERTIFICATE = os.getenv("CERTIFICATE")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_KID = os.getenv("JWT_KID")

EPS_FHIR_SUFFIX = "electronic-prescriptions"
PFP_SUFFIX = "prescriptions-for-patients"
PSU_SUFFIX = "prescription-status-update"


def count_of_scenarios_to_run(context):
    tags = context.config.tags
    total_scenarios = sum(
        1
        for feature in context._runner.features
        for scenario in feature.walk_scenarios()
        if isinstance(scenario, Scenario)
        and (not tags or scenario.should_run_with_tags(tags))
    )

    print(f"Total scenarios to be run: {total_scenarios}")
    return total_scenarios


def before_all(context):
    if count_of_scenarios_to_run(context) != 0:
        env = context.config.userdata["env"].upper()
        product = context.config.userdata["product"].upper()
        context.eps_fhir_base_url = os.path.join(select_base_url(env), EPS_FHIR_SUFFIX)
        context.pfp_base_url = os.path.join(select_base_url(env), PFP_SUFFIX)
        context.psu_base_url = os.path.join(select_base_url(env), PSU_SUFFIX)
        if PULL_REQUEST_ID:
            pull_request_id = PULL_REQUEST_ID.lower()
            if "pr-" in pull_request_id:
                get_url_with_pr(context, env, product)
    else:
        raise RuntimeError("no tests to run. Check your tags and try again")
    print("EPS: ", context.eps_fhir_base_url)
    print("PFP: ", context.pfp_base_url)
    print("PSU: ", context.psu_base_url)


def get_url_with_pr(context, env, product):
    assert PULL_REQUEST_ID is not None
    if product == "EPS-FHIR":
        context.eps_fhir_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{EPS_FHIR_SUFFIX}-{PULL_REQUEST_ID}"
        )
    if product == "PFP-APIGEE":
        context.pfp_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PFP_SUFFIX}-{PULL_REQUEST_ID}"
        )
    if product == "PFP-AWS":
        context.pfp_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PFP_SUFFIX}-{PULL_REQUEST_ID}"
        )
        if env == "INTERNAL-DEV":
            context.pfp_base_url = PFP_AWS_PR_URL.replace(
                "{{aws_pull_request_id}}", PULL_REQUEST_ID
            )
        if env == "INTERNAL-DEV-SANDBOX":
            context.pfp_base_url = PFP_AWS_SANDBOX_PR_URL.replace(
                "{{aws_pull_request_id}}", PULL_REQUEST_ID
            )

    if product == "PSU":
        context.psu_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PSU_SUFFIX}-{PULL_REQUEST_ID}"
        )


def after_all(context):
    # Add anything you want to happen after all the tests have completed here
    if count_of_scenarios_to_run(context) != 0:
        env = context.config.userdata["env"].upper()
        product = context.config.userdata["product"].upper()
        properties_dict = {"PRODUCT": product, "ENV": env}
        if PULL_REQUEST_ID:
            pull_request_id = PULL_REQUEST_ID.lower()
            if "pr-" in pull_request_id:
                env = os.path.join("PULL-REQUEST", PULL_REQUEST_ID)
                pull_request_link = os.path.join(
                    select_repository_base_url(product),
                    "pull",
                    PULL_REQUEST_ID.upper().replace("PR-", ""),
                )
                properties_dict = {
                    "PRODUCT": product,
                    "ENV": env,
                    "PULL-REQUEST": pull_request_link,
                }

        file_path = "./allure-results/environment.properties"
        write_properties_file(file_path, properties_dict)
    else:
        directory_path = "./allure-results"
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            print(f"Directory '{directory_path}' exists. Deleting...")
            shutil.rmtree(directory_path)


def setup_logging(level: int = logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
        handlers=handlers,
    )


def select_base_url(env):
    if env in ENVS:
        return ENVS[env]
    else:
        raise ValueError(f"Unknown environment or missing base URL for: {env} .")


def select_repository_base_url(product):
    if product in REPOS:
        return REPOS[product]
    else:
        raise ValueError(f"Unknown product or missing repository URL for: {product} .")


def write_properties_file(file_path, properties_dict):
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        for key, value in properties_dict.items():
            file.write(f"{key}={value}\n")
