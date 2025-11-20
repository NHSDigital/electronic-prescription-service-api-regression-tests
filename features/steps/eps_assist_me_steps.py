"""
EPS Assist Me direct lambda invocation step definitions

enables regression testing of slack bot functionality via direct lambda calls,
bypassing slack infrastructure for reliable automated validation.
"""

import json
import boto3
from behave import given, when, then  # type: ignore
from methods.shared.common import assert_that


# lambda client instance
lambda_client = None


def get_lambda_client(credentials):
    """initialise lambda client with assumed role credentials"""
    global lambda_client
    if lambda_client is None:
        lambda_client = boto3.client(
            "lambda",
            region_name="eu-west-2",
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
            aws_session_token=credentials["aws_session_token"],
        )
    return lambda_client


def get_lambda_function_name(context) -> str:
    """construct lambda function name from environment context"""
    client = boto3.client(
        "cloudformation",
        region_name="eu-west-2",
        aws_access_key_id=context.aws_credentials["aws_access_key_id"],
        aws_secret_access_key=context.aws_credentials["aws_secret_access_key"],
        aws_session_token=context.aws_credentials["aws_session_token"],
    )
    paginator = client.get_paginator("list_exports")

    for page in paginator.paginate():
        for export in page["Exports"]:
            if export["Name"] == context.espamSlackBotFunctionName:
                return export["Value"]
    return ""


def invoke_lambda_direct(context, payload):
    """invoke lambda with direct invocation payload"""
    client = get_lambda_client(credentials=context.aws_credentials)
    function_name = get_lambda_function_name(context)

    response = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )

    return json.loads(response["Payload"].read().decode("utf-8"))


# === GIVEN STEPS ===


@given("A regression test suite is executed")
def regression_test_suite_executed(context):
    """initialise regression test context"""
    context.test_type = "regression"


@given("A regression test with multiple related queries")
def regression_test_multiple_queries(context):
    """prepare context for session continuity testing"""
    context.session_id = None
    context.responses = []


# === WHEN STEPS ===


@when("The test invokes the slackbot lambda with a direct invocation event")
def invoke_slackbot_direct(context):
    """perform basic direct invocation test"""
    payload = {
        "invocation_type": "direct",
        "query": "How do I authenticate with EPS API?",
    }
    context.response = invoke_lambda_direct(context, payload)


@when("Tests are run with session_id continuity")
def run_tests_with_session_continuity(context):
    """execute multiple queries maintaining session context"""
    # first query without session
    first_payload = {
        "invocation_type": "direct",
        "query": "How do I authenticate with EPS API?",
    }
    first_response = invoke_lambda_direct(context, first_payload)
    context.responses.append(first_response)

    # extract session_id for subsequent queries
    if first_response.get("statusCode") == 200:
        context.session_id = first_response["response"]["session_id"]

    # second query with session continuity
    second_payload = {
        "invocation_type": "direct",
        "query": "What scopes do I need?",
        "session_id": context.session_id,
    }
    second_response = invoke_lambda_direct(context, second_payload)
    context.responses.append(second_response)


# === THEN STEPS ===


@then("The lambda returns a structured AI response matching expected format")
def validate_structured_ai_response(context):
    """validate complete response structure compliance"""
    response = context.response

    # validate basic structure
    assert_that(response).contains_key("statusCode")
    assert_that(response).contains_key("response")
    assert_that(response["statusCode"]).is_equal_to(200)

    # validate response fields
    response_data = response["response"]
    assert_that(response_data).contains_key("text")
    assert_that(response_data).contains_key("session_id")
    assert_that(response_data).contains_key("citations")
    assert_that(response_data).contains_key("timestamp")

    # validate field types
    assert_that(response_data["text"]).is_not_empty()
    assert_that(response_data["citations"]).is_instance_of(list)


@then("Lambda maintains conversation context across invocations")
def validate_conversation_context(context):
    """verify session continuity maintained between queries"""
    assert_that(context.responses).is_not_empty()
    assert (
        len(context.responses) >= 2
    ), "Need at least 2 responses for context validation"

    # verify all responses successful
    for response in context.responses:
        assert_that(response["statusCode"]).is_equal_to(200)

    # verify same session_id across responses
    session_ids = []
    for response in context.responses:
        session_id = response["response"]["session_id"]
        if session_id:
            session_ids.append(session_id)

    assert_that(session_ids).is_not_empty()
    first_session_id = session_ids[0]
    for session_id in session_ids:
        assert_that(session_id).is_equal_to(first_session_id)
