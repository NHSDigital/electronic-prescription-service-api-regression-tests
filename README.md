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
#### Example: `python runner.py --tags smoke --tags ~slow`
This will run all tests with the tag `@smoke` but skip any tests tagged with `@slow`

### Method 2:
If your IDE supports it, you can directly run the .feature files within `/features`
<br />
* Note in some IDEs, you will need to set the `BASE_URL` environment within the behave run configuration rather than the machine

### Method 3:
Run the tests by running `behave` in a command prompt or terminal window.
* This will run the tests and print the results to console

```
behave -D product=EPS-FHIR -D env=INT -f behave_cucumber_formatter:PrettyCucumberJSONFormatter -o reports/cucumber_json.json -f 
allure_behave.formatter:AllureFormatter -o allure-results -f pretty features --no-capture --no-capture-stderr --no-skipped --expand --logging-level=DEBUG --tags eps_fhir
```

change the `env` variable accordingly to either `INT` or `INTERNAL-DEV`

### Setting the BASE_URL
To run the tests from your IDE it is necessary to set the BASE_URL environment variable.
<br /> If running via GitHub actions this will default to `INT` and currently cannot be changed


### Getting the token to check the endpoint calls on Postman

Depending on which environment you have run your *behave* command you can pick from the following:

- INTERNAL-DEV: Call `https://sxhjsbv4d7tvmt67av3jlboera0yzvgc.lambda-url.eu-west-2.on.aws/?env=internal-dev` which provides the Authorization token for the internal-dev environment.
- INT: Run `poetry run python get_token.py env=INT` to get the Authorization token for the int environment.

### Commit to Git
1. Before committing run `make pre-install`
2. You can run the commit command by adding `--no-verify` if you want to avoid word heavy messages that block the commit. Make sure you have resolved them before the end of the ticket. 


### Schema
The schema for the request bodies needed for eac endpoint call can be found here: https://digital.nhs.uk/developer/api-catalogue/electronic-prescription-service-fhir#post-/FHIR/R4/$prepare 
