from behave import then, when  # pyright: ignore [reportGeneralTypeIssues]
from methods import api_methods
from methods.api_methods import assert_that


@when("I make a request to the ping endpoint")
def i_make_a_request_to_the_ping_endpoint(context):
    api_methods.request_ping(context)


@then("I get a {status_code:n} response code")
def i_get_a_status_code(context, status_code: int):
    api_methods.the_expected_response_code_is_returned(context, status_code)


@then("I can see the version information in the response")
def i_see_version_in_response(context):
    response = context.response.json()
    assert_that(response["version"], context).is_not_none()


@then("I can see the revision information in the response")
def i_see_revision_in_response(context):
    response = context.response.json()
    assert_that(response["revision"], context).is_not_none()


@then("I can see the releaseId information in the response")
def i_see_release_id_in_response(context):
    response = context.response.json()
    assert_that(response["releaseId"], context).is_not_none()


@then("I can see the commitId information in the response")
def i_see_commit_id_in_response(context):
    response = context.response.json()
    assert_that(response["commitId"], context).is_not_none()


@then("I can see the ping information in the response")
def step_impl(context):
    i_see_version_in_response(context)
    i_see_revision_in_response(context)
    i_see_release_id_in_response(context)
    i_see_commit_id_in_response(context)
