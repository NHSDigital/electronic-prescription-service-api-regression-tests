import logging
import os
import subprocess
import sys
from logging import DEBUG, INFO

if not os.getenv("BASE_URL"):
    raise EnvironmentError(
        """BASE_URL environment variable is not set on this machine. Tests will not run.
        See 'readme.md' for more information on how to set this variable"""
    )
BASE_URL = os.getenv("BASE_URL")


def before_all(context):
    if is_debug(context):
        setup_logging(level=DEBUG)
    else:
        setup_logging(level=INFO)
    context.base_url = BASE_URL
    logging.info("Using BASE_URL: '%s'", context.base_url)


def after_all(context):
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
