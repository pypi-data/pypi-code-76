import json
import logging
from os import environ
from urllib.parse import urlparse, urlunparse

import click
from pycognito import Cognito
from requests.auth import AuthBase

from .util import cached_request, get_nomitall_config
from .vars import CREDSTORE_PATH, DEFAULT_PROFILE

_logger = logging.getLogger(__name__)


def get_profiles():
    if CREDSTORE_PATH.exists() and CREDSTORE_PATH.is_file():
        with CREDSTORE_PATH.open() as f:
            return json.load(f)
    else:
        raise Exception(
            "No NND credentials found, please use `nnd login` or set environment variables"
        )


def login(username, password, user_pool_id, client_id):
    user = Cognito(
        user_pool_id,
        client_id,
        username=username,
        access_key="dummy_not_used",
        secret_key="dummy_not_used",
        user_pool_region="us-east-1",
    )
    try:
        user.authenticate(password=password)
    except user.client.exceptions.UserNotFoundException:
        raise click.ClickException(f"Nom Nom Data username not found {username}")
    except user.client.exceptions.NotAuthorizedException:
        raise click.ClickException(f"Authorization failed {username}")
    except user.client.exceptions.PasswordResetRequiredException:
        raise click.ClickException(f"Password reset required for {username}")
    return user


class _CognitoAuth(AuthBase):
    def __init__(self, profile=DEFAULT_PROFILE):
        self.profile = DEFAULT_PROFILE
        self.overrides = {}
        if environ.get("NND_USERNAME") and environ.get("NND_PASSWORD"):
            _logger.info("Found environment variables will use those instead")
        else:
            self.creds = get_profiles()

    def get_auth_creds(self, user_pool_id):
        return (
            self.creds[self.profile][user_pool_id]["id-token"],
            self.creds[self.profile][user_pool_id]["access-token"],
            self.creds[self.profile][user_pool_id]["refresh-token"],
        )

    def have_credentials(self, user_pool_id):
        try:
            self.creds[self.profile][user_pool_id]["id-token"]
            self.creds[self.profile][user_pool_id]["access-token"]
            self.creds[self.profile][user_pool_id]["refresh-token"]
            return True
        except KeyError:
            return False

    def __call__(self, request, client_id, user_pool_id):
        if environ.get("NND_USERNAME") and environ.get("NND_PASSWORD"):
            cognito = login(
                username=environ.get("NND_USERNAME"),
                password=environ.get("NND_PASSWORD"),
                user_pool_id=user_pool_id,
                client_id=client_id,
            )
        else:
            id_token, access_token, refresh_token = self.get_auth_creds(user_pool_id)
            cognito = Cognito(
                user_pool_id=user_pool_id,
                client_id=client_id,
                id_token=id_token,
                access_token=access_token,
                refresh_token=refresh_token,
                access_key="dummy_not_used",
                secret_key="dummy_not_used",
                user_pool_region="us-east-1",
            )
        if cognito.check_token():
            _logger.info("Tokens refreshed")
            self.creds[self.profile][user_pool_id]["access-token"] = cognito.access_token
            self.creds[self.profile][user_pool_id][
                "refresh-token"
            ] = cognito.refresh_token
            self.creds[self.profile][user_pool_id]["id-token"] = cognito.id_token
            with CREDSTORE_PATH.open("w") as f:
                json.dump(self.creds, f)
            CREDSTORE_PATH.chmod(0o600)

        request.headers["cognito-access-token"] = cognito.access_token
        request.headers["cognito-id-token"] = cognito.id_token
        return request


class NominodeAuth(_CognitoAuth):
    def __call__(self, request):
        parsed_url = urlparse(request.url)
        parsed_url = parsed_url._replace(path="api/v2/config", query="")
        resp = cached_request("GET", urlunparse(parsed_url))
        nominode_config = resp.json()
        config = get_nomitall_config(
            nominode_config.get("nomitall_api_url", "https://user.api.nomnomdata.com")
        )

        if (
            not environ.get("NND_USERNAME")
            and not environ.get("NND_PASSWORD")
            and not self.have_credentials(config["COGNITO_USERPOOL_ID"])
        ):
            raise click.ClickException(
                f'Could not find credentials for the nomitall {nominode_config["nomitall_api_url"]} which the nominode uses, please check {CREDSTORE_PATH} and/or `nnd login --nomitall-url {nominode_config["nomitall_api_url"]}`'
            )

        return super().__call__(
            request, config["COGNITO_CLIENT_ID"], config["COGNITO_USERPOOL_ID"]
        )


class NomitallAuth(_CognitoAuth):
    def __call__(self, request):
        config = get_nomitall_config(request.url)
        if (
            not environ.get("NND_USERNAME")
            and not environ.get("NND_PASSWORD")
            and not self.have_credentials(config["COGNITO_USERPOOL_ID"])
        ):
            parsed_url = urlparse(request.url)
            raise click.ClickException(
                f"Could not find credentials for {parsed_url.netloc}, please check {CREDSTORE_PATH} and/or run nnd login --nomitall-url {urlunparse(parsed_url)}"
            )
        return super().__call__(
            request, config["COGNITO_CLIENT_ID"], config["COGNITO_USERPOOL_ID"]
        )


# alias
NNDAuth = NomitallAuth
