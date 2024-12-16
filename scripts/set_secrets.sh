#!/usr/bin/env bash

check_gh_logged_in() {
    if ! gh auth status >/dev/null 2>&1; then
        echo "You need to login using gh auth login"
        exit 1
    fi
}

set_environment_secret() {
    secret_name=$1
    secret_value=$2
    environment=$3
    if [ -z "${secret_value}" ]; then
        echo "value passed for secret ${secret_name} is unset or set to the empty string. Not setting"
        return 0
    fi
    echo "setting value for ${secret_name}"
    echo "secret_value: ${secret_value}"
    read -r -p "Press Enter to set secret or ctrl+c to exit"
    gh secret set "${secret_name}" \
        --repo NHSDigital/electronic-prescription-service-api-regression-tests \
        --app actions \
        --env "${environment}" \
        --body "${secret_value}"
}

set_repository_secret() {
    secret_name=$1
    secret_value=$2
    if [ -z "${secret_value}" ]; then
        echo "value passed for secret ${secret_name} is unset or set to the empty string. Not setting"
        return 0
    fi
    echo "setting value for ${secret_name}"
    echo "secret_value: ${secret_value}"
    read -r -p "Press Enter to set secret or ctrl+c to exit"
    gh secret set "${secret_name}" \
        --repo NHSDigital/electronic-prescription-service-api-regression-tests \
        --app actions \
        --body "${secret_value}"
}

check_gh_logged_in
set_environment_secret CLIENT_ID "${REF_CLIENT_ID}" REF
set_environment_secret CLIENT_ID "${INTERNAL_DEV_SANDBOX_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret CLIENT_ID "${INTERNAL_DEV_CLIENT_ID}" INTERNAL-DEV
set_environment_secret CLIENT_ID "${INT_CLIENT_ID}" INT
set_environment_secret CLIENT_ID "${INTERNAL_QA_CLIENT_ID}" INTERNAL-QA

set_environment_secret CLIENT_SECRET "${REF_CLIENT_SECRET}" REF
set_environment_secret CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret CLIENT_SECRET "${INTERNAL_DEV_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret CLIENT_SECRET "${INT_CLIENT_SECRET}" INT
set_environment_secret CLIENT_SECRET "${INTERNAL_QA_CLIENT_SECRET}" INTERNAL-QA

set_environment_secret JWT_KID "${REF_JWT_KID}" REF
set_environment_secret JWT_KID "${INTERNAL_DEV_SANDBOX_JWT_KID}" INTERNAL-DEV-SANDBOX
set_environment_secret JWT_KID "${INTERNAL_DEV_JWT_KID}" INTERNAL-DEV
set_environment_secret JWT_KID "${INT_JWT_KID}" INT
set_environment_secret JWT_KID "${INTERNAL_QA_JWT_KID}" INTERNAL-QA

set_environment_secret JWT_PRIVATE_KEY "${REF_JWT_PRIVATE_KEY}" REF
set_environment_secret JWT_PRIVATE_KEY "${INTERNAL_DEV_SANDBOX_JWT_PRIVATE_KEY}" INTERNAL-DEV-SANDBOX
set_environment_secret JWT_PRIVATE_KEY "${INTERNAL_DEV_JWT_PRIVATE_KEY}" INTERNAL-DEV
set_environment_secret JWT_PRIVATE_KEY "${INT_JWT_PRIVATE_KEY}" INT
set_environment_secret JWT_PRIVATE_KEY "${INTERNAL_QA_JWT_PRIVATE_KEY}" INTERNAL-QA

set_environment_secret SHA1_CLIENT_ID "${REF_SHA1_CLIENT_ID}" REF
set_environment_secret SHA1_CLIENT_ID "${INTERNAL_DEV_SANDBOX_SHA1_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret SHA1_CLIENT_ID "${INTERNAL_DEV_SHA1_CLIENT_ID}" INTERNAL-DEV
set_environment_secret SHA1_CLIENT_ID "${INT_SHA1_CLIENT_ID}" INT
set_environment_secret SHA1_CLIENT_ID "${INTERNAL_QA_SHA1_CLIENT_ID}" INTERNAL-QA

set_environment_secret SHA1_CLIENT_SECRET "${REF_SHA1_CLIENT_SECRET}" REF
set_environment_secret SHA1_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_SHA1_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret SHA1_CLIENT_SECRET "${INTERNAL_DEV_SHA1_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret SHA1_CLIENT_SECRET "${INT_SHA1_CLIENT_SECRET}" INT
set_environment_secret SHA1_CLIENT_SECRET "${INTERNAL_QA_SHA1_CLIENT_SECRET}" INTERNAL-QA

set_repository_secret AUTOMERGE_APP_ID "${AUTOMERGE_APP_ID}"
set_repository_secret AUTOMERGE_PEM "${AUTOMERGE_PEM}"
set_repository_secret CERTIFICATE "${CERTIFICATE}"
set_repository_secret PRIVATE_KEY "${PRIVATE_KEY}"
set_repository_secret REGRESSION_TESTS_PEM "${REGRESSION_TESTS_PEM}"
set_repository_secret SONAR_TOKEN "${SONAR_TOKEN}"
