#!/usr/bin/env bash

# Allow ENVIRONMENT to be provided as the first argument or pre-set in the shell.
if [ -n "$1" ]; then
    ENVIRONMENT="$1"
elif [ -z "${ENVIRONMENT}" ]; then
    echo "Usage: $0 <environment> or set ENVIRONMENT beforehand" >&2
    exit 1
fi

export ENVIRONMENT

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

set_local_environment_secret() {
    local variable_name=$1
    local secret_path=$2

    if [ -z "${variable_name}" ] || [ -z "${secret_path}" ]; then
        echo "set_local_environment_secret requires both a variable name and AWS secret path" >&2
        return 1
    fi

    local secret_value
    if ! secret_value=$(get_aws_secret "${secret_path}"); then
        echo "Failed to set ${variable_name} from secret ${secret_path}" >&2
        return 1
    fi

    printf -v "${variable_name}" '%s' "${secret_value}"
    echo "Set ${variable_name} from AWS secret ${secret_path}"
    # shellcheck disable=SC2163
    export "${variable_name}"
}

set_local_environment_secret CPT_FHIR_CLIENT_ID "/regression-tests/${ENVIRONMENT}/CPT_FHIR_CLIENT_ID"
set_local_environment_secret CPT_FHIR_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/CPT_FHIR_CLIENT_SECRET"
set_local_environment_secret EPS_FHIR_CLIENT_ID "/regression-tests/${ENVIRONMENT}/EPS_FHIR_CLIENT_ID"
set_local_environment_secret EPS_FHIR_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/EPS_FHIR_CLIENT_SECRET"
set_local_environment_secret EPS_FHIR_SHA1_CLIENT_ID "/regression-tests/${ENVIRONMENT}/EPS_FHIR_SHA1_CLIENT_ID"
set_local_environment_secret EPS_FHIR_SHA1_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/EPS_FHIR_SHA1_CLIENT_SECRET"
set_local_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_ID "/regression-tests/${ENVIRONMENT}/EPS_FHIR_PRESCRIBING_CLIENT_ID"
set_local_environment_secret EPS_FHIR_PRESCRIBING_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/EPS_FHIR_PRESCRIBING_CLIENT_SECRET"
set_local_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID "/regression-tests/${ENVIRONMENT}/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID"
set_local_environment_secret EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET"
set_local_environment_secret EPS_FHIR_DISPENSING_CLIENT_ID "/regression-tests/${ENVIRONMENT}/EPS_FHIR_DISPENSING_CLIENT_ID"
set_local_environment_secret EPS_FHIR_DISPENSING_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/EPS_FHIR_DISPENSING_CLIENT_SECRET"
set_local_environment_secret EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY "/regression-tests/${ENVIRONMENT}/EPS_FHIR_DISPENSING_JWT_PRIVATE_KEY"
set_local_environment_secret EPS_FHIR_DISPENSING_JWT_KID "/regression-tests/${ENVIRONMENT}/EPS_FHIR_DISPENSING_JWT_KID"
set_local_environment_secret PFP_CLIENT_ID "/regression-tests/${ENVIRONMENT}/PFP_CLIENT_ID"
set_local_environment_secret PFP_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/PFP_CLIENT_SECRET"
set_local_environment_secret PSU_CLIENT_ID "/regression-tests/${ENVIRONMENT}/PSU_CLIENT_ID"
set_local_environment_secret PSU_CLIENT_SECRET "/regression-tests/${ENVIRONMENT}/PSU_CLIENT_SECRET"
set_local_environment_secret JWT_KID "/regression-tests/${ENVIRONMENT}/JWT_KID"
set_local_environment_secret JWT_PRIVATE_KEY "/regression-tests/${ENVIRONMENT}/JWT_PRIVATE_KEY"
