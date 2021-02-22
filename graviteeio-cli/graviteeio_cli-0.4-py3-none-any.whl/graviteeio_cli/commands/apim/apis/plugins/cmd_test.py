import click
import requests
import webbrowser


@click.command()
@click.pass_context
def test(ctx):

    webbrowser.open('www.google.com')
