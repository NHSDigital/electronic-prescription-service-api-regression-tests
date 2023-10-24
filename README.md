[![Regression Tests](https://github.com/NHSDigital/electronic-prescription-service-api-regression-tests/actions/workflows/regression_tests.yml/badge.svg?branch=main)](https://github.com/NHSDigital/direct-care-api-regression-tests/actions/workflows/regression_tests.yml)

# Regression Tests
These tests will automate regression testing of the Electronic Prescription Service API< /br>
Any test failures will result in a failed build being reported

## General usage
These tests are run automatically during deployment and shouldn't need to be touched unless performing debugging or
adding/removing/changing the test cases

## Preparing your development environment
This test pack utilises the power of Docker to fast and easily spin up a dev environment for you to work in with minimal set up (WIP)

## Developing/Debugging Tests

## Running the tests:
### Method 1 (Recommended):
Run the `runner.py` file located in the same folder as this read me. <br />
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

## Debug mode
##### This is intended for developers and testers who want to change the code or diagnose why tests are failing. You can run in debug mode in the following ways:
### Method 1:
via `runner.py` include `--debug` as a parameter.
#### Example: `python runner.py --tags critical --debug`
### Method 2:
via behave. Include `-D debug=True` as a parameter.
#### Example: `behave -D debug=True`
When running in debug mode, the logging level is set to DEBUG and will start printing debug messages to the console


### Setting the BASE_URL
To run the tests from your IDE it is necessary to set the BASE_URL environment variable. Follow the steps below to get the correct URL:
<br /> ((INPUT INFORMATION OF HOW TO GET URL HERE))
#### If you do not set the BASE_URL environment variable, these tests will refuse to run
