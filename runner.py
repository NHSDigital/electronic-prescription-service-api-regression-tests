import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # commandline arguments
    parser.add_argument(
        "--env",
        required=True,
        help="The environment the tests are going to run in.",
    )
    parser.add_argument(
        "--tags",
        required=False,
        help="Tags to include or exclude. use ~tag_name to exclude tags",
    )
    argument = parser.parse_args()

    # Convert to behave commandline args
    tags = f" --tags {argument.tags} " if argument.tags else ""
    ENV = f" -D env={argument.env}"
    LOGGING_LEVEL = "DEBUG"

    # complete command
    command = (
        f"behave{ENV}"
        f" -f behave_cucumber_formatter:PrettyCucumberJSONFormatter"
        f" -o reports/cucumber_json.json"
        f" -f allure_behave.formatter:AllureFormatter"
        f" -o allure-results"
        f" -f pretty features"
        f" --no-logcapture --logging-level={LOGGING_LEVEL}{tags}"
    )
    print(f"Running subprocess with command: '{command}'")
    subprocess.run(command, shell=True, check=True)
