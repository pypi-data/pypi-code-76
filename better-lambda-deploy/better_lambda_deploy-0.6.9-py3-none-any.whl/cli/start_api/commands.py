from ...deployer import Deployer
import click


@click.command()
@click.option("--name", default="local", help="The name of the project to run.")
@click.option("--dir", default="./", help="The directory to deploy as a BLD project.")
@click.option(
    "--local", is_flag=True, default=True, help="Build locally instead of using SAM."
)
def start_api(name, dir, local):
    deployer = Deployer(name, dir, local=local)
    deployer.start_api()
