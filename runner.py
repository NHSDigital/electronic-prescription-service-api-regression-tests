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
        "--product",
        required=True,
        help="The product under test",
    )
    parser.add_argument(
        "--tags",
        required=False,
        help="Tags to include or exclude. use ~tag_name to exclude tags",
    )
    argument = parser.parse_args()

    # Convert to behave commandline args
    product_tag = argument.product.lower().replace("-", "_")
    if argument.tags:
        tags = f" --tags {product_tag} --tags {argument.tags} "
    else:
        tags = f" --tags {product_tag}"
    PRODUCT = f" -D product={argument.product}"
    ENV = f" -D env={argument.env}"

    # complete command
    command = (
        f"behave{PRODUCT}{ENV}"
        f" -f behave_cucumber_formatter:PrettyCucumberJSONFormatter"
        f" -o reports/cucumber_json.json"
        f" -f allure_behave.formatter:AllureFormatter"
        f" -o allure-results"
        f" -f pretty features"
        f" --no-logcapture --no-skipped --expand --logging-level=DEBUG '{tags}'"
    )
    print(f"Running subprocess with command: '{command}'")
    subprocess.run(command, shell=True, check=True)
