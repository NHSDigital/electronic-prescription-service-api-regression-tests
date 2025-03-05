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
    echo
    echo "*****************************************"
    echo
    echo "setting value for ${secret_name} in environment ${environment}"
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
    echo
    echo "*****************************************"
    echo
    echo "setting value for ${secret_name}"
    echo "secret_value: ${secret_value}"
    read -r -p "Press Enter to set secret or ctrl+c to exit"
    gh secret set "${secret_name}" \
        --repo NHSDigital/electronic-prescription-service-api-regression-tests \
        --app actions \
        --body "${secret_value}"
}

check_gh_logged_in
# CPT_FHIR credentials
set_environment_secret CPT_FHIR_CLIENT_ID "${REF_CPT_FHIR_CLIENT_ID}" REF
set_environment_secret CPT_FHIR_CLIENT_ID "${INTERNAL_DEV_SANDBOX_CPT_FHIR_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret CPT_FHIR_CLIENT_ID "${INTERNAL_DEV_CPT_FHIR_CLIENT_ID}" INTERNAL-DEV
set_environment_secret CPT_FHIR_CLIENT_ID "${INT_CPT_FHIR_CLIENT_ID}" INT
set_environment_secret CPT_FHIR_CLIENT_ID "${INTERNAL_QA_CPT_FHIR_CLIENT_ID}" INTERNAL-QA

# EPS_FHIR credentials
set_environment_secret EPS_FHIR_CLIENT_ID "${REF_EPS_FHIR_CLIENT_ID}" REF
set_environment_secret EPS_FHIR_CLIENT_ID "${INTERNAL_DEV_SANDBOX_EPS_FHIR_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_CLIENT_ID "${INTERNAL_DEV_EPS_FHIR_CLIENT_ID}" INTERNAL-DEV
set_environment_secret EPS_FHIR_CLIENT_ID "${INT_EPS_FHIR_CLIENT_ID}" INT
set_environment_secret EPS_FHIR_CLIENT_ID "${INTERNAL_QA_EPS_FHIR_CLIENT_ID}" INTERNAL-QA

set_environment_secret EPS_FHIR_CLIENT_SECRET "${REF_EPS_FHIR_CLIENT_SECRET}" REF
set_environment_secret EPS_FHIR_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_EPS_FHIR_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_CLIENT_SECRET "${INTERNAL_DEV_EPS_FHIR_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret EPS_FHIR_CLIENT_SECRET "${INT_EPS_FHIR_CLIENT_SECRET}" INT
set_environment_secret EPS_FHIR_CLIENT_SECRET "${INTERNAL_QA_EPS_FHIR_CLIENT_SECRET}" INTERNAL-QA

# EPS_FHIR_SHA1 credentials
set_environment_secret EPS_FHIR_SHA1_CLIENT_ID "${REF_EPS_FHIR_SHA1_CLIENT_ID}" REF
set_environment_secret EPS_FHIR_SHA1_CLIENT_ID "${INTERNAL_DEV_SANDBOX_EPS_FHIR_SHA1_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_SHA1_CLIENT_ID "${INTERNAL_DEV_EPS_FHIR_SHA1_CLIENT_ID}" INTERNAL-DEV
set_environment_secret EPS_FHIR_SHA1_CLIENT_ID "${INT_EPS_FHIR_SHA1_CLIENT_ID}" INT
set_environment_secret EPS_FHIR_SHA1_CLIENT_ID "${INTERNAL_QA_EPS_FHIR_SHA1_CLIENT_ID}" INTERNAL-QA

set_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "${REF_EPS_FHIR_SHA1_CLIENT_SECRET}" REF
set_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_EPS_FHIR_SHA1_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "${INTERNAL_DEV_EPS_FHIR_SHA1_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "${INT_EPS_FHIR_SHA1_CLIENT_SECRET}" INT
set_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "${INTERNAL_QA_EPS_FHIR_SHA1_CLIENT_SECRET}" INTERNAL-QA


# EPS_FHIR_PRESCRIBING credentials
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "${REF_EPS_FHIR_PRESCRIBING_CLIENT_ID}" REF
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "${INTERNAL_DEV_SANDBOX_EPS_FHIR_PRESCRIBING_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "${INTERNAL_DEV_EPS_FHIR_PRESCRIBING_CLIENT_ID}" INTERNAL-DEV
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "${INT_EPS_FHIR_PRESCRIBING_CLIENT_ID}" INT
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "${INTERNAL_QA_EPS_FHIR_PRESCRIBING_CLIENT_ID}" INTERNAL-QA

set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "${REF_EPS_FHIR_PRESCRIBING_CLIENT_SECRET}" REF
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_EPS_FHIR_PRESCRIBING_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "${INTERNAL_DEV_EPS_FHIR_PRESCRIBING_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "${INT_EPS_FHIR_PRESCRIBING_CLIENT_SECRET}" INT
set_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "${INTERNAL_QA_EPS_FHIR_PRESCRIBING_CLIENT_SECRET}" INTERNAL-QA


# EPS_FHIR_SHA1_PRESCRIBING credentials
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "${REF_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID}" REF
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "${INTERNAL_DEV_SANDBOX_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "${INTERNAL_DEV_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID}" INTERNAL-DEV
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "${INT_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID}" INT
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "${INTERNAL_QA_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID}" INTERNAL-QA

set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "${REF_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET}" REF
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "${INTERNAL_DEV_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "${INT_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET}" INT
set_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "${INTERNAL_QA_EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET}" INTERNAL-QA

# EPS_FHIR_DISPENSING credentials
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "${REF_EPS_FHIR_DISPENSING_CLIENT_ID}" REF
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "${INTERNAL_DEV_SANDBOX_EPS_FHIR_DISPENSING_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "${INTERNAL_DEV_EPS_FHIR_DISPENSING_CLIENT_ID}" INTERNAL-DEV
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "${INT_EPS_FHIR_DISPENSING_CLIENT_ID}" INT
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "${INTERNAL_QA_EPS_FHIR_DISPENSING_CLIENT_ID}" INTERNAL-QA

set_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "${REF_EPS_FHIR_DISPENSING_CLIENT_SECRET}" REF
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_EPS_FHIR_DISPENSING_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "${INTERNAL_DEV_EPS_FHIR_DISPENSING_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "${INT_EPS_FHIR_DISPENSING_CLIENT_SECRET}" INT
set_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "${INTERNAL_QA_EPS_FHIR_DISPENSING_CLIENT_SECRET}" INTERNAL-QA

# PFP credentials
set_environment_secret PFP_CLIENT_ID "${REF_PFP_CLIENT_ID}" REF
set_environment_secret PFP_CLIENT_ID "${INTERNAL_DEV_SANDBOX_PFP_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret PFP_CLIENT_ID "${INTERNAL_DEV_PFP_CLIENT_ID}" INTERNAL-DEV
set_environment_secret PFP_CLIENT_ID "${INT_PFP_CLIENT_ID}" INT
set_environment_secret PFP_CLIENT_ID "${INTERNAL_QA_PFP_CLIENT_ID}" INTERNAL-QA

set_environment_secret PFP_CLIENT_SECRET "${REF_PFP_CLIENT_SECRET}" REF
set_environment_secret PFP_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_PFP_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret PFP_CLIENT_SECRET "${INTERNAL_DEV_PFP_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret PFP_CLIENT_SECRET "${INT_PFP_CLIENT_SECRET}" INT
set_environment_secret PFP_CLIENT_SECRET "${INTERNAL_QA_PFP_CLIENT_SECRET}" INTERNAL-QA

# PSU credentials
set_environment_secret PSU_CLIENT_ID "${REF_PSU_CLIENT_ID}" REF
set_environment_secret PSU_CLIENT_ID "${INTERNAL_DEV_SANDBOX_PSU_CLIENT_ID}" INTERNAL-DEV-SANDBOX
set_environment_secret PSU_CLIENT_ID "${INTERNAL_DEV_PSU_CLIENT_ID}" INTERNAL-DEV
set_environment_secret PSU_CLIENT_ID "${INT_PSU_CLIENT_ID}" INT
set_environment_secret PSU_CLIENT_ID "${INTERNAL_QA_PSU_CLIENT_ID}" INTERNAL-QA

set_environment_secret PSU_CLIENT_SECRET "${REF_PSU_CLIENT_SECRET}" REF
set_environment_secret PSU_CLIENT_SECRET "${INTERNAL_DEV_SANDBOX_PSU_CLIENT_SECRET}" INTERNAL-DEV-SANDBOX
set_environment_secret PSU_CLIENT_SECRET "${INTERNAL_DEV_PSU_CLIENT_SECRET}" INTERNAL-DEV
set_environment_secret PSU_CLIENT_SECRET "${INT_PSU_CLIENT_SECRET}" INT
set_environment_secret PSU_CLIENT_SECRET "${INTERNAL_QA_PSU_CLIENT_SECRET}" INTERNAL-QA

# jwt
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

# automerge apps
set_repository_secret AUTOMERGE_APP_ID "${AUTOMERGE_APP_ID}"
set_repository_secret AUTOMERGE_PEM "${AUTOMERGE_PEM}"

# signing certificate
set_repository_secret CERTIFICATE "${CERTIFICATE}"
set_repository_secret PRIVATE_KEY "${PRIVATE_KEY}"

set_repository_secret REGRESSION_TESTS_PEM "${REGRESSION_TESTS_PEM}"

# sonar token
set_repository_secret SONAR_TOKEN "${SONAR_TOKEN}"
