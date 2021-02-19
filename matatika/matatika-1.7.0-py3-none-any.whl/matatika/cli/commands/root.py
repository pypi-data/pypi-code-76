"""CLI entrypoint 'matatika' command"""

from textwrap import dedent
import click
import pkg_resources
import requests
from matatika.exceptions import MatatikaException

version = pkg_resources.require("matatika")[0].version


class ExceptionHandler(click.Group):
    """CLI entrypoint and error handling"""

    def invoke(self, ctx):
        """Invoke method override"""

        try:
            return super().invoke(ctx)

        except MatatikaException as err:
            click.secho(str(err), fg='red')

        except requests.exceptions.HTTPError as err:

            msg = dedent(f"""\
                {repr(err)}
                
                Possible causes:
                \t- the authentication token may not be in the correct format (check it was copied correctly)
                \t- the authentication token may not be valid for the specified endpoint url
                \t- the authentication token may have expired
                """)

            click.secho(msg, fg='red')


@click.group(cls=ExceptionHandler)
@click.pass_context
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.option("--trace", "-t", is_flag=True, help="Trace variable sources")
@click.version_option(version=version)
def matatika(ctx, auth_token, endpoint_url, trace):
    """CLI entrypoint and base command"""

    ctx.ensure_object(dict)

    ctx.obj['auth_token'] = auth_token
    ctx.obj['endpoint_url'] = endpoint_url
    ctx.obj['trace'] = trace
