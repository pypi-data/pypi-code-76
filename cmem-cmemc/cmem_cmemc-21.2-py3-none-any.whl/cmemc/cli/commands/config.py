"""configuration commands for cmem command line interface."""
import click

from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup


@click.command(cls=CmemcCommand, name="list")
@click.pass_obj
def list_command(app):
    """List configured connections.

    This command lists all configured
    connections from the currently used config file.

    The connection identifier can be used with the --connection option
    in order to use a specific Corporate Memory instance.

    In order to apply commands on more than one instance, you need to use
    typical unix gear such as xargs or parallel:

    cmemc config list | xargs -I % sh -c 'cmemc -c % admin status'

    cmemc config list | parallel --jobs 5 cmemc -c {} admin status
    """
    for section_string in sorted(app.config, key=str.casefold):
        if section_string != "DEFAULT":
            app.echo_result(section_string)


@click.command(cls=CmemcCommand, name="edit")
@click.pass_obj
def edit_command(app):
    """Edit the user-scope configuration file."""
    app.echo_info("Open editor for config file " + app.config_file)
    click.edit(filename=app.config_file)


@click.group(cls=CmemcGroup)
def config():
    u"""List and edit configurations.

    Configurations are identified by the section identifier in the
    config file. Each configuration represent a Corporate Memory deployment
    with its specific access method as well as credentials.

    A minimal configuration which uses client credentials has the following
    entries:

    \b
    [example.org]
    CMEM_BASE_URI=https://cmem.example.org/
    OAUTH_GRANT_TYPE=client_credentials
    OAUTH_CLIENT_ID=cmem-service-account
    OAUTH_CLIENT_SECRET=my-secret-account-pass

    Note that OAUTH_GRANT_TYPE can be either client_credentials, password or
    prefetched_token.

    In addition to that, the following config parameters can be used as well:

    \b
    SSL_VERIFY=False    - for ignoring certificate issues (not recommended)
    DP_API_ENDPOINT=URL - to point to a non-standard DataPlatform location
    DI_API_ENDPOINT=URL - to point to a non-standard DataIntegration location
    OAUTH_TOKEN_URI=URL - to point to an external IdentityProvider location
    OAUTH_USER=username - only if OAUTH_GRANT_TYPE=password
    OAUTH_PASSWORD=password - only if OAUTH_GRANT_TYPE=password
    OAUTH_ACCESS_TOKEN=token - only if OAUTH_GRANT_TYPE=prefetched_token

    In order to request passwords on start, you can use the following
    parameter instead the PASSWORD parameter: OAUTH_PASSWORD_ENTRY=True
    OAUTH_CLIENT_SECRET_ENTRY=True.
    """


config.add_command(list_command)
config.add_command(edit_command)
