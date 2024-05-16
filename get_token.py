import sys
from methods.shared.common import get_auth, get_auth_internal_dev


def get_token(environment):
    if environment == "INT":
        return get_auth("dispenser", environment)
    elif environment == "INTERNAL-DEV":
        return get_auth_internal_dev()
    else:
        raise ValueError("Invalid environment specified")


if __name__ == "__main__":
    environment = sys.argv[1]
    print(get_token(environment))
