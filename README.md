[![Regression Tests](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml/badge.svg?branch=main)](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml)

# Regression Tests
These tests will automate End-to-End regression testing for:
* [Electronic Prescription Service (EPS-FHIR)](https://digital.nhs.uk/developer/api-catalogue/electronic-prescription-service-fhir)
* [Prescriptions for Patients (PfP)](https://digital.nhs.uk/developer/api-catalogue/prescriptions-for-patients)
* [Prescription Status Update (PSU)](https://digital.nhs.uk/developer/api-catalogue/prescription-status-update-fhir/)
* [Clinical Prescription Tracker UI (CPT-UI)](https://github.com/NHSDigital/eps-prescription-tracker-ui)
* [Clinical Prescription Tracker API (CPT-API)](https://github.com/NHSDigital/electronic-prescription-service-clinical-prescription-tracker)

Key contents of this repository:

* features  - Behave feature files and Python step implementation code
* src       - EPS test support library source files, see [Package Documentation](#eps-test-support-package) section below.

## General usage
These tests are run automatically during deployment and shouldn't need to be touched unless performing debugging or
adding/removing/changing test cases <br />
If there are any test failures, this will report a failed build

When developing new features that need to be regression tested, you'll need to create a new PR for them on this repository. When you are happy with the tests and the feature, merge the regression tests first. This will create a new tagged release, which you should then reference in the counterpart feature pull request before merging the code.

## Setup

### Environment Variables
It is necessary to set some Environment variables in order to run any tests in your local environment. The tests will look for environment variables in the following order
(For security, the values will not be displayed here):
1. `.env` file
2. OS environment variable

The following environment variables may need to be set for the correct environment you wish to test against:
* CPT_FHIR_CLIENT_ID
* CPT_FHIR_CLIENT_SECRET
* EPS_FHIR_CLIENT_ID
* EPS_FHIR_CLIENT_SECRET
* EPS_FHIR_SHA1_CLIENT_ID
* EPS_FHIR_SHA1_CLIENT_SECRET
* EPS_FHIR_PRESCRIBING_CLIENT_ID
* EPS_FHIR_PRESCRIBING_CLIENT_SECRET
* EPS_FHIR_PRESCRIBING_SHA1_CLIENT_ID
* EPS_FHIR_PRESCRIBING_SHA1_CLIENT_SECRET
* EPS_FHIR_DISPENSING_CLIENT_ID
* EPS_FHIR_DISPENSING_CLIENT_SECRET
* PFP_CLIENT_ID
* PFP_CLIENT_SECRET
* PSU_CLIENT_ID
* PSU_CLIENT_SECRET
* PRIVATE_KEY
* CERTIFICATE


To make this easier, a `template.env` file is located on the root. Fill in the values and rename this to `.env`

Any file that begins with `.env` is automatically ignored by Git

### Preparing your development environment
This test pack utilises the power of Docker to quickly and easily spin up a dev environment for you to work in
the Dockerfile is located in `{project_root}/.devcontainer/Dockerfile`

### Setup without docker development environment
If you'd like to use your own machine without containerisation. You will need the following;
* Ubuntu (WSL)
* [ASDF](https://asdf-vm.com/guide/getting-started.html)
* You can now run the `make install-full` command

Once this is completed, everything you need to get going should now be installed. </br>
You can now activate your virtual environment `source .venv/bin/activate`

## Developing/Debugging Tests

## Running the tests:
A note for Apple Silicon users, prior to running the tests locally you may find that Chrome doesn't offer an aarch64 or arm64 package.
You will need to use Chromium instead (similarly named, but the OSS version of Chrome).

```playwright install chromium```

To ensure the tests can continue to run in Chrome supported environments, an input toggle has been added that Apple users must use.

Pass the `arm64=true` argument when you attempt to run the tests.
ie.
```
product=cpts-ui env=internal-dev arm64=true PULL_REQUEST_ID=pr-300 tags=login HEADLESS=true make run-tests
```

### Method 1 (Recommended):
Run the `runner.py` file located in the root of the project <br />
This is the preferred method and allows you to include/exclude tags <br />
a `~` before the tag name excludes it. <br />
This is how the tests are run on the CI
<h4> You MUST specify the environment and product <br />

#### Example: `python runner.py --product=EPS-FHIR --env=INT --tags smoke --tags ~slow`
This will run all tests with the tag `@smoke` but skip any tests tagged with `@slow`

### Method 2:
If your IDE supports it, you can directly run the .feature files within `/features` <br />
Make sure that your behave run configuration includes the `--product=` & `--env=` <B>These are mandatory</B>

### Method 3:
Run the tests by calling the Make command `make run-tests`. This requires the parameters `product=` and `env=` to be passed in.
Optionally, you can pass in tags to be run, for example `tags=cpt-ui` will run all CPT-UI-tagged tests.
Further, if you want to actually see the tests being executed, you can pass a `HEADLESS=true` to the makefile.
If you want to throttle the speed that the tests are done, you can insert a delay between each action by passing the `SLOWMO=<delay, ms>` environment variable. This lets a human keep track of what steps are being done.

For example:
```
product=cpts-ui env=internal-dev PULL_REQUEST_ID=pr-300 tags=login HEADLESS=false SLOWMO=2000 make run-tests
```

Note that CPT-UI supports localhost testing. To do this, use the `env=localhost` variable - but ensure you have *not* set the `PULL_REQUEST_ID` variable, as it is not needed and will break the tests. Make sure your localhost server is running!

Playwright has a built-in inspector, that allows you to interact with and debug tests as they are running. This disables headless mode, and removes the limits on test timeouts, so you can play with failed cases. To enable this, add `PWDEBUG=1` to the `make run-tests` variables. For example:
```
product=cpts-ui env=localhost PWDEBUG=1 make run-tests
```

### Method 4 (Not Recommended):
Run the tests by running `behave` in a command prompt or terminal window.
* This will run the tests and print the results to console

Example:
```
behave -D product=EPS-FHIR -D env=INT -f behave_cucumber_formatter:PrettyCucumberJSONFormatter -o reports/cucumber_json.json -f
allure_behave.formatter:AllureFormatter -o allure-results -f pretty features --no-capture --no-capture-stderr --no-skipped --expand --logging-level=DEBUG --tags eps_fhir
```

Change the `env` variable accordingly to either `INT` or `INTERNAL-DEV`.
If you wish to test a different product i.e. `PFP-APIGEE` then you must change `product=` and `--tags` respectively.

### Method 5:
Run the tests by pushing changes to GitHub in a pull request and running the regression tests job.
You can do this by the browser or by running this
```
BRANCH=fix_tests_take_2
gh workflow run regression_tests.yml \
    --ref ${BRANCH} \
    -f tags=@regression \
    -f environment=INTERNAL-DEV \
    -f pull_request_id=pr-2877 \
    -f github_tag=${BRANCH}
```

### Getting the token to check the endpoint calls on Postman
On the root of the project is a file `get_token.py` <br>
This interactive Python script will assist you in generating a CIS2 authentication token that you can use elsewhere to make API calls (e.g. in Postman)
<br> **You will need a Client ID and Client Secret set as environment variables** </br>
Example:
```
This tool will allow you to generate a CIS2 authentication token. You can use this token to authenticate with APIs that support this service.
Please ensure the appropriate environment variables are set: CLIENT_ID, CLIENT_SECRET
User (dispenser or practitioner): dispenser
Env (INTERNAL-DEV-SANDBOX, SANDBOX, INT, INTERNAL-QA, INTERNAL-DEV, REF): int
Successfully Authenticated in INT
J6cdtaZa...
```
### Commit to Git
Pre commit hooks run checks on your code to ensure quality before being allowed to commit. You can perform this process by running: <br /> `make pre-commit`

This process will stop after the first program detects an error or if Black modified any files.
You may need to run this multiple times to ensure everything is ok before committing.


### Generating the allure report from a GitHub test run
To generate and view the results of a GitHub test run, first authenticate to GitHub by running this and following instructions
```
gh auth login
```
Then download the allure results by noting the GitHub run ID in a browser and running this
```
GITHUB_RUN_ID=11523235428 make download-allure-report
```

# UI testing
This pack has recently been updated to include UI-based testing using Playwright for CPTS-UI. It will run headless using the Chrome browser

## Setup
If you did not set up your environment using the `make install-full` command, then you may need to install playwright:
* Activate your virtual environment `source .venv/bin/activate` followed by `make install-playwright` to install the playwright tools.
* Check if these are installed properly, run `playwright codegen` a browser window will appear.

## Recording new tests:
Playwright contains a handy (but not perfect) feature which will record actions you make and give you the code for them
to begin, run the command: <br />
`playwright codegen`

## Building new tests:

### Fake Time / Mocked time
For tests making use of Playwright's clock functionality, you will need to provide the `@fake_time` tag on the scenario.
This tag is identified in the Behave before scenario function and will instatiate the Playwright clock mock.

### Concurrent sessions
For concurrent session testing, you'll need to make use of the Behave step "I switch the browser context to "{browser}" and login again".
This step has protection in place that the `@concurrency` tag is supplied on the scenario; this is to ensure the concurrent session Playwright trace is created, as it is disabled in `environment.py` otherwise.

### Uptime monitoring
During migrations it is useful to monitor responses from the API to quantify outages.
There is a wrapper script to do this reusing the functionality of the tests at `scripts/run_uptime_monitor.py`

---

## EPS Test Support Package

This repository also publishes the `eps-test-support` Python package to GitHub Packages, containing reusable test utilities for EPS testing.

### Package Contents

- **API Client Methods** - HTTP wrappers for EPS, PSU, CPTS, and PFP APIs
- **Page Object Models** - Playwright-based UI testing components
- **FHIR Message Builders** - Template builders for prescriptions, dispense notifications, cancellations, etc.
- **Test Utilities** - Prescription ID generators, NHS number generators, signing utilities

Full documentation: [src/eps_test_support/README.md](src/eps_test_support/README.md)

### Installation for Consumers

To use the `eps-test-support` package in your own test project:

#### 1. Configure Poetry to use GitHub Packages

```bash
poetry config repositories.github-packages https://pypi.pkg.github.com/NHSDigital/electronic-prescription-service-api-regression-tests/simple
```

#### 2. Authenticate with GitHub

Create a [Personal Access Token (PAT)](https://github.com/settings/tokens) with `read:packages` permission, then:

```bash
poetry config http-basic.github-packages <your-github-username> <your-github-pat>
```

#### 3. Add the package to your project

```bash
poetry add eps-test-support --source github-packages
```

Or add to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
eps-test-support = {version = "^0.1.0", source = "github-packages"}

[[tool.poetry.source]]
name = "github-packages"
url = "https://pypi.pkg.github.com/NHSDigital/electronic-prescription-service-api-regression-tests/simple"
priority = "supplemental"
```

### Usage Example

```python
from eps_test_support.api.eps_api_methods import create_signed_prescription
from eps_test_support.messages.eps_fhir.prescription import Prescription
from eps_test_support.shared.common import get_auth, assert_that

# Authenticate
auth_token = get_auth(env="int", app="EPS-FHIR")

# Build and send prescription
prescription = Prescription(context)
response = create_signed_prescription(context)
assert_that(response.status_code).is_equal_to(201)
```
