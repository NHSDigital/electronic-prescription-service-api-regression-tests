[![Regression Tests](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml/badge.svg?branch=main)](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml)

# Regression Tests
These tests will automate regression testing of the Electronic Prescription Service API
<br /> Any test failures will result in a failed build being reported (When run in CI)

## General usage
These tests are run automatically during deployment and shouldn't need to be touched unless performing debugging or
adding/removing/changing the test cases

## Preparing your development environment
This test pack utilises the power of Docker to fast and easily spin up a dev environment for you to work in
the Dockerfile is located in `{project_root}/.devcontainer/Dockerfile`

## Setup without docker development environment
If you'd like to use your own machine without containerisation. You will need the following;
* Ubuntu (WSL)
* [ASDF](https://asdf-vm.com/guide/getting-started.html)
#### Once ASDF is installed, add the following plugins:
* ASDF python plugin `asdf plugin add python`
* ASDF poetry plugin `asdf plugin add poetry`
* ASDF shellcheck plugin `asdf plugin add shellcheck`
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
<h4> You MUST specify the environment and product
#### Example: `python runner.py  --product=EPS-FHIR --env=INT --tags smoke --tags ~slow`
This will run all tests with the tag `@smoke` but skip any tests tagged with `@slow`

### Method 2:
If your IDE supports it, you can directly run the .feature files within `/features`
<br />
* Note in some IDEs, you will need to set the `BASE_URL` environment within the behave run configuration rather than the machine.

### Method 3:
Run the tests by running `behave` in a command prompt or terminal window.
* This will run the tests and print the results to console

```
behave -D product=EPS-FHIR -D env=INT -f behave_cucumber_formatter:PrettyCucumberJSONFormatter -o reports/cucumber_json.json -f
allure_behave.formatter:AllureFormatter -o allure-results -f pretty features --no-capture --no-capture-stderr --no-skipped --expand --logging-level=DEBUG --tags eps_fhir
```

change the `env` variable accordingly to either `INT` or `INTERNAL-DEV`.
If you wish to test a different product i.e. `PFP-APIGREE` then you must change `product=` and `--tags` respectively.

### Setting the BASE_URL
The BASE_URL is set based on the environment you provide in the above command. This cannot be overridden


### Environment Variables
It is necessary to set some Environment variables in order to run any tests in your local environment. The tests will look for environment variables in the following order:
(For security, the values will not be displayed here)
1. `.env` file
2. OS environment variable
use the `template.env` file located on the root to see which variables need to be set
<p> Any file that beings with `.env` is automatically ignored by Git </p>

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
1. Before committing run `make pre-commit`. <br>
Note: This process will stop after the first program detects an error or if Black modified any files. You may need to run this multiple times to ensure everything is ok before committing.


### APIs tested and their Documentation
* [EPS-FHIR](https://digital.nhs.uk/developer/api-catalogue/electronic-prescription-service-fhir)
* [Prescriptions for Patients (PfP)](https://digital.nhs.uk/developer/api-catalogue/prescriptions-for-patients)
