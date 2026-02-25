import argparse
import os
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
        "--product",
        required=True,
        help="The product under test",
    )
    parser.add_argument(
        "--tags",
        action="append",  # allow multiple tags as behave does
        dest="tags",
        required=False,
        help="Tags to include or exclude. use ~tag_name to exclude tags",
    )
    parser.add_argument(
        "--arm64",
        required=False,
        type=str,
        help="Run tests using Chromium to support arm64 architecture",
    )
    argument = parser.parse_args()

    product_tag = argument.product.lower().replace("-", "_")
    tags = [tag.split(":") for tag in argument.tags] if argument.tags else []
    # Prepend product_tag to flattened list of tags
    tags = [product_tag] + [item for sublist in tags for item in sublist]

    PRODUCT = f" -D product={argument.product}"
    ENV = f" -D env={argument.env}"
    ARM64 = f" -D arm64={argument.arm64}"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # complete command
    command = (
        f"behave{PRODUCT}{ENV}{ARM64}"
        f" -f behave_cucumber_formatter:PrettyCucumberJSONFormatter"
        f" -o reports/cucumber_json.json"
        f" -f allure_behave.formatter:AllureFormatter"
        f" -o allure-results"
        f" -f pretty features"
        f" --no-logcapture"
        f" --no-skipped "
        f" --expand"
        f" --logging-level={LOG_LEVEL}"
        f" {" ".join(f"--tags {tag}" for tag in tags)}"
    )
    print(f"Running subprocess with command: '{command}'")
    subprocess.run(command, shell=True, check=True)
