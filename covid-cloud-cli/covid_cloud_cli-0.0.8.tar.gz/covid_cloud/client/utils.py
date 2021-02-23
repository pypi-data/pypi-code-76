import click
from requests.exceptions import SSLError


def handle_client_results(results, search_url):
    try:
        yield from results
    except SSLError:
        click.secho(f"There was an error retrieving the SSL certificate from {search_url}", fg='red')
        return
    except:
        click.secho(f"There was an error querying from {search_url}", fg='red')
        return
