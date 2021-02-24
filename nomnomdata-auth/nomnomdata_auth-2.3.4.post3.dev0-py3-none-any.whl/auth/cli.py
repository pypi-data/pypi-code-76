import json
from collections import defaultdict
from urllib.parse import urlparse

import click
import requests
from pycognito import Cognito

from .util import get_nomitall_config
from .vars import CREDSTORE_PATH, DEFAULT_PROFILE


class URL(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        if not isinstance(value, tuple):
            parsed = urlparse(value)
            parsed = parsed._replace(scheme="https")
            if not parsed.netloc:
                self.fail(
                    f"invalid URL {value}, must have a domain name",
                    param,
                    ctx,
                )
            return parsed


@click.group(
    name="login",
    help="Stores login credentials for use by the Nom Nom Data CLI",
    invoke_without_command=True,
)
@click.option(
    "--profile", envvar="NND_PROFILE", default=DEFAULT_PROFILE, show_default=True
)
@click.option(
    "--nomitall-url",
    envvar="NND_NOMITALL_URL",
    default="https://user.api.nomnomdata.com",
    show_default=True,
    type=URL(),
)
@click.option("--username", prompt="NND Username")
@click.option("--password", prompt=True, hide_input=True)
def login(profile, nomitall_url, username, password):
    if not CREDSTORE_PATH.exists():
        CREDSTORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        creds = defaultdict(dict)
    else:
        with CREDSTORE_PATH.open() as f:
            creds = defaultdict(dict, json.load(f))

    config = get_nomitall_config(nomitall_url.geturl())
    user = Cognito(
        config["COGNITO_USERPOOL_ID"],
        config["COGNITO_CLIENT_ID"],
        username=username,
        access_key="dummy_not_used",
        secret_key="dummy_not_used",
        user_pool_region="us-east-1",
    )
    try:
        user.authenticate(password=password)
    except (
        user.client.exceptions.UserNotFoundException,
        user.client.exceptions.NotAuthorizedException,
    ):
        raise click.ClickException(f"Incorrect username or password")
    except user.client.exceptions.PasswordResetRequiredException:
        raise click.ClickException(f"Password reset required for {username}, please")
    creds[profile][config["COGNITO_USERPOOL_ID"]] = {
        "access-token": user.access_token,
        "refresh-token": user.refresh_token,
        "id-token": user.id_token,
    }

    user_uuid = user.verify_token(user.id_token, "id_token", "id")["sub"]
    results = requests.get(
        f"{nomitall_url.geturl()}/api/1/user/{user_uuid}/organizations",
        headers={
            "cognito-access-token": user.access_token,
            "cognito-id-token": user.id_token,
        },
    )
    if results.status_code == 200:
        orgs = results.json()["results"]
        choice_dict = {i: org for i, org in enumerate(orgs)}
        click.secho("Available organizations:")
        for i, org in choice_dict.items():
            click.secho(f"{i}) {org['name']}")
        choices = click.Choice(choice_dict.keys())
        org_choice = click.prompt(
            "Choose default organization", value_proc=int, type=choices, default=0
        )
        creds[profile][config["COGNITO_USERPOOL_ID"]]["default-org"] = choice_dict[
            org_choice
        ]["uuid"]
        with CREDSTORE_PATH.open("w") as f:
            json.dump(creds, f, indent=4)
            CREDSTORE_PATH.chmod(0o600)
        click.secho(f"Logged in successfully, credentials stored @ {CREDSTORE_PATH}")

    else:
        raise click.Abort("Error fetching organizations for user")
