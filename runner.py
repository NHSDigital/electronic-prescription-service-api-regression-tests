import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # commandline arguments
    parser.add_argument(
        "--tags",
        required=False,
        help="Tags to include or exclude. use ~tag_name to exclude tags",
    )
    parser.add_argument(
        "--debug",
        required=False,
        action="store_true",
        help="Run in debug mode. The browser will not be headless and logging will be set to DEBUG",
    )
    argument = parser.parse_args()

    # Convert to behave commandline args
    tags = f" --tags {argument.tags} " if argument.tags else ""
    DEBUG = " -D debug=True" if argument.debug else " -D debug=False"
    LOGGING_LEVEL = "DEBUG" if argument.debug else "INFO"

    # complete command
    command = (
        f"behave{DEBUG}"
        f" -f behave_cucumber_formatter:PrettyCucumberJSONFormatter"
        f" -o reports/cucumber_json.json"
        f" -f allure_behave.formatter:AllureFormatter"
        f" -o not-allure-results"
        f" -f pretty features"
        f" --no-logcapture --logging-level={LOGGING_LEVEL}{tags}"
    )
    print(f"Running subprocess with command: '{command}'")
    subprocess.run(command, shell=True, check=True)
