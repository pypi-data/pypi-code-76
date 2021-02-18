from ...deployer import Deployer
import click


@click.command()
@click.argument("function")
@click.option("--dir", default="./", help="The directory to deploy as a BLD project.")
def invoke(function):
    deployer = Deployer(dir)
    deployer.invoke(function)
