from ...deployer import Deployer
import click


@click.command()
@click.option("--name", required=True, help="The name of the project to deploy.")
@click.option("--dir", default="./", help="The directory to deploy as a BLD project.")
@click.option(
    "--docker", is_flag=True, default=False, help="Run the SAM build in Docker."
)
@click.option(
    "--local", is_flag=True, default=False, help="Build locally instead of using SAM."
)
@click.option(
    "--environment",
    default="prod",
    help="The environment name to use for the deployment.",
)
@click.option("--subdomain", help="The subdomain to use for the deployed URL.")
@click.option("--domain", help="The domain to use for the deployed URL.")
@click.option("--pool-id", help="The Cognito user pool to use for the API layer.")
@click.option("--certificate-id", help="The ID of the certificate to use for HTTPS.")
def deploy(
    name, dir, docker, local, environment, subdomain, domain, pool_id, certificate_id
):
    deployer = Deployer(
        name,
        dir,
        docker=docker,
        local=local,
        environment=environment,
        subdomain=subdomain,
        domain=domain,
        pool_id=pool_id,
        certificate_id=certificate_id,
    )
    deployer.deploy()
