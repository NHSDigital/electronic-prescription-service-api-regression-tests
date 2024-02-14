import logging
import os
import sys


INTERNAL_QA_BASE_URL = "https://internal-qa.api.service.nhs.uk/"
INTERNAL_DEV_BASE_URL = "https://internal-dev.api.service.nhs.uk/"
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

REPOS = {
    "EPS-FHIR": "https://github.com/NHSDigital/electronic-prescription-service-api"
}

# This will need rework when the pack includes additional products to test
PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")
EPS_SUFFIX = "electronic-prescriptions"


def before_all(context):
    env = context.config.userdata["env"].upper()

    context.fhir_base_url = os.path.join(select_base_url(env), EPS_SUFFIX)
    # This will need rework when the pack includes additional products to test
    if PULL_REQUEST_ID:
        context.fhir_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{EPS_SUFFIX}-{PULL_REQUEST_ID}"
        )

    logging.info("Using BASE_URL: '%s'", context.fhir_base_url)


def after_all(context):
    # Add anything you want to happen after all the tests have completed here
    env = context.config.userdata["env"].upper()
    product = context.config.userdata["product"].upper()
    properties_dict = {"PRODUCT": product, "ENV": env}
    if PULL_REQUEST_ID:
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
    return


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
        raise ValueError(f"Unknown environment or missing repository URL for: {env} .")


def select_repository_base_url(product):
    if product in REPOS:
        return REPOS[product]
    else:
        raise ValueError(f"Unknown product or missing base URL for: {product} .")


def write_properties_file(file_path, properties_dict):
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        for key, value in properties_dict.items():
            file.write(f"{key}={value}\n")
