import logging
import os
import sys
from dotenv import load_dotenv
from logging import DEBUG, INFO

load_dotenv()

if not os.getenv("BASE_URL"):
    raise EnvironmentError(
        """BASE_URL environment variable is not set on this machine. Tests will not run.
        See 'readme.md' for more information on how to set this variable"""
    )
DEV_BASE_URL = os.getenv("DEV_BASE_URL")
QA_BASE_URL = os.getenv("QA_BASE_URL")
INT_BASE_URL = os.getenv("INT_BASE_URL")

ENVS = {
    "DEV": DEV_BASE_URL,
    "QA": QA_BASE_URL,
    "INT": INT_BASE_URL,
}

PULL_REQUEST_ID = os.getenv("PULL_REQUEST_ID")

def before_all(context):
    if is_debug(context):
        setup_logging(level=DEBUG)
    else:
        setup_logging(level=INFO)
        
    eps_pr_suffix = "electronic-prescriptions" + build_pull_request_id(PULL_REQUEST_ID)
    base_url = select_base_url()
    
    if PULL_REQUEST_ID:
        context.base_url = DEV_BASE_URL + eps_pr_suffix
    
    context.base_url = base_url + eps_pr_suffix
    
    logging.info("Using BASE_URL: '%s'", context.base_url)

def after_all(context):
    return
    # Add anything you want to happen after all the tests have completed here


def setup_logging(level: int = logging.INFO):
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=level,
        handlers=handlers,
    )


def is_debug(context):
    try:
        debug = context.config.userdata["debug"]
    except KeyError:
        print("Running in Normal mode")
        return False
    if str(debug) == "True":
        print("Running in DEBUG mode")
        return True
    print("Running in Normal mode")
    return False

def build_pull_request_id(id):
    pr_suffix = f"-pr-{id}" if id else ""
    return pr_suffix

def select_base_url(env):
    if env in ENVS:
        return ENVS[env]
    else:
        raise ValueError(f"Unknown environment or missing base URL for: {env} .")


# add logic on before all to check the existence of PR ID and enforce internal dev base url if it exists
# check if it works
# if so call Anth to confirm changes on EPS repo