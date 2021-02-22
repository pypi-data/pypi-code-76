"""DataIntegration project commands for the cmem command line interface."""

import os
from pathlib import Path

import click

from jinja2 import Template

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup
from cmem.cmempy.config import get_di_api_endpoint
from cmem.cmempy.plugins.marshalling import (
    get_extension_by_plugin,
    get_plugin_by_extension
)
from cmem.cmempy.workspace.projects.export_ import export_project
from cmem.cmempy.workspace.projects.import_ import import_project
from cmem.cmempy.workspace.projects.project import (
    delete_project,
    get_projects,
    make_new_project
)


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "project_ids",
    nargs=-1,
    required=True,
    type=click.STRING,
    autocompletion=completion.project_ids
)
@click.pass_obj
def open_command(app, project_ids):
    """Open projects in the browser.

    With this command, you can open a project in the workspace in
    your browser to change them.

    The command accepts multiple projects IDs which results in
    opening multiple browser tabs.
    """
    projects = get_projects()
    for _ in project_ids:
        if _ not in (p["name"] for p in projects):
            raise ValueError("Project '{}' not found.".format(_))
        open_project_uri = "{}/workbench/projects/{}".format(
            get_di_api_endpoint(),
            _
        )
        app.echo_debug("Open {}: {}".format(_, open_project_uri))
        click.launch(open_project_uri)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON."
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only project identifier and no labels or other "
         "meta data. This is useful for piping the IDs into other commands."
)
@click.pass_obj
def list_command(app, raw, id_only):
    """List available projects.

    Outputs a list of project IDs which can be used as reference for
    the project create, delete, export and import commands.
    """
    projects = get_projects()
    if raw:
        app.echo_info_json(projects)
        return
    if id_only:
        for _ in sorted(projects, key=lambda k: k["name"].lower()):
            app.echo_result(_["name"])
        return
    # output a user table
    table = []
    for _ in projects:
        row = [
            _["name"],
            _["metaData"]["label"],
        ]
        table.append(row)
    # sort output by label - https://docs.python.org/3/howto/sorting.html
    table = sorted(table, key=lambda k: k[1].lower())
    app.echo_info_table(
        table,
        headers=["Project ID", "Label"]
    )


@click.command(cls=CmemcCommand, name="delete")
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Delete all projects. "
         "This is a dangerous option, so use it with care.",
)
@click.argument(
    "project_ids",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.project_ids
)
@click.pass_obj
def delete_command(app, all_, project_ids):
    """Delete project(s).

    This deletes existing data integration projects from Corporate Memory.
    Projects will be deleted without prompting!

    Example: cmemc project delete my_project

    Projects can be listed by using the 'cmemc project list' command.
    """
    if project_ids == () and not all_:
        raise ValueError("Either specify at least one project ID "
                         + "or use the --all option to delete all projects.")
    if all_:
        # in case --all is given, a list of project is fetched
        project_ids = (
            [currentProjects["name"] for currentProjects in get_projects()]
        )
    count = len(project_ids)
    current = 1
    for project_id in project_ids:
        app.echo_info("Delete project {}/{}: {} ... "
                      .format(current, count, project_id), nl=False)
        # always fetch the current list of projects
        if project_id in ([_["name"] for _ in get_projects()]):
            delete_project(project_id)
            app.echo_success("done")
        else:
            app.echo_error("not found")
        current = current + 1


@click.command(cls=CmemcCommand, name="create")
@click.argument(
    "project_ids",
    nargs=-1,
    required=True,
    type=click.STRING
)
@click.pass_obj
def create_command(app, project_ids):
    """Create empty new project(s).

    This creates one or more new projects.
    Existing projects will not be overwritten.

    Example: cmemc project create my_project

    Projects can be listed by using the 'cmemc project list' command.
    """
    count = len(project_ids)
    current = 1
    for project_id in project_ids:
        app.echo_info("Create new project {}/{}: {} ... "
                      .format(current, count, project_id), nl=False)
        app.echo_debug(get_projects())
        # always fetch the current list of projects
        if project_id not in ([_["name"] for _ in get_projects()]):
            make_new_project(project_id)
            app.echo_success("done")
        else:
            app.echo_error("already there")
        current = current + 1


# pylint: disable=too-many-arguments
@click.command(cls=CmemcCommand, name="export")
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Export all projects.",
)
@click.option(
    "-o", "--overwrite",
    is_flag=True,
    help="Overwrite existing files. This is a dangerous option, "
         "so use it with care.",
)
@click.option(
    "--output-dir",
    default=".",
    show_default=True,
    type=click.Path(
        writable=True,
        file_okay=False
    ),
    # autocompletion=directories,
    help="Directory, where the project files will be created. "
         "This directory will be created as well it does not exists."
)
@click.option(
    "--type", "marshalling_plugin",
    default="xmlZip",
    show_default=True,
    type=click.STRING,
    autocompletion=completion.marshalling_plugins,
    help="Type of the exported project file(s)."
)
@click.option(
    "--filename-template", "-t", "template",
    default="{{date}}-{{connection}}-{{id}}.project",
    show_default=True,
    type=click.STRING,
    autocompletion=completion.project_export_templates,
    help="Template for the export file name(s). "
         "Possible placeholders are (Jinja2): "
         "{{id}} (the project ID), "
         "{{connection}} (from the --connection option) and "
         "{{date}} (the current date as YYYY-MM-DD). "
         "The file suffix will be appended. "
         "Needed directories will be created."
)
@click.argument(
    "project_ids",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.project_ids
)
@click.pass_obj
def export_command(
        app, all_, project_ids, overwrite, marshalling_plugin,
        template, output_dir):
    """Export project(s) to file(s).

    Projects can be exported with different export formats.
    The default type is a zip archive which includes meta data as well
    as dataset resources.
    If more than one project is exported, a file is created for each project.
    By default, these files are created in the current directory and with
    a descriptive name (see --template option default).

    Example: cmemc project export my_project

    Available projects can be listed by using the 'cmemc project list' command.

    You can use the template string to create subdirectories as well:
    cmemc config list | parallel -I% cmemc -c % project export --all
    -t "dump/{{connection}}/{{date}}-{{id}}.project"
    """
    # pylint: disable=too-many-arguments
    if project_ids == () and not all_:
        raise ValueError("Either specify at least one project ID "
                         + "or use the --all option to export all projects.")
    if all_:
        # in case --all is given, a list of project is fetched
        project_ids = ([_["name"] for _ in get_projects()])

    template_data = app.get_template_data()

    count = len(project_ids)
    current = 1
    for project_id in project_ids:
        # prepare the template data and create the actual file incl. suffix
        template_data.update(id=project_id)
        file_name = Template(template).render(template_data)\
            + "." + get_extension_by_plugin(marshalling_plugin)
        # join with given output directory and normalize full path
        export_path = os.path.normpath(os.path.join(output_dir, file_name))
        app.echo_info("Export project {}/{}: {} to {} ... "
                      .format(current, count, project_id, export_path),
                      nl=False)
        if os.path.exists(export_path) and overwrite is not True:
            app.echo_error("file exists")
        else:
            # always fetch the current list of projects
            if project_id in ([_["name"] for _ in get_projects()]):
                export_data = export_project(project_id, marshalling_plugin)
                # output directory is created lazy
                Path(
                    os.path.dirname(export_path)
                ).mkdir(parents=True, exist_ok=True)
                # do the export
                with open(export_path, "wb") as export_file:
                    export_file.write(export_data)
                app.echo_success("done")
            else:
                app.echo_error("project not found")
        current = current + 1


@click.command(cls=CmemcCommand, name="import")
@click.argument(
    "file",
    autocompletion=completion.project_files,
    type=click.Path(
        allow_dash=False,
        dir_okay=False,
        readable=True
    )
)
@click.argument(
    "project_id",
    type=click.STRING,
    autocompletion=completion.project_ids
)
@click.pass_obj
def import_command(app, file, project_id):
    """Import a project from a file.

    Example: cmemc project import my_project.zip my_project
    """
    file_extension = os.path.splitext(file)[1][1:]
    plugin_id = get_plugin_by_extension(file_extension)
    app.echo_info("Import file {} to project {} ... "
                  .format(file, project_id),
                  nl=False)
    if project_id not in ([_["name"] for _ in get_projects()]):
        import_project(project_id, file, plugin_id)
        app.echo_success("done")
    else:
        app.echo_error("already there")


@click.group(cls=CmemcGroup)
def project():
    """List, import, export, create or delete projects.

    Projects are identified by an PROJECTID. The get a list of existing
    projects, execute the list command or use tab-completion.
    """


project.add_command(open_command)
project.add_command(list_command)
project.add_command(export_command)
project.add_command(import_command)
project.add_command(delete_command)
project.add_command(create_command)
