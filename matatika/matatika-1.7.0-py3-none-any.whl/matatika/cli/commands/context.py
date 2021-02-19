"""CLI 'context' command and subcommands"""

# external
import click
# local
from matatika.cli.utility import create_table
from matatika.context import MatatikaContext
from matatika.exceptions import NoDefaultContextSetError
from .root import matatika


@matatika.group("context", short_help="Context operations")
def context():
    """Base context command"""


@context.command("list", short_help="List all configured contexts")
def list_():
    """Lists all configured contexts"""

    contexts = MatatikaContext().get_all_contexts()

    names = ["CONTEXT NAME"]
    auth_tokens = ["AUTH TOKEN"]
    endpoint_urls = ["ENDPOINT URL"]
    workspace_ids = ["WORKSPACE ID"]

    for name, variables in contexts.items():
        names.append(name)
        auth_tokens.append(variables['auth_token'])
        endpoint_urls.append(variables['endpoint_url'])
        workspace_ids.append(variables['workspace_id'])

    table = create_table(names, auth_tokens, endpoint_urls, workspace_ids)
    click.echo(table)


@context.command("create", short_help="Create a new context")
@click.argument("context-name")
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--endpoint-url", "-e", default='https://catalog.matatika.com/api',
              help="Endpoint URL")
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def create(context_name, auth_token, endpoint_url, workspace_id):
    """Creates a new context"""

    variables = {
        'auth_token': auth_token,
        'endpoint_url': endpoint_url,
        'workspace_id': str(workspace_id) if workspace_id else None
    }

    MatatikaContext().create_context(context_name, variables)


@context.command("delete", short_help="Delete a context")
@click.argument("context-name")
def delete(context_name):
    """Deletes an existing context"""

    try:
        default_context_name, _default_context_variables = MatatikaContext().get_default_context()

        if context_name == default_context_name:
            MatatikaContext().set_default_context(None)

    except NoDefaultContextSetError:
        pass

    finally:
        MatatikaContext().delete_context(context_name)


@context.command("use", short_help="Set a default context")
@click.argument("context-name")
def use(context_name):
    """Set a context to use by default"""

    MatatikaContext().set_default_context(context_name)


@context.command("info", short_help="Show the default context")
def info():
    """Shows the default context"""

    name, variables = MatatikaContext().get_default_context()

    var_labels = ["CONTEXT NAME", "AUTH TOKEN", "ENDPOINT URL", "WORKSPACE ID"]
    var_values = [name] + list(variables.values())
    table = create_table(var_labels, var_values, separator="\t-->\t")

    click.echo(table)


@context.command("update", short_help="Update the default context")
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def update(auth_token, endpoint_url, workspace_id):
    """Updates the default context"""

    variables = {}

    if auth_token:
        variables.update({'auth_token': auth_token})
    if endpoint_url:
        variables.update({'endpoint_url': endpoint_url})
    if workspace_id:
        variables.update({'workspace_id': str(workspace_id)})

    MatatikaContext().update_default_context_variables(variables)
