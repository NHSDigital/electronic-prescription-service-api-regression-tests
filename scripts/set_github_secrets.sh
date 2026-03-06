#!/usr/bin/env bash

check_gh_logged_in() {
    if ! gh auth status >/dev/null 2>&1; then
        echo "You need to login using gh auth login"
        exit 1
    fi
}

get_aws_secret() {
    local secret_path=$1

    if [ -z "${secret_path}" ]; then
        echo "get_aws_secret requires the AWS secret path" >&2
        return 1
    fi

    local secret_value
    if secret_value=$(aws secretsmanager get-secret-value \
        --secret-id "${secret_path}" \
        --query SecretString \
        --output text 2>/dev/null) && [ "${secret_value}" != "None" ]; then
        printf '%s' "${secret_value}"
        return 0
    fi

    if secret_value=$(aws secretsmanager get-secret-value \
        --secret-id "${secret_path}" \
        --query SecretBinary \
        --output text 2>/dev/null) && [ "${secret_value}" != "None" ]; then
        printf '%s' "${secret_value}" | base64 --decode
        return 0
    fi

    echo "Failed to retrieve AWS secret for ${secret_path}" >&2
    return 1
}

set_github_environment_secret() {
    secret_name=$1
    secret_path=$2
    environment=$3
    if [ -z "${secret_name}" ]; then
        echo "value passed for secret ${secret_name} is unset or set to the empty string. Not setting"
        return 0
    fi
    if [ -z "${secret_path}" ]; then
        echo "value passed for secret ${secret_path} is unset or set to the empty string. Not setting"
        return 0
    fi
    secret_value=$(get_aws_secret "${secret_path}")
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
set_github_environment_secret CPT_FHIR_CLIENT_ID "/regression-tests/REF/CPT_FHIR_CLIENT_ID" REF
set_github_environment_secret CPT_FHIR_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/CPT_FHIR_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret CPT_FHIR_CLIENT_ID "/regression-tests/INTERNAL_DEV/CPT_FHIR_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret CPT_FHIR_CLIENT_ID "/regression-tests/INT/CPT_FHIR_CLIENT_ID" INT
set_github_environment_secret CPT_FHIR_CLIENT_ID "/regression-tests/INTERNAL_QA/CPT_FHIR_CLIENT_ID" INTERNAL-QA

set_github_environment_secret CPT_FHIR_CLIENT_SECRET "/regression-tests/REF/CPT_FHIR_CLIENT_SECRET" REF
set_github_environment_secret CPT_FHIR_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/CPT_FHIR_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret CPT_FHIR_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/CPT_FHIR_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret CPT_FHIR_CLIENT_SECRET "/regression-tests/INT/CPT_FHIR_CLIENT_SECRET" INT
set_github_environment_secret CPT_FHIR_CLIENT_SECRET "/regression-tests/INTERNAL_QA/CPT_FHIR_CLIENT_SECRET" INTERNAL-QA

# EPS_FHIR credentials
set_github_environment_secret EPS_FHIR_CLIENT_ID "/regression-tests/REF/EPS_FHIR_CLIENT_ID" REF
set_github_environment_secret EPS_FHIR_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_CLIENT_ID "/regression-tests/INTERNAL_DEV/EPS_FHIR_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_CLIENT_ID "/regression-tests/INT/EPS_FHIR_CLIENT_ID" INT
set_github_environment_secret EPS_FHIR_CLIENT_ID "/regression-tests/INTERNAL_QA/EPS_FHIR_CLIENT_ID" INTERNAL-QA

set_github_environment_secret EPS_FHIR_CLIENT_SECRET "/regression-tests/REF/EPS_FHIR_CLIENT_SECRET" REF
set_github_environment_secret EPS_FHIR_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/EPS_FHIR_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_CLIENT_SECRET "/regression-tests/INT/EPS_FHIR_CLIENT_SECRET" INT
set_github_environment_secret EPS_FHIR_CLIENT_SECRET "/regression-tests/INTERNAL_QA/EPS_FHIR_CLIENT_SECRET" INTERNAL-QA

# EPS_FHIR_SHA1 credentials
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_ID "/regression-tests/REF/EPS_FHIR_SHA1_CLIENT_ID" REF
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_SHA1_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_ID "/regression-tests/INTERNAL_DEV/EPS_FHIR_SHA1_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_ID "/regression-tests/INT/EPS_FHIR_SHA1_CLIENT_ID" INT
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_ID "/regression-tests/INTERNAL_QA/EPS_FHIR_SHA1_CLIENT_ID" INTERNAL-QA

set_github_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "/regression-tests/REF/EPS_FHIR_SHA1_CLIENT_SECRET" REF
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_SHA1_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/EPS_FHIR_SHA1_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "/regression-tests/INT/EPS_FHIR_SHA1_CLIENT_SECRET" INT
set_github_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "/regression-tests/INTERNAL_QA/EPS_FHIR_SHA1_CLIENT_SECRET" INTERNAL-QA


# EPS_FHIR_PRESCRIBING credentials
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "/regression-tests/REF/EPS_FHIR_PRESCRIBING_CLIENT_ID" REF
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_PRESCRIBING_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "/regression-tests/INTERNAL_DEV/EPS_FHIR_PRESCRIBING_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "/regression-tests/INT/EPS_FHIR_PRESCRIBING_CLIENT_ID" INT
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "/regression-tests/INTERNAL_QA/EPS_FHIR_PRESCRIBING_CLIENT_ID" INTERNAL-QA

set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "/regression-tests/REF/EPS_FHIR_PRESCRIBING_CLIENT_SECRET" REF
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_PRESCRIBING_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/EPS_FHIR_PRESCRIBING_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "/regression-tests/INT/EPS_FHIR_PRESCRIBING_CLIENT_SECRET" INT
set_github_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "/regression-tests/INTERNAL_QA/EPS_FHIR_PRESCRIBING_CLIENT_SECRET" INTERNAL-QA


# EPS_FHIR_SHA1_PRESCRIBING credentials
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "/regression-tests/REF/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID" REF
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "/regression-tests/INTERNAL_DEV/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "/regression-tests/INT/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID" INT
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "/regression-tests/INTERNAL_QA/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID" INTERNAL-QA

set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "/regression-tests/REF/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET" REF
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "/regression-tests/INT/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET" INT
set_github_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "/regression-tests/INTERNAL_QA/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET" INTERNAL-QA

# EPS_FHIR_DISPENSING credentials
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "/regression-tests/REF/EPS_FHIR_DISPENSING_CLIENT_ID" REF
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_DISPENSING_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "/regression-tests/INTERNAL_DEV/EPS_FHIR_DISPENSING_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "/regression-tests/INT/EPS_FHIR_DISPENSING_CLIENT_ID" INT
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "/regression-tests/INTERNAL_QA/EPS_FHIR_DISPENSING_CLIENT_ID" INTERNAL-QA

set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "/regression-tests/REF/EPS_FHIR_DISPENSING_CLIENT_SECRET" REF
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_DISPENSING_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/EPS_FHIR_DISPENSING_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "/regression-tests/INT/EPS_FHIR_DISPENSING_CLIENT_SECRET" INT
set_github_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "/regression-tests/INTERNAL_QA/EPS_FHIR_DISPENSING_CLIENT_SECRET" INTERNAL-QA

# EPS_FHIR_DISPENSING_JWT credentials
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY "/regression-tests/REF/EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY" REF
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY "/regression-tests/INTERNAL_DEV/EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY "/regression-tests/INT/EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY" INT
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY "/regression-tests/INTERNAL_QA/EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY" INTERNAL-QA

set_github_environment_secret EPS_FHIR_DISPENSING_JWT_KID "/regression-tests/REF/EPS_FHIR_DISPENSING_JWT_KID" REF
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_KID "/regression-tests/INTERNAL_DEV_SANDBOX/EPS_FHIR_DISPENSING_JWT_KID" INTERNAL-DEV-SANDBOX
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_KID "/regression-tests/INTERNAL_DEV/EPS_FHIR_DISPENSING_JWT_KID" INTERNAL-DEV
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_KID "/regression-tests/INT/EPS_FHIR_DISPENSING_JWT_KID" INT
set_github_environment_secret EPS_FHIR_DISPENSING_JWT_KID "/regression-tests/INTERNAL_QA/EPS_FHIR_DISPENSING_JWT_KID" INTERNAL-QA

# PFP credentials
set_github_environment_secret PFP_CLIENT_ID "/regression-tests/REF/PFP_CLIENT_ID" REF
set_github_environment_secret PFP_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/PFP_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret PFP_CLIENT_ID "/regression-tests/INTERNAL_DEV/PFP_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret PFP_CLIENT_ID "/regression-tests/INT/PFP_CLIENT_ID" INT
set_github_environment_secret PFP_CLIENT_ID "/regression-tests/INTERNAL_QA/PFP_CLIENT_ID" INTERNAL-QA

set_github_environment_secret PFP_CLIENT_SECRET "/regression-tests/REF/PFP_CLIENT_SECRET" REF
set_github_environment_secret PFP_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/PFP_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret PFP_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/PFP_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret PFP_CLIENT_SECRET "/regression-tests/INT/PFP_CLIENT_SECRET" INT
set_github_environment_secret PFP_CLIENT_SECRET "/regression-tests/INTERNAL_QA/PFP_CLIENT_SECRET" INTERNAL-QA

# PSU credentials
set_github_environment_secret PSU_CLIENT_ID "/regression-tests/REF/PSU_CLIENT_ID" REF
set_github_environment_secret PSU_CLIENT_ID "/regression-tests/INTERNAL_DEV_SANDBOX/PSU_CLIENT_ID" INTERNAL-DEV-SANDBOX
set_github_environment_secret PSU_CLIENT_ID "/regression-tests/INTERNAL_DEV/PSU_CLIENT_ID" INTERNAL-DEV
set_github_environment_secret PSU_CLIENT_ID "/regression-tests/INT/PSU_CLIENT_ID" INT
set_github_environment_secret PSU_CLIENT_ID "/regression-tests/INTERNAL_QA/PSU_CLIENT_ID" INTERNAL-QA

set_github_environment_secret PSU_CLIENT_SECRET "/regression-tests/REF/PSU_CLIENT_SECRET" REF
set_github_environment_secret PSU_CLIENT_SECRET "/regression-tests/INTERNAL_DEV_SANDBOX/PSU_CLIENT_SECRET" INTERNAL-DEV-SANDBOX
set_github_environment_secret PSU_CLIENT_SECRET "/regression-tests/INTERNAL_DEV/PSU_CLIENT_SECRET" INTERNAL-DEV
set_github_environment_secret PSU_CLIENT_SECRET "/regression-tests/INT/PSU_CLIENT_SECRET" INT
set_github_environment_secret PSU_CLIENT_SECRET "/regression-tests/INTERNAL_QA/PSU_CLIENT_SECRET" INTERNAL-QA

# jwt
set_github_environment_secret JWT_KID "/regression-tests/REF/JWT_KID" REF
set_github_environment_secret JWT_KID "/regression-tests/INTERNAL_DEV_SANDBOX/JWT_KID" INTERNAL-DEV-SANDBOX
set_github_environment_secret JWT_KID "/regression-tests/INTERNAL_DEV/JWT_KID" INTERNAL-DEV
set_github_environment_secret JWT_KID "/regression-tests/INT/JWT_KID" INT
set_github_environment_secret JWT_KID "/regression-tests/INTERNAL_QA/JWT_KID" INTERNAL-QA

set_github_environment_secret JWT_PRIVATE_KEY "/regression-tests/REF/JWT_PRIVATE_KEY" REF
set_github_environment_secret JWT_PRIVATE_KEY "/regression-tests/INTERNAL_DEV_SANDBOX/JWT_PRIVATE_KEY" INTERNAL-DEV-SANDBOX
set_github_environment_secret JWT_PRIVATE_KEY "/regression-tests/INTERNAL_DEV/JWT_PRIVATE_KEY" INTERNAL-DEV
set_github_environment_secret JWT_PRIVATE_KEY "/regression-tests/INT/JWT_PRIVATE_KEY" INT
set_github_environment_secret JWT_PRIVATE_KEY "/regression-tests/INTERNAL_QA/JWT_PRIVATE_KEY" INTERNAL-QA

# automerge apps
set_repository_secret AUTOMERGE_APP_ID "${AUTOMERGE_APP_ID}"
set_repository_secret AUTOMERGE_PEM "${AUTOMERGE_PEM}"

# signing certificate
set_repository_secret CERTIFICATE "${CERTIFICATE}"
set_repository_secret PRIVATE_KEY "${PRIVATE_KEY}"

set_repository_secret REGRESSION_TESTS_PEM "${REGRESSION_TESTS_PEM}"

# sonar token
set_repository_secret SONAR_TOKEN "${SONAR_TOKEN}"

# APIGEE
set_repository_secret APIGEE_USER "${APIGEE_USER}"
set_repository_secret APIGEE_PASSWORD "${APIGEE_PASSWORD}"
set_repository_secret APIGEE_MFA_SECRET "${APIGEE_MFA_SECRET}"
