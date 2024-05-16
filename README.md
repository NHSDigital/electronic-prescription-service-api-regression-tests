[![Regression Tests](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml/badge.svg?branch=main)](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml)

# Regression Tests
These tests will automate regression testing of the Electronic Prescription Service API
<br /> Any test failures will result in a failed build being reported (When run in CI)

## General usage
These tests are run automatically during deployment and shouldn't need to be touched unless performing debugging or
adding/removing/changing the test cases

## Preparing your development environment
This test pack utilizes the power of Docker to fast and easily spin up a dev environment for you to work in
the Dockerfile is located in `{project_root}/.devcontainer/Dockerfile`

## Setup without docker development environment
If you'd like to use your own machine without containerization. You will need the following;
* Ubuntu (WSL)
* [ASDF](https://asdf-vm.com/guide/getting-started.html)
#### Once ASDF is installed, add the following plugins:
* ASDF python plugin `asdf plugin add python`
* ASDF poetry plugin `asdf plugin add poetry`
* ASDF shellcheck plugin `asdf plugin add shellcheck`
#### Once the plugins are added you can install them
`asdf install` This will install the versions as described in .tool-versions

Now you can run `make install` to install the virtualenv and packages

## Obtaining certificates and env files
TBA

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


### Getting the token to check the endpoint calls on Postman

Depending on which environment you have run your *behave* command you can pick from the following:

- INTERNAL-DEV: Run `poetry run python get_token.py INTERNAL-DEV` to get the Authorization token for the internal-dev environment.
- INT: Run `poetry run python get_token.py INT` to get the Authorization token for the int environment.

### Commit to Git
1. Before committing run `make pre-commit`. <br>
Note: This process will stop after the first program detects an error or if Black modified any files. You may need to run this multiple times to ensure everything is ok before committing.


### APIs tested and their Documentation
* [EPS-FHIR](https://digital.nhs.uk/developer/api-catalogue/electronic-prescription-service-fhir)
* [Prescriptions for Patients (PfP)](https://digital.nhs.uk/developer/api-catalogue/prescriptions-for-patients)
