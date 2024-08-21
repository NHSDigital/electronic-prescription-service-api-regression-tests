import json

# pylint: disable=no-name-in-module
from behave import when, then  # pyright: ignore [reportAttributeAccessIssue]

from methods.api.psu_api_methods import send_status_update
from methods.shared.common import assert_that, get_auth


@when("I am authenticated")
def i_am_authenticated(context):
    env = context.config.userdata["env"].lower()
    if "sandbox" in env:
        return
    context.auth_token = get_auth("dispenser", env, "PFP-APIGEE")
