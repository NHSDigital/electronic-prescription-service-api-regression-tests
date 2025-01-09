[![Regression Tests](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml/badge.svg?branch=main)](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml)

# Regression Tests
These tests will automate End-to-End regression testing for:
* [Electronic Prescription Service (EPS-FHIR)](https://digital.nhs.uk/developer/api-catalogue/electronic-prescription-service-fhir)
* [Prescriptions for Patients (PfP)](https://digital.nhs.uk/developer/api-catalogue/prescriptions-for-patients)
* [Prescription Status Update (PSU)](https://digital.nhs.uk/developer/api-catalogue/prescription-status-update-fhir/)
* [Clinical Prescription Tracker UI (CPT-UI)](https://github.com/NHSDigital/eps-prescription-tracker-ui)

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

The following environment variables need to be set for the correct environment you wish to test against:
* CLIENT_ID
* CLIENT_SECRET
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
#### Once ASDF is installed, add the following plugins:
* ASDF python plugin `asdf plugin add python`
* ASDF poetry plugin `asdf plugin add poetry`
* ASDF shellcheck plugin `asdf plugin add shellcheck`
* ASDF nodejs plugin `asdf plugin add nodejs`
#### Once the plugins are added you can install them
`asdf install` This will install the versions as described in .tool-versions

Now you can run `make install` to install the virtualenv and packages

## Developing/Debugging Tests

## Running the tests:
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

For example:
```
product=cpts-ui env=internal-dev PULL_REQUEST_ID=pr-300 tags=cpt-ui HEADLESS=true make run-tests
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
Run the tests by pushing changes to github in a pull request and running the regression tests job.
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

## Recording new tests:
Playwright contains a handy (but not perfect) feature which will record actions you make and give you the code for them
to begin, run the command: <br />
`playwright codegen`
