from .constants import *
from datetime import datetime
from requests.exceptions import SSLError
import click
import json
from requests import HTTPError
from search_python_client.search import SearchClient
from covid_cloud.client.utils import handle_client_results


def query(search_url, q, download=False, use_json=False, raw=False):
    search_client = SearchClient(search_url)
    results = search_client.search_table(q)

    if use_json or not raw:
        output = json.dumps(list(handle_client_results(results, search_url)), indent=4)
    else:
        outputs = []
        for res in handle_client_results(results, search_url):
            data_row = map(str, res.values())
            outputs.append(",".join(data_row))
        output = "\n".join(outputs)

    if download:
        # TODO: be able to specify output file
        download_file = f"{downloads_directory}/query{str(datetime.now())}{'.json' if use_json or not raw else '.csv'}"
        with open(download_file, "w") as fs:
            fs.write(output)
    else:
        return output


def get_tables(search_url):
    search_client = SearchClient(search_url)
    tables_iterator = search_client.get_table_list()

    return json.dumps(list(handle_client_results(tables_iterator, search_url)), indent=4)


def get_table(search_url, table_name):
    search_client = SearchClient(search_url)

    try:
        table_info = search_client.get_table_info(table_name)
    except SSLError:
        click.secho(f"Unable to retrieve SSL certificate from {search_url}", fg='red')
        return
    except HTTPError as error:
        if '404' in str(error.response):
            click.secho('Invalid table name. ', fg='red')
        else:
            click.echo(error.response)
        return

    # formatting response to remove unnecessary fields
    results = table_info.to_dict()
    results["name"] = table_info["name"]["$id"]
    results["description"] = table_info["description"]["$id"]

    return json.dumps(results, indent=4)
