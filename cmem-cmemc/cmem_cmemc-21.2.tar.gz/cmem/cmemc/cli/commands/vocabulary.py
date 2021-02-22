"""vocabularies commands for cmem command line interface."""

from six.moves.urllib.parse import quote

import click

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.vocabularies import (
    get_global_vocabs_cache,
    get_vocabularies,
    install_vocabulary,
    uninstall_vocabulary
)
from cmem.cmempy.workspace import update_global_vocabulary_cache


def _transform_cache_to_table(cache_category, table):
    """Transform a cache category dict to a tabulate table."""
    for item in cache_category:
        uri = item["genericInfo"]["uri"]
        try:
            label = item["genericInfo"]["label"]
        except KeyError:
            label = ""
        row = [uri, "class", label]
        table.append(row)
    return table


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "iri",
    type=click.STRING,
    autocompletion=completion.installed_vocabularies
)
@click.pass_obj
def open_command(app, iri):
    """Open / explore a vocabulary graph in the browser.

    Vocabularies are identified by their graph IRI.
    Installed vocabularies can be listed with the "vocabulary list" command.
    """
    explore_uri = get_cmem_base_uri() + "/explore?graph=" + quote(iri)
    click.launch(explore_uri)
    app.echo_debug(explore_uri)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only vocabulary identifier (IRIs) and no labels or other "
         "meta data. This is useful for piping the ids into other cmemc "
         "commands."
)
@click.option(
    "--filter", "filter_",
    type=click.Choice(
        ["all", "installed", "installable"],
        case_sensitive=True
    ),
    default="installed",
    show_default=True,
    help="Filter list based on status."
)
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON."
)
@click.pass_obj
def list_command(app, id_only, filter_, raw):
    """Output a list of vocabularies.

    Vocabularies are graphs (see 'cmemc graph' command group) which consists
    of class and property descriptions.
    """
    vocabs = get_vocabularies(filter_=filter_)
    if raw:
        app.echo_info_json(vocabs)
    elif id_only:
        for _ in vocabs:
            app.echo_info(_["iri"])
    else:
        table = []
        for _ in vocabs:
            iri = _["iri"]
            try:
                label = _["label"]["title"]
            except (KeyError, TypeError):
                if _["vocabularyLabel"]:
                    label = _["vocabularyLabel"]
                else:
                    label = "[no label given]"
            table.append((iri, label))
        # sort output by label - https://docs.python.org/3/howto/sorting.html
        table = sorted(table, key=lambda k: k[1].lower())
        app.echo_info_table(
            table,
            headers=["Vocabulary Graph IRI", "Label"]
        )


@click.command(cls=CmemcCommand, name="install")
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.installable_vocabularies
)
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Install all vocabularies from the catalog."
)
@click.pass_obj
def install_command(app, iris, all_):
    """Install one or more vocabularies from the catalog.

    Vocabularies are identified by their graph IRI.
    Installable vocabularies can be listed with the
    "vocabulary list --filter installable" command.
    """
    if iris == () and not all_:
        raise ValueError("Either specify at least one vocabulary "
                         + "IRI or use the --all option to install all "
                           "vocabularies from the catalog.")
    if all_:
        iris = (
            [iri["iri"] for iri in get_vocabularies(filter_="installable")]
        )
    count: int = len(iris)
    current: int = 1
    for iri in iris:
        app.echo_info(
            "Install vocabulary {}/{}: {} ... ".format(current, count, iri),
            nl=False)
        install_vocabulary(iri)
        app.echo_success("done")
        current = current + 1


@click.command(cls=CmemcCommand, name="uninstall")
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.installed_vocabularies
)
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Uninstall all installed vocabularies."
)
@click.pass_obj
def uninstall_command(app, iris, all_):
    """Uninstall one or more vocabularies.

    Vocabularies are identified by their graph IRI.
    Already installed vocabularies can be listed with the
    "vocabulary list --filter installed" command.
    """
    if iris == () and not all_:
        raise ValueError("Either specify at least one vocabulary "
                         + "IRI or use the --all option to uninstall all "
                           "installed vocabularies.")
    if all_:
        iris = (
            [iri["iri"] for iri in get_vocabularies(filter_="installed")]
        )
    count: int = len(iris)
    current: int = 1
    for iri in iris:
        app.echo_info(
            "Uninstall vocabulary {}/{}: {} ... ".format(current, count, iri),
            nl=False)
        uninstall_vocabulary(iri)
        app.echo_success("done")
        current = current + 1


@click.command(cls=CmemcCommand, name="update")
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.installed_vocabularies
)
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Update cache for all installed vocabularies."
)
@click.pass_obj
def cache_update_command(app, iris, all_):
    """Reload / updates the data integration cache for a vocabulary."""
    if iris == () and not all_:
        raise ValueError("Either specify at least one vocabulary "
                         + "IRI or use the --all option to update the "
                           "cache for all installed vocabularies.")
    if all_:
        iris = (
            [iri["iri"] for iri in get_vocabularies(filter_="installed")]
        )
    count: int = len(iris)
    current: int = 1
    for iri in iris:
        app.echo_info(
            "Update cache {}/{}: {} ... ".format(current, count, iri),
            nl=False)
        update_global_vocabulary_cache(iri)
        app.echo_success("done")
        current = current + 1


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only vocabulary term identifier (IRIs) and no labels or other "
         "meta data. This is useful for piping the ids into other cmemc "
         "commands."
)
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON."
)
@click.pass_obj
def cache_list_command(app, id_only, raw):
    """Output the content of the global vocabulary cache."""
    cache_ = get_global_vocabs_cache()
    if raw:
        app.echo_info_json(cache_)
    elif id_only:
        for vocab in cache_["vocabularies"]:
            for class_ in vocab["classes"]:
                app.echo_info(class_["genericInfo"]["uri"])
            for property_ in vocab["properties"]:
                app.echo_info(property_["genericInfo"]["uri"])
    else:
        table = []
        for vocab in cache_["vocabularies"]:
            table = _transform_cache_to_table(vocab["classes"], table)
            table = _transform_cache_to_table(vocab["properties"], table)
        app.echo_info_table(
            table,
            headers=["IRI", "Type", "Label"]
        )


@click.group(cls=CmemcGroup)
def cache():
    """List und update the vocabulary cache."""


cache.add_command(cache_update_command)
cache.add_command(cache_list_command)


@click.group(cls=CmemcGroup)
def vocabulary():
    """List, install, uninstall and open vocabularies."""


vocabulary.add_command(open_command)
vocabulary.add_command(list_command)
vocabulary.add_command(install_command)
vocabulary.add_command(uninstall_command)
vocabulary.add_command(cache)
