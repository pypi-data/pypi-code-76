import click
from sym.cli.errors import CliError, CliErrorWithHint


class LoginError(CliError):
    def __init__(self, response_body) -> None:
        super().__init__(f"Error logging in: {response_body}")


class UnknownOrgError(CliError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Unknown organization for email: {email}")


class InvalidTokenError(CliError):
    def __init__(self, raw_token) -> None:
        super().__init__(f"Unable to parse token: {raw_token}")


class NotAuthorizedError(CliError):
    def __init__(self) -> None:
        super().__init__(f"Please run `symflow login`")


class SymAPIRequestError(CliErrorWithHint):
    def __init__(self, message: str, request_id: str) -> None:
        super().__init__(
            f"An API error occurred!",
            message
            + click.style(
                f"\n\nPlease contact support and include your Request ID ({request_id}).\nhttps://docs.symops.com/docs/support",
                fg="white",
                bold=True,
            ),
        )


class SymAPIMissingEntityError(SymAPIRequestError):
    error_codes = [404]

    def __init__(self, response_code: int, request_id: str) -> None:
        super().__init__(f"Missing entity ({response_code}).", request_id)


class SymAPIUnknownError(SymAPIRequestError):
    def __init__(self, response_code: int, request_id: str) -> None:
        super().__init__(
            f"An unknown error with status code {response_code}.", request_id
        )
