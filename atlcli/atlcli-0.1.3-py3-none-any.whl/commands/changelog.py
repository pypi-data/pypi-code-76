import click
import json
from cli.services import ConfluenceService
from cli.services import BitbucketService
from cli.utils import ConfigurationManager

skipssl = False


@click.group()
@click.pass_context
def changelog(ctx):
    """Creates a changelog page on Confluence"""
    context_parent = click.get_current_context(silent=True)
    ctx.ensure_object(dict)
    confManager = ConfigurationManager()

    conf = confManager.load_config()

    if conf is None:
        ctx.obj['bitbucket_url'] = context_parent.obj["bitbucket_url"]
        ctx.obj['jira_url'] = context_parent.obj["jira_url"]
        ctx.obj['confluence_url'] = context_parent.obj["confluence_url"]
        ctx.obj['username'] = context_parent.obj["username"]
        ctx.obj['password'] = context_parent.obj["password"]
    else:
        ctx.obj['bitbucket_url'] = conf["bitbucket_url"]
        ctx.obj['jira_url'] = conf["jira_url"]
        ctx.obj['confluence_url'] = conf["confluence_url"]
        ctx.obj['username'] = conf["credentials"]["username"]
        ctx.obj['password'] = conf["credentials"]["password"]

    skipssl = context_parent.obj["skipssl"]
    pass


@changelog.command()
@click.pass_context
@click.option('-v', '--version', required=True, default="", help="Product version")
@click.option('-s', '--space-key', required=True, default="", help="Space key for the Confluence space")
@click.option('-n', '--product-name', required=True, default="", help="Product name")
@click.option('-f', '--configuration-repos', required=False, default="configuration", help="Name of the repos where the configurations are stored")
@click.option('-j', '--project-key', required=True, default="", help="Project key used in your Jira project")
@click.option('-i', '--parent-page-id', required=True, default="", help="Id of the page under which you will create your changelogs")
@click.option('-t', '--template-file', required=True, default="", help="Path to the template file for your changelog")
@click.option('--dry-run/--no-dry-run', required=False, default=False, help="Dry run for testing")
def generate_product(ctx, version, space_key, product_name,
                     configuration_repos, project_key, parent_page_id, template_file, dry_run):
    """Creates the changelog for a product on confluence"""

    version = version.strip()
    space_key = space_key.strip()
    product_name = product_name.strip()
    configuration_repos = configuration_repos.strip()
    project_key = project_key.strip()
    parent_page_id = parent_page_id.strip()
    template_file = template_file.strip()

    confluence_service = ConfluenceService(
        ctx.obj['confluence_url'], ctx.obj['jira_url'], ctx.obj['bitbucket_url'], ctx.obj['username'], ctx.obj['password'], ctx.obj['skipssl'])

    if not configuration_repos:
        configuration_repos = "configuration"

    if space_key is not None or parent_page_id is not None:
        if not dry_run:
            confluence_service.push_changelog(product_name,
                                              space_key, version, parent_page_id)
        else:
            print("This was a dry-run test")
    else:
        print("ERROR: Missing space-key or parent-page-id options.")


@changelog.command()
@click.pass_context
@click.option('-v', '--version', required=True, default="", help="Component/service version")
@click.option('-s', '--space-key', required=True, default="", help="Space key for the Confluence space")
@click.option('-n', '--component-name', required=True, default="", help="Component name")
@click.option('-i', '--parent-page-id', required=True, default="", help="Id of the page under which you will create your changelogs")
@click.option('-t', '--template-file', required=True, default="", help="Path to the template file for your changelog")
@click.option('--dry-run/--no-dry-run', required=False, default=False, help="Dry run for testing")
def generate_component(ctx, version, space_key, component_name, parent_page_id, template_file, dry_run):
    """Creates the changelog for a product on confluence"""
    version = version.strip()
    space_key = space_key.strip()
    component_name = component_name.strip()
    parent_page_id = parent_page_id.strip()
    template_file = template_file.strip()

    confluence_service = ConfluenceService(ctx.obj['skipssl'])

    if space_key is not None or parent_page_id is not None:
        if not dry_run:
            confluence_service.push_changelog(component_name,
                                              space_key, version, parent_page_id, True)
        else:
            print("This was a dry-run test")
    else:
        print("ERROR: Missing space-key or parent-page-id options.")
