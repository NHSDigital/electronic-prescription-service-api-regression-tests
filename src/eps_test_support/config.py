"""
Configuration and constants for EPS Test Support package.

This module contains shared constants used by the test utilities,
including API credentials, user IDs, and environment-specific settings.
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

# API Application Credentials
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

# CIS2 Test User Credentials
CIS2_USERS = {
    "prescriber": {"user_id": "656005750107", "role_id": "555254242105"},
    "dispenser": {"user_id": "555260695103", "role_id": "555265434108"},
}

# AWS Role Configurations
AWS_ROLES = {
    "eps-assist-me": {"role_id": os.getenv("EPS_ASSIST_ME_ROLE_ARN")},
}

# Digital Signature Keys
CERTIFICATE = os.getenv("CERTIFICATE")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# JWT Configuration
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_KID = os.getenv("JWT_KID")

# Login User Configuration
LOGIN_USERS = {"user_id": "9449304130"}
