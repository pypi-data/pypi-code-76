import geodesic.oauth as oauth
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "command", type=str, choices=["authenticate"], help="which command to run"
)


def main():
    args = parser.parse_args()

    if args.command == "authenticate":
        auth = oauth.AuthManager()
        auth.authenticate()


if __name__ == "__main__":
    main()
