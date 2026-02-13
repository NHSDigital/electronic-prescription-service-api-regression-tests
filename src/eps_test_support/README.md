# EPS Test Support

A Python package providing reusable test utilities for NHS Electronic Prescription Service (EPS) testing.

## Overview

This package contains shared test infrastructure used by the EPS regression test suite, including:

- **API Client Methods** - HTTP wrappers for EPS, PSU, CPTS, and PFP APIs
- **Page Object Models** - Playwright-based UI testing components for CPTS UI
- **FHIR Message Builders** - Template builders for prescription, dispense, cancel, and other FHIR resources
- **Test Utilities** - Prescription ID generators, NHS number generators, signing utilities

## Installation

### From GitHub Packages

Add the GitHub Packages repository to your Poetry configuration:

```bash
poetry config repositories.github-packages https://pypi.pkg.github.com/NHSDigital/electronic-prescription-service-api-regression-tests/simple
```

Authenticate with a GitHub Personal Access Token (PAT) with `read:packages` permission:

```bash
poetry config http-basic.github-packages <github-username> <github-pat>
```

Install the package:

```bash
poetry add eps-test-support --source github-packages
```

### From Source (Development)

Clone the repository and install in editable mode:

```bash
git clone https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests.git
cd electronic-prescription-service-api-regression-tests
poetry install
```

## Package Structure

```
eps_test_support/
├── api/                    # API client methods
│   ├── common_api_methods.py   # Generic HTTP GET/POST with logging
│   ├── eps_api_methods.py      # EPS FHIR API methods
│   ├── psu_api_methods.py      # Prescription Status Update API methods
│   ├── cpts_api_methods.py     # Clinical Practitioner Tracking Service API methods
│   └── pfp_api_methods.py      # Prescriptions for Patients API methods
│
├── pages/                  # Page Object Models for UI testing
│   ├── search_for_a_prescription.py
│   ├── prescription_details.py
│   ├── prescription_list_page.py
│   └── [20+ more page objects]
│
├── messages/               # FHIR message builders
│   ├── eps_fhir/              # EPS FHIR message templates
│   │   ├── prescription.py         # Prescription bundle builder
│   │   ├── dispense_notification.py  # Dispense notification builder
│   │   ├── cancel.py               # Cancellation builder
│   │   ├── prescription_return.py  # Return builder
│   │   └── signed_prescription.py  # Digital signature wrapper
│   └── psu/                   # PSU message templates
│       └── prescription_status_update.py
│
├── shared/                 # Shared utilities
│   └── common.py              # Authentication, assertions, AWS helpers
│
└── utils/                  # General utilities
    ├── prescription_id_generator.py  # Valid prescription ID generation
    ├── random_nhs_number_generator.py  # Valid NHS number generation
    └── signing.py                    # Digital signature utilities
```

## Usage Examples

### API Methods

```python
from eps_test_support.api.eps_api_methods import create_signed_prescription, dispense_prescription
from eps_test_support.shared.common import get_auth, assert_that

# Authenticate
auth_token = get_auth(env="int", app="EPS-FHIR")

# Create and send a prescription
response = create_signed_prescription(context)
assert_that(response.status_code).is_equal_to(201)

# Dispense the prescription
dispense_response = dispense_prescription(context)
assert_that(dispense_response.status_code).is_equal_to(200)
```

### FHIR Message Builders

```python
from eps_test_support.messages.eps_fhir.prescription import Prescription
from eps_test_support.utils.prescription_id_generator import generate_short_form_id
from eps_test_support.utils.random_nhs_number_generator import generate_single

# Generate test data
context.prescription_id = generate_short_form_id()
context.nhs_number = generate_single()

# Build prescription message
prescription = Prescription(context)
prescription_json = prescription.body
```

### Page Objects (Playwright)

```python
from eps_test_support.pages.search_for_a_prescription import SearchForAPrescription
from playwright.sync_api import sync_playwright

# Initialize page object
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    search_page = SearchForAPrescription(page)

    # Interact with page
    search_page.prescription_id_input.fill("ABC123")
    search_page.search_button.click()
```

### Utilities

```python
from eps_test_support.utils.prescription_id_generator import generate_short_form_id
from eps_test_support.utils.random_nhs_number_generator import generate_single

# Generate valid prescription ID with check digit
prescription_id = generate_short_form_id()  # e.g., "16B2E0-A83008-81D0F2"

# Generate valid NHS number
nhs_number = generate_single()  # e.g., "9990548609"
```

## API Reference

### Common API Methods (`eps_test_support.api.common_api_methods`)

- `get(context, **kwargs)` - HTTP GET with request/response logging to Allure
- `post(data, url, context, headers)` - HTTP POST with request/response logging to Allure
- `get_headers(context, auth_type)` - Build HTTP headers with authentication
- `request_ping(context)` - Health check endpoint
- `request_metadata(context)` - Metadata endpoint

### Shared Common (`eps_test_support.shared.common`)

- `get_auth(env, app)` - Get OAuth2 token for API authentication
- `assert_that(value)` - Fluent assertion wrapper (assertpy)
- `convert_to_uri(prescription_id)` - Convert prescription ID to URI format
- `the_expected_response_code_is_returned(context, expected_code)` - Assert response status code

### Message Builders

#### Prescription (`eps_test_support.messages.eps_fhir.prescription`)

```python
class Prescription:
    def __init__(self, context): ...
    body: str  # JSON string of FHIR Bundle
```

Required context attributes: `prescription_id`, `nhs_number`, `sender_ods_code`, etc.

#### Dispense Notification (`eps_test_support.messages.eps_fhir.dispense_notification`)

```python
class DispenseNotification:
    def __init__(self, context, props: DNProps): ...
    body: str  # JSON string of FHIR Bundle
```

#### Status Update (`eps_test_support.messages.psu.prescription_status_update`)

```python
class StatusUpdate:
    def __init__(self, context): ...
    body: str  # JSON string of status update
```

## Dependencies

Key dependencies included in the package:

- `requests` - HTTP client
- `assertpy` - Fluent assertions
- `playwright` - Browser automation
- `allure-behave` - Test reporting (for attachment helpers)
- `boto3` - AWS SDK (for AWS helpers in shared.common)
- `cryptography` - Digital signatures
- `jsonschema` - JSON validation

## Version

Current version: **0.1.0**

## License

See LICENSE file in the repository root.

## Contributing

This package is part of the [electronic-prescription-service-api-regression-tests](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests) repository. See CONTRIBUTING.md for guidelines.

## Support

For issues or questions, open an issue in the GitHub repository.
