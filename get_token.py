from methods.shared.common import get_auth

if __name__ == "__main__":
    print(
        "This tool will allow you to generate a CIS2 authentication token. You can use this token to authenticate"
        " with APIs that support this service."
    )
    print(
        "Please ensure the appropriate environment variables are set: CLIENT_ID, CLIENT_SECRET"
    )
    user = input("User (dispenser or practitioner): ").lower()
    env = input(
        "Env (INTERNAL-DEV-SANDBOX, SANDBOX, INT, INTERNAL-QA, INTERNAL-DEV, REF): "
    ).upper()
    print(get_auth(user=user, env=env))
