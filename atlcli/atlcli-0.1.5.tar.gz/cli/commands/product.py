import click
import pprint36 as pprint
from cli.services import JiraService
from cli.utils import ConfigurationManager

skipssl = False


@click.group()
@click.pass_context
def product(ctx):
    """Get information about a product"""
    confManager = ConfigurationManager()

    conf = confManager.load_config()
    context_parent = click.get_current_context(silent=True)
    ctx.ensure_object(dict)

    ctx.obj['skipssl'] = context_parent.obj["skipssl"]

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

    pass


@product.command()
def list():
    """Lists all the deployed versions of a product"""
    print("lists products")


@product.command()
@click.pass_context
def info():
    """Provides info about a product release"""
    pass


@product.command()
@click.pass_context
def versions(ctx):
    """Lists all the deployed versions of a product"""

    print("lists product versions")
    # print(productName)
    context_parent = click.get_current_context()


@product.command()
@click.pass_context
@click.option('-v', '--product-version', required=True, default=False)
@click.option('-j', '--project-key', required=True, default=False)
@click.option('--changes/--no-changes', required=False, default=False)
@click.option('--confluence/--no-confluence', required=False, default=False)
def tickets(ctx, product_version, project_key, changes, confluence):
    """Lists all components of a product"""
    jiraService = JiraService(
        ctx.obj['jira_url'], ctx.obj['username'], ctx.obj['password'], ctx.obj['skipssl'])

    product_version = product_version.strip()
    versionInfo = jiraService.get_project_version_infos(project_key,
                                                        product_version)

    if confluence:
        confMarkup = jiraService.get_issues_confluence_markup(project_key,
                                                              versionInfo["id"])
        print(confMarkup)
    else:
        output = "\nId: {0}\nName: {1}\nDescription: {2}\nReleased: {3}\nStart date: {4}\nRelease date: {5}\n"

        if versionInfo is not None:
            print("test")
            print(output.format(
                versionInfo["id"],
                versionInfo["name"],
                versionInfo["description"],
                versionInfo["released"],
                versionInfo["startDate"],
                versionInfo["releaseDate"]))

        if changes:
            output = jiraService.get_issues_printable(versionInfo["id"])
            print(output)


@product.command()
@click.pass_context
def info(ctx):
    """Displays info about a product"""

    print("product info here")
