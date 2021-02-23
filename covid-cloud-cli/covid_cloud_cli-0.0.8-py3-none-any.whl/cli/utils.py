import sys
import click


def assert_config(ctx, var_name):
    if var_name not in ctx.obj.keys() or not ctx.obj[var_name]:
        click.secho(
            F"The {var_name} configuration variable is not set. Run covid-cloud config {var_name} [URL] to configure it",
            fg='red')
        sys.exit()
