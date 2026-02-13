import argparse
from eps_test_support.shared.common import get_auth


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a CIS2 authentication token.")
    parser.add_argument(
        "--user",
        choices=["dispenser", "practitioner"],
        help="User (dispenser or practitioner)",
    )
    parser.add_argument(
        "--env",
        choices=[
            "INTERNAL-DEV-SANDBOX",
            "SANDBOX",
            "INT",
            "INTERNAL-QA",
            "INTERNAL-DEV",
            "REF",
        ],
        help="Env (INTERNAL-DEV-SANDBOX, SANDBOX, INT, INTERNAL-QA, INTERNAL-DEV, REF)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print(
        "This tool will allow you to generate a CIS2 authentication token. You can use this token to authenticate"
        " with APIs that support this service."
    )
    print("Please ensure the appropriate environment variables are set: CLIENT_ID, CLIENT_SECRET")

    if not args.user:
        args.user = input("User (dispenser or practitioner): ")

    if not args.env:
        args.env = input("Env (INTERNAL-DEV-SANDBOX, SANDBOX, INT, INTERNAL-QA, INTERNAL-DEV, REF): ")

    print(get_auth(env=args.env.upper(), product="EPS-FHIR", user=args.user.lower()))
