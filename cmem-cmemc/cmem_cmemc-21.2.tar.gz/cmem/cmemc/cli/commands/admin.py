"""admin commands for cmem command line interface."""

import click

from cmem.cmempy.api import (
    get_access_token,
    get_token
)
from cmem.cmempy.dp.admin import (
    create_showcase_data,
    import_bootstrap_data
)
from cmem.cmempy.config import (
    get_cmem_base_uri
)
from cmem.cmempy.health import (
    di_is_healthy,
    dp_is_healthy,
    get_di_version,
    get_dp_version
)
from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup
from cmem.cmemc.cli.commands.workspace import workspace


@click.command(cls=CmemcCommand, name="bootstrap")
@click.option(
    "--import", "import_",
    is_flag=True,
    help="Delete existing bootstrap data if present and import bootstrap "
         "data which was delivered "
)
@click.pass_obj
def bootstrap_command(app, import_):
    """Update/Import bootstrap data.

    This command imports the bootstrap data needed for managing shapes,
    access conditions, the query catalog and the vocabulary catalog.

    Note: There is currently no deletion mechanism for the bootstrap data,
    so you need to remove the graphs manually (or just remove all graphs).
    """
    if not import_:
        raise ValueError("Use the --import flag to update/import "
                         "bootstrap data.")
    import_bootstrap_data()
    app.echo_success("Bootstrap data updated.")


@click.command(cls=CmemcCommand, name="showcase")
@click.option(
    "--scale",
    type=click.INT,
    default="10",
    show_default=True,
    help="The scale factor provides a way to set the target size of the "
         "scenario. A value of 10 results in around 40k triples, a value of "
         "50 in around 350k triples."
)
@click.option(
    "--create",
    is_flag=True,
    help="Delete old showcase data if present and create new showcase data"
         "based on the given scale factor."
)
@click.option(
    "--delete",
    is_flag=True,
    help="Delete existing showcase data if present."
)
@click.pass_obj
def showcase_command(app, scale, create, delete):
    """Create showcase data.

    This command creates a showcase scenario of multiple graphs including
    integration graphs, shapes, statement annotations etc.

    Note: There is currently no deletion mechanism for the showcase data, so
    you need to remove the showcase graphs manually (or just remove all
    graphs).
    """
    if not delete and not create:
        raise ValueError("Either use the --create or the --delete flag.")
    if delete:
        raise NotImplementedError(
            "This feature is not implemented yet. "
            "Please delete the graphs manually."
        )
    if create:
        create_showcase_data(scale_factor=scale)
        app.echo_success(
            "Showcase data with scale factor {} created."
            .format(scale)
        )


@click.command(cls=CmemcCommand, name="status")
@click.pass_obj
def status_command(app):
    """Output health and version information.

    This command outputs version and health information of the
    selected deployment. In addition to that, this command warns you if the
    target version of your cmemc client is newer than the version of your
    backend.

    To get status information of all configured
    deployments use this command in combination with xargs:

    cmemc config list | xargs -i cmemc -c {} admin status
    """
    app.check_versions()
    app.echo_result(get_cmem_base_uri())
    # check DP
    app.echo_result("- DataPlatform ", nl=False)
    if dp_is_healthy():
        app.echo_result(get_dp_version() + " ... ", nl=False)
        app.echo_success("UP")
    else:
        app.echo_result(get_dp_version() + " ... ", nl=False)
        app.echo_error("DOWN")
    # check DI
    app.echo_result("- DataIntegration ", nl=False)
    if di_is_healthy():
        app.echo_result(get_di_version() + " ... ", nl=False)
        app.echo_success("UP")
    else:
        app.echo_result(get_di_version() + " ... ", nl=False)
        app.echo_error("DOWN")


@click.command(cls=CmemcCommand, name="token")
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON. Note that this option will always try to fetch "
         "a new JSON token response. In case you are working with "
         "OAUTH_GRANT_TYPE=prefetched_token, this may lead to an error."
)
@click.pass_obj
def token_command(app, raw):
    """Fetch and output an access token.

    This command can be used to check for correct authentication as well as to
    use the token with wget / curl or similar standard tools:

    curl -H "Authorization: Bearer $(cmemc admin token)"
    https://your-cmem/dataplatform/api/custom/slug
    """
    if raw:
        app.echo_info_json(get_token())
        return
    app.echo_info(get_access_token())


@click.group(cls=CmemcGroup)
def admin():
    """Import bootstrap data and create showcase data.

    This command group consists of commands for setting up and
    configuring eccenca Corporate Memory.
    """


admin.add_command(showcase_command)
admin.add_command(bootstrap_command)
admin.add_command(status_command)
admin.add_command(token_command)
admin.add_command(workspace)
