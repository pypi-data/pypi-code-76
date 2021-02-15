
import click
from cli.utils import ConfigurationManager

confManager = ConfigurationManager()


@click.command()
def config():
    """Configure Gandalf for local use."""
    dict_file = dict()
    credentials = dict()
    confluence_config = dict()
    confluence_parentpages = dict()

    dict_file["product-name"] = click.prompt(
        "Please enter the name of the product", type=str)

    dict_file["project-key"] = click.prompt(
        "Please enter the project key on Jira", type=str)

    dict_file["bitbucket-url"] = click.prompt(
        "Please enter the url for Bitbucket", type=str)

    dict_file["jira-url"] = click.prompt(
        "Please enter the url for Jira", type=str)

    dict_file["confluence-url"] = click.prompt(
        "Please enter the url for Confluence", type=str)
    confluence_config["spacekey"] = click.prompt(
        "Please enter the space-key for your project's Confluence space", type=str)

    confluence_parentpages["releasenote"] = click.prompt(
        "Please enter the id for the release note parent page", type=str)

    confluence_parentpages["changelog"] = click.prompt(
        "Please enter the id for the changelog parent page", type=str)

    confluence_config["parent-page-ids"] = confluence_parentpages

    dict_file["confluence"] = confluence_config

    credentials["username"] = click.prompt(
        "Atlassian username", type=str)

    credentials["password"] = click.prompt(
        "Atlassian password", type=str)

    dict_file["credentials"] = credentials

    confManager.create_config(dict_file)
