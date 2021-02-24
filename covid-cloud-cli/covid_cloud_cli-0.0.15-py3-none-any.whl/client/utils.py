import click
from requests.exceptions import SSLError
from search_python_client.search import SearchClient, DrsClient
from typing import Optional


def handle_client_results(results, search_url):
    try:
        yield from results
    except SSLError:
        click.secho(f"There was an error retrieving the SSL certificate from {search_url}", fg='red')
        return
    except:
        click.secho(f"There was an error querying from {search_url}", fg='red')
        return


def get_search_client(search_url, oauth_token: Optional[str] = None):
    # TODO get new token if expired
    if oauth_token:
        search_client = SearchClient(search_url, wallet=oauth_token)
    else:
        search_client = SearchClient(search_url)

    return search_client


def get_drs_client(drs_url, oauth_token: Optional[str] = None):
    # TODO get new token if expired
    if oauth_token:
        drs_client = DrsClient(drs_url, wallet=oauth_token)
    else:
        drs_client = DrsClient(drs_url)

    return drs_client
