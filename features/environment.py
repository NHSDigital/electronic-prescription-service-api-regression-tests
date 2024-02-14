import logging
import os
import sys


INTERNAL_QA_BASE_URL = "Https://internal-qa.api.service.nhs.uk/"
INTERNAL_DEV_BASE_URL = "Https://internal-dev.api.service.nhs.uk/"
INT_BASE_URL = "Https://int.api.service.nhs.uk/"
SANDBOX_DEV_BASE_URL = "Https://internal-dev-sandbox.api.service.nhs.uk/"
SANDBOX_INT_BASE_URL = "Https://sandbox.api.service.nhs.uk/"
REF_BASE_URL = "Https://ref.api.service.nhs.uk/"

ENVS = {
    "INTERNAL-DEV": INTERNAL_DEV_BASE_URL,
    "INTERNAL-QA": INTERNAL_QA_BASE_URL,
    "INT": INT_BASE_URL,
    "REF": REF_BASE_URL,
    "INTERNAL-DEV-SANDBOX": SANDBOX_DEV_BASE_URL,
    "SANDBOX": SANDBOX_INT_BASE_URL,
}

# This will need rework when the pack includes additional products to test
PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")
EPS_SUFFIX = "electronic-prescriptions"


def before_all(context):
    env = context.config.userdata["env"].upper()

    context.fhir_base_url = select_base_url(env) + EPS_SUFFIX
    # This will need rework when the pack includes additional products to test
    if PULL_REQUEST_ID:
        context.fhir_base_url = (
            INTERNAL_DEV_BASE_URL + EPS_SUFFIX + build_pull_request_id()
        )

    logging.info("Using BASE_URL: '%s'", context.fhir_base_url)


def after_all(context):
    # Add anything you want to happen after all the tests have completed here
    env = context.config.userdata["env"].upper()
    product = context.config.userdata["product"].upper()
    if PULL_REQUEST_ID:
            env = f"PULL_REQUEST/PR-{PULL_REQUEST_ID}"
    properties_dict = {"PRODUCT": product, "ENV": env, "PR_ID": PULL_REQUEST_ID}

    file_path = "./allure-results/environment.properties"
    write_properties_file(file_path, properties_dict)
    return


def setup_logging(level: int = logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
        handlers=handlers,
    )


def build_pull_request_id():
    pr_suffix = ""
    if PULL_REQUEST_ID:
        if "pr-" in str({PULL_REQUEST_ID}):
            pr_suffix = f"-{PULL_REQUEST_ID}"
        else:
            pr_suffix = f"-pr-{PULL_REQUEST_ID}"
    return pr_suffix


def select_base_url(env):
    if env in ENVS:
        return ENVS[env]
    else:
        raise ValueError(f"Unknown environment or missing base URL for: {env} .")


def write_properties_file(file_path, properties_dict):
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        for key, value in properties_dict.items():
            file.write(f"{key}={value}\n")
