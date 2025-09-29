import logging
import os
import shutil
import sys
import uuid
from behave.model import Scenario
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect
from methods.api import eps_api_methods
import allure
import requests
import json

load_dotenv(override=True)
global _page
global _playwright
INTERNAL_QA_BASE_URL = "https://internal-qa.api.service.nhs.uk/"
INTERNAL_DEV_BASE_URL = "https://internal-dev.api.service.nhs.uk/"
INT_BASE_URL = "https://int.api.service.nhs.uk/"
SANDBOX_DEV_BASE_URL = "https://internal-dev-sandbox.api.service.nhs.uk/"
SANDBOX_INT_BASE_URL = "https://sandbox.api.service.nhs.uk/"
REF_BASE_URL = "https://ref.api.service.nhs.uk/"

LOCALHOST_URL = "http://localhost:3000/"

AWS_BASE_URL = ".eps.national.nhs.uk/"
PFP_AWS_PR_URL = "https://pfp-{{aws_pull_request_id}}.dev.eps.national.nhs.uk/"
PFP_AWS_SANDBOX_PR_URL = (
    "https://pfp-{{aws_pull_request_id}}-sandbox.dev.eps.national.nhs.uk/"
)
CPTS_UI_PR_URL = "https://cpt-ui-{{aws_pull_request_id}}.dev.eps.national.nhs.uk/"
CPTS_UI_SANDBOX_PR_URL = (
    "https://cpt-ui-{{aws_pull_request_id}}sandbox.dev.eps.national.nhs.uk/"
)

APIGEE_ENVS = {
    "INTERNAL-DEV": INTERNAL_DEV_BASE_URL,
    "INTERNAL-QA": INTERNAL_QA_BASE_URL,
    "INT": INT_BASE_URL,
    "REF": REF_BASE_URL,
    "INTERNAL-DEV-SANDBOX": SANDBOX_DEV_BASE_URL,
    "SANDBOX": SANDBOX_INT_BASE_URL,
    "LOCALHOST": LOCALHOST_URL,
}

AWS_ENVS = {
    "INTERNAL-DEV": f".dev{AWS_BASE_URL}",
    "INTERNAL-QA": f".qa{AWS_BASE_URL}",
    "INT": f".int{AWS_BASE_URL}",
    "REF": f".ref{AWS_BASE_URL}",
    "INTERNAL-DEV-SANDBOX": f".sandbox{AWS_BASE_URL}",
    "SANDBOX": f".sandbox.dev{AWS_BASE_URL}",
}

APIGEE_APPS = {
    "CPTS-FHIR": {
        "client_id": os.getenv("CPT_FHIR_CLIENT_ID"),
        "client_secret": os.getenv("CPT_FHIR_CLIENT_SECRET"),
    },
    "EPS-FHIR": {
        "client_id": os.getenv("EPS_FHIR_CLIENT_ID"),
        "client_secret": os.getenv("EPS_FHIR_CLIENT_SECRET"),
    },
    "EPS-FHIR-SHA1": {
        "client_id": os.getenv("EPS_FHIR_SHA1_CLIENT_ID"),
        "client_secret": os.getenv("EPS_FHIR_SHA1_CLIENT_SECRET"),
    },
    "EPS-FHIR-PRESCRIBING": {
        "client_id": os.getenv("EPS_FHIR_PRESCRIBING_CLIENT_ID"),
        "client_secret": os.getenv("EPS_FHIR_PRESCRIBING_CLIENT_SECRET"),
    },
    "EPS-FHIR-PRESCRIBING-SHA1": {
        "client_id": os.getenv("EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID"),
        "client_secret": os.getenv("EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET"),
    },
    "EPS-FHIR-DISPENSING": {
        "client_id": os.getenv("EPS_FHIR_DISPENSING_CLIENT_ID"),
        "client_secret": os.getenv("EPS_FHIR_DISPENSING_CLIENT_SECRET"),
    },
    "PFP-APIGEE": {
        "client_id": os.getenv("PFP_CLIENT_ID"),
        "client_secret": os.getenv("PFP_CLIENT_SECRET"),
    },
    "PSU": {
        "client_id": os.getenv("PSU_CLIENT_ID"),
        "client_secret": os.getenv("PSU_CLIENT_SECRET"),
    },
}
CIS2_USERS = {
    "prescriber": {"user_id": "656005750107", "role_id": "555254242105"},
    "dispenser": {"user_id": "555260695103", "role_id": "555265434108"},
}
LOGIN_USERS = {"user_id": "9449304130"}
# Roles with Access: multiple | Roles without Access: multiple | Selected Role: No
# this is not used
MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_ZERO_NO_ACCESS = "555043308599"

# Roles with Access: multiple | Roles without Access: 0 | Selected Role: No
# any tests that use this should have tag @multiple_access
MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES = "555043308597"

# Roles with Access: multiple | Roles without Access: multiple | Selected Role: Yes
# any tests that use this should have tag @multiple_access_pre_selected
MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE = "555043304334"

# Roles with Access: 1 | Roles without Access: 0 | Selected Role: No
# any tests that use this should have tag @single_access
MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE = "555043300081"

# Roles with Access: 1 | Roles without Access: multiple | Selected Role: No
# any tests that use this should have tag @multiple_roles_single_access
MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT = "555043303526"

# Roles with Access: 0 | Roles without Access: multiple | Selected Role: No
# any tests that use this should have tag @multiple_roles_no_access
MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE = "555083343101"

# Roles with Access: 0 | Roles without Access: 0 | Selected Role: No
# any tests that use this should have tag @no_roles_no_access
# this is not currently used
MOCK_CIS2_LOGIN_ID_NO_ROLES = "555073103101"

account_scenario_tags = {
    "multiple_access": MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES,
    "multiple_access_pre_selected": MOCK_CIS2_LOGIN_ID_MULTIPLE_ACCESS_ROLES_WITH_SELECTED_ROLE,
    "single_access": MOCK_CIS2_LOGIN_ID_SINGLE_ACCESS_ROLE,
    "multiple_roles_single_access": MOCK_CIS2_LOGIN_ID_SINGLE_ROLE_WITH_ACCESS_MULTIPLE_WITHOUT,
    "multiple_roles_no_access": MOCK_CIS2_LOGIN_ID_NO_ACCESS_ROLE,
    "no_roles_no_access": MOCK_CIS2_LOGIN_ID_NO_ROLES,
}

REPOS = {
    "CPTS-UI": "https://github.com/NHSDigital/eps-prescription-tracker-ui",
    "CPTS-FHIR": "https://github.com/NHSDigital/electronic-prescription-service-clinical-prescription-tracker",
    "EPS-FHIR": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "EPS-FHIR-PRESCRIBING": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "EPS-FHIR-DISPENSING": "https://github.com/NHSDigital/electronic-prescription-service-api",
    "PFP-APIGEE": "https://github.com/NHSDigital/prescriptions-for-patients",
    "PFP-AWS": "https://github.com/NHSDigital/prescriptionsforpatients",
    "PSU": "https://github.com/NHSDigital/eps-prescription-status-update-api",
}

CERTIFICATE = os.getenv("CERTIFICATE")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_KID = os.getenv("JWT_KID")
HEADLESS = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")
SLOWMO = float(os.getenv("SLOWMO", "0.0"))

CPTS_UI_PREFIX = "cpt-ui"
CPTS_FHIR_SUFFIX = "clinical-prescription-tracker"
EPS_FHIR_SUFFIX = "electronic-prescriptions"
EPS_FHIR_PRESCRIBING_SUFFIX = "fhir-prescribing"
EPS_FHIR_DISPENSING_SUFFIX = "fhir-dispensing"
PFP_SUFFIX = "prescriptions-for-patients"
PSU_SUFFIX = "prescription-status-update"


class ConflictException(Exception):
    pass


class TestingSupportFailure(Exception):
    pass


def clear_scenario_user_sessions(context, scenario_tags):
    conflict_tags = set(account_scenario_tags)

    conflict = conflict_tags.intersection(scenario_tags)
    if len(conflict) > 1:
        raise ConflictException(
            f"You're attempting to use conflicting account credential tags in scenario {context.scenario.name}"
        )

    for tag in scenario_tags:
        for key, value in account_scenario_tags.items():
            if tag == key:
                request_id = str(uuid.uuid4())
                print(
                    f"Logging out all sessions for Mock_{value} ahead of running {context.scenario.name}.\
                        Request ID: {request_id}"
                )
                payload = json.dumps(
                    {"username": "Mock_" + value, "request_id": request_id}
                )
                # Not catching any exceptions, we want this to raise a stack if it doesn't work
                response = requests.post(
                    f"{context.cpts_ui_base_url}/api/test-support-clear-active-session",
                    data=payload,
                    headers={
                        "Source": f"{context.scenario.name}",
                    },
                    timeout=60,
                )
                if response.json()["message"] != "Success":
                    print(response)
                    raise TestingSupportFailure("Failed to clear active sessions")


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


def before_feature(context, feature):
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
        return
    environment = context.config.userdata["env"].lower()
    if "skip-sandbox" in feature.tags and "sandbox" in environment:
        feature.skip("Marked with @skip-sandbox")
        return


def before_scenario(context, scenario):
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
        return
    environment = context.config.userdata["env"].lower()
    if "skip-sandbox" in scenario.effective_tags and "sandbox" in environment:
        scenario.skip("Marked with @skip-sandbox")
        return
    if "deployed_only" in scenario.effective_tags and environment == "localhost":
        scenario.skip("Marked as only to run in deployed environments")
        return
    product = context.config.userdata["product"].upper()
    if product == "CPTS-UI":
        clear_scenario_user_sessions(context, scenario.effective_tags)

        global _playwright  # noqa: F824
        global _page  # noqa:
        expect.set_options(timeout=10_000)
        # Playwright supports browser contexts that allow for isolated instances
        # See: https://playwright.dev/python/docs/browser-contexts
        context.primary_context = context.browser.new_context()
        context.concurrent_context = context.browser.new_context()

        # Set primary context as default
        # Concurrent context usage is only need in concurrent scenarios
        context.primary_context.add_init_script(
            """
            window.__copiedText = "";
            navigator.clipboard.writeText = (text) => {
                window.__copiedText = text;
                return Promise.resolve();
            };
        """
        )
        context.primary_context.tracing.start(
            screenshots=True, snapshots=True, sources=True
        )

        context.concurrent_context.add_init_script(
            """
            window.__copiedText = "";
            navigator.clipboard.writeText = (text) => {
                window.__copiedText = text;
                return Promise.resolve();
            };
        """
        )
        context.concurrent_context.tracing.start(
            screenshots=True, snapshots=True, sources=True
        )

        context.active_page = context.primary_context.new_page()
        _page = context.active_page
        set_page(context, _page)


def after_scenario(context, scenario):
    product = context.config.userdata["product"].upper()
    if product == "CPTS-UI":
        if hasattr(context.browser, "tracing"):
            context.browser.tracing.stop(path="/tmp/trace.zip")
        if hasattr(context, "page"):
            if scenario.status == "failed":
                allure.attach(
                    context.active_page.screenshot(),
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach.file(
                    "/tmp/trace.zip",
                    name="playwright_failure_trace.zip",
                    attachment_type="application/zip",
                )
            if context.active_page is not None:
                global _page  # noqa: F824
                _page.close()


def before_all(context):
    product = context.config.userdata["product"].upper()
    if count_of_scenarios_to_run(context) != 0:
        env = context.config.userdata["env"].upper()
        print(f"Environment: {env}")

        # Currently, only the CPT-UI product is supported for local testing
        if env == "LOCALHOST":
            context.cpts_ui_base_url = LOCALHOST_URL

        else:
            context.cpts_ui_base_url = (
                f"https://{CPTS_UI_PREFIX}" + select_aws_base_url(env)
            )

        context.eps_fhir_base_url = os.path.join(
            select_apigee_base_url(env), EPS_FHIR_SUFFIX
        )
        context.eps_fhir_prescribing_base_url = os.path.join(
            select_apigee_base_url(env), EPS_FHIR_PRESCRIBING_SUFFIX
        )
        context.eps_fhir_dispensing_base_url = os.path.join(
            select_apigee_base_url(env), EPS_FHIR_DISPENSING_SUFFIX
        )
        context.pfp_base_url = os.path.join(select_apigee_base_url(env), PFP_SUFFIX)
        context.psu_base_url = os.path.join(select_apigee_base_url(env), PSU_SUFFIX)
        context.cpts_fhir_base_url = os.path.join(
            select_apigee_base_url(env), CPTS_FHIR_SUFFIX
        )

        if PULL_REQUEST_ID and env != "LOCALHOST":
            print(f"--- Using pull request id: '{PULL_REQUEST_ID}'")
            pull_request_id = PULL_REQUEST_ID.lower()
            if "pr-" in pull_request_id:
                get_url_with_pr(context, env, product)

    else:
        print("no tests to run. Check your tags and try again")
        sys.exit(0)
    print(f"Run using arm64 version of Chromium: {context.config.userdata['arm64']}")
    if product == "CPTS-UI":
        global _playwright
        _playwright = sync_playwright().start()
        context.browser = _playwright.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOWMO,
            channel=(
                None if context.config.userdata["arm64"].upper() == "TRUE" else "chrome"
            ),
        )
        # For usage in concurrent session scenarios
        # context.primary_context = context.browser.new_context()
        # context.concurrent_context = context.browser.new_context()
        # context.active_browser_context = context.primary_context  # Set browser context by default

    eps_api_methods.calculate_eps_fhir_base_url(context)
    print("CPTS-UI: ", context.cpts_ui_base_url)
    print("CPTS-FHIR: ", context.cpts_fhir_base_url)
    print("EPS: ", context.eps_fhir_base_url)
    print("EPS-PRESCRIBING: ", context.eps_fhir_prescribing_base_url)
    print("EPS-DISPENSING: ", context.eps_fhir_dispensing_base_url)
    print("PFP: ", context.pfp_base_url)
    print("PSU: ", context.psu_base_url)


def get_url_with_pr(context, env, product):
    assert PULL_REQUEST_ID is not None
    pull_request_id = PULL_REQUEST_ID.lower()
    if product == "EPS-FHIR":
        context.eps_fhir_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{EPS_FHIR_SUFFIX}-{pull_request_id}"
        )
    if product in ["EPS-FHIR-PRESCRIBING", "EPS-FHIR-DISPENSING"]:
        context.eps_fhir_prescribing_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL,
            f"{EPS_FHIR_PRESCRIBING_SUFFIX}-{pull_request_id}",
        )
        context.eps_fhir_dispensing_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL,
            f"{EPS_FHIR_DISPENSING_SUFFIX}-{pull_request_id}",
        )
    if product == "PFP-APIGEE":
        context.pfp_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PFP_SUFFIX}-{pull_request_id}"
        )
    if product == "PSU":
        context.psu_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{PSU_SUFFIX}-{pull_request_id}"
        )
    if product == "PFP-AWS":
        handle_pfp_aws_pr_url(context, env)
    if product == "CPTS-UI":
        handle_cpt_ui_pr_url(context, env)
    if product == "CPTS-FHIR":
        context.cpts_fhir_base_url = os.path.join(
            INTERNAL_DEV_BASE_URL, f"{CPTS_FHIR_SUFFIX}-{pull_request_id}"
        )


def handle_cpt_ui_pr_url(context, env):
    assert PULL_REQUEST_ID is not None
    pull_request_id = PULL_REQUEST_ID.lower()
    context.cpts_ui_base_url = (
        f"https://{CPTS_UI_PREFIX}-{pull_request_id}{select_apigee_base_url(env)}"
    )
    if env == "INTERNAL-DEV":
        context.cpts_ui_base_url = CPTS_UI_PR_URL.replace(
            "{{aws_pull_request_id}}", pull_request_id
        )
    if env == "INTERNAL-DEV-SANDBOX":
        context.cpts_ui_base_url = CPTS_UI_SANDBOX_PR_URL.replace(
            "{{aws_pull_request_id}}", pull_request_id
        )


def handle_pfp_aws_pr_url(context, env):
    assert PULL_REQUEST_ID is not None
    pull_request_id = PULL_REQUEST_ID.lower()
    context.pfp_base_url = os.path.join(
        INTERNAL_DEV_BASE_URL, f"{PFP_SUFFIX}-{pull_request_id}"
    )
    if env == "INTERNAL-DEV":
        context.pfp_base_url = PFP_AWS_PR_URL.replace(
            "{{aws_pull_request_id}}", pull_request_id
        )
    if env == "INTERNAL-DEV-SANDBOX":
        context.pfp_base_url = PFP_AWS_SANDBOX_PR_URL.replace(
            "{{aws_pull_request_id}}", pull_request_id
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
        if "_page" in vars() or "_page" in globals():
            _page.close()


def setup_logging(level: int = logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
        handlers=handlers,
    )


def select_apigee_base_url(env):
    if env in APIGEE_ENVS:
        return APIGEE_ENVS[env]
    raise ValueError(f"Unknown environment or missing base URL for: {env} .")


def select_aws_base_url(env):
    if env in AWS_ENVS:
        return AWS_ENVS[env]
    raise ValueError(f"Unknown environment or missing base URL for: {env} .")


def select_repository_base_url(product):
    if product in REPOS:
        return REPOS[product]
    raise ValueError(f"Unknown product or missing repository URL for: {product} .")


def write_properties_file(file_path, properties_dict):
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        for key, value in properties_dict.items():
            file.write(f"{key}={value}\n")


def get_page(self):
    return self._page


def set_page(self, _page):
    self._page = _page
