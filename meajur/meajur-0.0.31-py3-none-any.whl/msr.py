import click
import requests

__author__ = "Athmane Bouazzouni"

@click.group()
def main():
    """
    Simple CLI by Athmane Bouazzouni
    """
    pass

@main.command()
@click.argument('query')
def search(query):
    """This search and return results corresponding to the given query from Google Books"""
    url_format = 'https://www.googleapis.com/books/v1/volumes'
    query = "+".join(query.split())

    query_params = {
        'q': query
    }

    response = requests.get(url_format, params=query_params)

    click.echo(response.json()['items'])

@main.command()
@click.argument('id')
def get(id):
    """This return a particular book from the given id on Google Books"""
    url_format = 'https://www.googleapis.com/books/v1/volumes/{}'
    #click.echo(id)

    response = requests.get(url_format.format(id))

    click.echo(response.json())


if __name__ == "__main__":
    main()