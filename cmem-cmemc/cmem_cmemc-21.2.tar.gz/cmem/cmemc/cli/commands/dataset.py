"""workspace commands for cmem command line interface."""

import json
import os

import click

import requests.exceptions

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup
from cmem.cmempy.workspace.search import list_items
from cmem.cmempy.workspace.projects.project import (
    get_projects
)
from cmem.cmempy.workspace.projects.datasets.dataset import (
    create_dataset,
    delete_dataset,
    get_dataset
)
from cmem.cmempy.workspace.projects.resources.resource import (
    create_resource,
    get_resource_response,
    resource_exist
)
from cmem.cmempy.workspace import (
    get_task_plugin_description,
    get_task_plugins
)


def _validate_and_split_dataset_id(dataset_id):
    """Validate and split cmemc dataset ID.

    Args:
        dataset_id (str): The cmemc dataset ID in the workspace.

    Raises:
        ValueError: in case the dataset ID is not splittable
    """
    try:
        project_part = dataset_id.split(":")[0]
        dataset_part = dataset_id.split(":")[1]
    except IndexError as error:
        raise ValueError(
            "{} is not a valid dataset ID. Use the 'cmemc dataset list' "
            "command to get a list of existing datasets."
            .format(dataset_id)
        ) from error
    return project_part, dataset_part


def _upload_file_resource(
        app=None,
        project_id=None,
        local_file_name=None,
        remote_file_name=None,
        replace=False
):
    """Upload a local file as a dataset resource to a project.

    Args:
        app (ApplicationContext): the click cli app context.
        project_id (str): The project ID in the workspace.
        local_file_name (str): The path to the local file name
        remote_file_name (str): The remote file name
        replace (bool): Replace resource if needed.

    Raises:
        ValueError: if resource exists and no replace
    """
    exist = resource_exist(
        project_name=project_id, resource_name=remote_file_name
    )
    if exist and not replace:
        raise ValueError(
            "A file resource with the name '{}' already exists "
            "in this project. \n"
            "Please rename the file or use the '--replace' "
            "parameter in order to overwrite the remote file."
            .format(remote_file_name)
        )
    if exist:
        app.echo_info(
            "Replace content of {} with content from {} in project {} ... "
            .format(
                remote_file_name,
                local_file_name,
                project_id
            ),
            nl=False
        )
    else:
        app.echo_info(
            "Upload {} as a file resource {} to project {} ... "
            .format(
                local_file_name,
                remote_file_name,
                project_id
            ),
            nl=False
        )
    create_resource(
        project_name=project_id,
        resource_name=remote_file_name,
        file_resource=click.open_file(local_file_name, "rb"),
        replace=replace
    )
    app.echo_success("done")


def _get_metadata_out_of_parameter(parameter_dict):
    """Extract metadata keys out of the parameter dict.

    Args:
        parameter_dict (dict): the dictionary of given parameters.

    Returns:
        The dictionary of only the known metadata fields.
    """
    metadata_dict = {}
    if "label" in parameter_dict:
        metadata_dict["label"] = parameter_dict["label"]
    if "description" in parameter_dict:
        metadata_dict["description"] = parameter_dict["description"]
    return metadata_dict


def _extend_parameter_with_metadata(
        app,
        parameter_dict=None,
        dataset_type=None,
        dataset_file=None
):
    """Extend the parameter with label if needed.

    Args:
        app (ApplicationContext): the click cli app context.
        parameter_dict (dict): The dictionary of given dataset parameters
        dataset_type (str): The dataset type ID
        dataset_file (str): The path of the local file

    Returns:
        An extended parameter dictionary (label + file)
    """
    if "label" not in parameter_dict:
        if dataset_file:
            parameter_dict["label"] = os.path.basename(dataset_file)
        if "file" in parameter_dict:
            parameter_dict["label"] = parameter_dict["file"]
        if "label" not in parameter_dict:
            parameter_dict["label"] = "Unnamed {} dataset".format(dataset_type)
        app.echo_warning("Missing dataset label (-p label xxx) - "
                         "this generated label will be used: {}"
                         .format(parameter_dict["label"])
                         )
    return parameter_dict


def _check_or_set_dataset_type(
        app,
        parameter_dict=None,
        dataset_type=None,
        dataset_file=None
):
    """Check for missing dataset type.

    Args:
        app (ApplicationContext): the click cli app context.
        parameter_dict (dict): The dictionary of given dataset parameters
        dataset_type (str): The dataset type ID.
        dataset_file (str): The path of the local file.

    Returns:
        A dataset type based the given file names.
    """
    if dataset_file:
        source = os.path.basename(dataset_file)
    else:
        source = ""
    if "file" in parameter_dict:
        target = parameter_dict["file"]
    else:
        target = ""
    suggestions = (
        (".ttl", "file"),
        (".csv", "csv"),
        (".xlsx", "excel"),
        (".xml", "xml"),
        (".json", "json"),
        (".orc", "orc"),
        (".zip", "multiCsv")
    )
    if not dataset_type:
        for check, type_ in suggestions:
            if source.endswith(check) or target.endswith(check):
                dataset_type = type_
        if not dataset_type:
            raise ValueError("Missing parameter. Please specify a dataset "
                             "type with '--type'.")
        app.echo_warning(
            "Missing dataset type (--type) - based on the used file name, "
            "this type is assumed: {}".format(dataset_type)
        )
    return dataset_type


def _show_parameter_list(app, dataset_type=None):
    """Output the parameter list for a given dataset type.

    Args:
        app (ApplicationContext): the click cli app context.
        dataset_type (dict): The type from which the parameters are listed.
    """
    plugin = get_task_plugin_description(dataset_type)
    properties = plugin["properties"]
    required_properties = plugin["required"]
    table = []
    for key in properties:
        if key in required_properties:
            parameter = key + " *"
            description = "(Required) " + properties[key]["description"]
        else:
            parameter = key
            description = properties[key]["description"]
        row = [
            parameter,
            description,
        ]
        table.append(row)
    # metadata always on top, then sorted by key
    table = sorted(table, key=lambda k: k[0].lower())
    table = completion.add_metadata_parameter(table)
    app.echo_info_table(
        table,
        headers=["Parameter", "Description"]
    )


def _show_type_list(app):
    """Output the list of dataset types.

    Args:
        app (ApplicationContext): the click cli app context.
    """
    plugins = get_task_plugins()
    table = []
    for plugin_id in plugins:
        plugin = plugins[plugin_id]
        if plugin["taskType"] == "Dataset":
            id_ = plugin_id
            description = "{}: {}".format(
                plugin["title"],
                plugin["description"].partition("\n")[0]
            )
            row = [
                id_,
                description,
            ]
            table.append(row)
    table = sorted(table, key=lambda k: k[1].lower())
    app.echo_info_table(
        table,
        headers=["Dataset Type", "Description"]
    )


def _get_metadata_table(project, table=None, prefix=""):
    """Prepare flat key/value table.

    This function gets the project dictionary and creates
    a flat structure out of it key by key. For each level deeper
    it prefixes the father keys.

    Example input:  {'k1': '1', 'k2': {'k3': '3', 'k4': '4'}}
    Example output: [['k1', '1'], ['k2:k3', '3'], ['k2:k4', '4']]

    Args:
        project (dict): The dictionary which is transformed into a table.
        table (list): The table where the key/value rows will be appended.
        prefix (str): A prefix which is used to indicate the level.

    Returns:
        The input table extended with rows from the input dictionary.
    """
    if table is None:
        table = []
    if len(prefix) != 0:
        prefix = prefix + ":"
    for key in project:
        if isinstance(project[key], str):
            row = [
                prefix + key,
                project[key]
            ]
            table.append(row)
        if isinstance(project[key], dict):
            table = _get_metadata_table(
                project[key],
                table,
                prefix + key
            )
    return table


def _check_or_select_project(app, project_id=None):
    """Check for given project, select the first one if there is only one.

    Args:
        app (ApplicationContext): the click cli app context.
        project_id (str): The project ID.

    Raises:
        ValueError: if no projects available.
        ValueError: if more than one project is.

    Returns:
        Maybe project_id if there was no project_id before.
    """
    if project_id is not None:
        return project_id

    projects = get_projects()
    if len(projects) == 1:
        app.echo_warning(
            "Missing project (--project) - since there is only one project, "
            "this is selected: {}"
            .format(projects[0]["name"])
        )
        return projects[0]["name"]

    if len(projects) == 0:
        raise ValueError(
            "There are no projects available. "
            "Please create a project with"
            "'cmemc project create'."
        )

    # more than one project
    raise ValueError(
        "There is more than one project available so you need to "
        "specify the project with '--project'."
    )


def _check_or_select_dataset_type(app, dataset_type):
    """Test type and return plugin.

    Args:
        app (ApplicationContext): the click cli app context.
        dataset_type (str): A dataset type

    Raises:
        ValueError: If type is not known

    Returns:
        A tuple of dataset_type and corresponding plugin description (dict)
    """
    try:
        app.echo_debug("check type {}".format(dataset_type))
        plugin = get_task_plugin_description(dataset_type)
        return dataset_type, plugin
    except requests.exceptions.HTTPError as error:
        raise ValueError(
            "Unknown dataset type: {}."
            .format(dataset_type)
        ) from error


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--project", "project_id",
    type=click.STRING,
    autocompletion=completion.project_ids,
    help="The project, from which you want to list the datasets. "
         "Project IDs can be listed with the 'project list' command."
)
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON objects of dataset search API response."
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only dataset identifier and no labels or other meta data. "
         "This is useful for piping the ids into other cmemc commands."
)
@click.pass_obj
def list_command(app, project_id, raw, id_only):
    """List available datasets.

    Outputs a list of datasets IDs which can be used as reference for
    the dataset create and delete commands.
    """
    results = list_items(
        item_type="dataset",
        project=project_id
    )
    datasets = results["results"]
    if raw:
        app.echo_info_json(results)
    elif id_only:
        for _ in datasets:
            app.echo_info(_["projectId"] + ":" + _["id"])
    else:
        table = []
        for _ in datasets:
            row = [
                _["projectId"] + ":" + _["id"],
                _["pluginId"],
                _["label"],
            ]
            table.append(row)
        # sort output by label - https://docs.python.org/3/howto/sorting.html
        table = sorted(table, key=lambda k: k[2].lower())
        app.echo_info_table(
            table,
            headers=["Dataset ID", "Type", "Label"]
        )


@click.command(cls=CmemcCommand, name="delete")
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Delete all datasets. "
         "This is a dangerous option, so use it with care.",
)
@click.option(
    "--project", "project_id",
    type=click.STRING,
    autocompletion=completion.project_ids,
    help="In combination with the '--all' flag, this option allows for "
         "deletion of all datasets of a certain project. The behaviour is "
         "similar to the 'dataset list --project' command."
)
@click.argument(
    "dataset_ids",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.dataset_ids
)
@click.pass_obj
def delete_command(app, project_id, all_, dataset_ids):
    """Delete datasets.

    This deletes existing datasets in integration projects from Corporate
    Memory. Datasets will be deleted without prompting!
    Dataset resources will not be deleted.

    Example: cmemc dataset delete my_project:my_dataset

    Datasets can be listed by using the 'cmemc dataset list' command.
    """
    if dataset_ids == () and not all_:
        raise ValueError("Either specify at least one dataset ID "
                         + "or use the --all option to delete all datasets.")

    if all_:
        # in case --all is given, a list of datasets is fetched
        dataset_ids = []
        datasets = list_items(item_type="dataset", project=project_id)
        for _ in datasets["results"]:
            dataset_ids.append(_["projectId"] + ":" + _["id"])

    count = len(dataset_ids)
    current = 1
    for _ in dataset_ids:
        app.echo_info("Delete dataset {}/{}: {} ... "
                      .format(current, count, _), nl=False)
        project_part, dataset_part = _validate_and_split_dataset_id(_)
        app.echo_debug("Project ID is {}, dataset ID is {}"
                       .format(project_part, dataset_part))
        delete_dataset(project_part, dataset_part)
        app.echo_success("done")
        current = current + 1


@click.command(cls=CmemcCommand, name="download")
@click.argument(
    "dataset_id",
    type=click.STRING,
    autocompletion=completion.dataset_ids
)
@click.argument(
    "output_path",
    required=True,
    type=click.Path(
        allow_dash=True,
        dir_okay=False,
        writable=True
    )
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace existing files. This is a dangerous option, "
         "so use it with care.",
)
@click.pass_obj
def download_command(app, dataset_id, output_path, replace):
    """Download the resource file of a dataset.

    This command downloads the file resource of a dataset to your local
    file system or to standard out (-).
    Note that this is not possible for dataset types such as
    Knowledge Graph (eccencaDataplatform) or SQL endpoint (sqlEndpoint).

    Without providing an output path, the output file name will be the
    same as the remote file resource.

    Datasets can be listed by using the 'cmemc dataset list' command.
    """
    app.echo_debug(
        "Dataset ID is {}; output path is {}. replace is {}."
        .format(dataset_id, click.format_filename(output_path), replace)
    )
    project_part, dataset_part = _validate_and_split_dataset_id(dataset_id)
    project = get_dataset(project_part, dataset_part)
    try:
        file = project['data']['parameters']['file']
    except KeyError as no_file_resource:
        raise ValueError(
            "The dataset {} has no associated file resource."
            .format(dataset_id)
        ) from no_file_resource
    if os.path.exists(output_path) and replace is not True:
        raise ValueError("Target file {} already exists. "
                         "Use --replace in case you want to replace it."
                         .format(click.format_filename(output_path))
                         )
    with get_resource_response(project_part, file) as response:
        # if piping file to stdout, no info messages
        if output_path != "-":
            app.echo_info(
                "Download resource {} of dataset {} to file {} ... "
                .format(file, dataset_id, click.format_filename(output_path)),
                nl=False
            )
        with click.open_file(output_path, "wb") as resource_file:
            for chunk in response.iter_content(chunk_size=8192):
                resource_file.write(chunk)
            # if piping file to stdout, no info messages
        if output_path != "-":
            app.echo_success("done")


@click.command(cls=CmemcCommand, name="upload")
@click.argument(
    "dataset_id",
    type=click.STRING,
    autocompletion=completion.dataset_ids
)
@click.argument(
    "input_path",
    required=True,
    autocompletion=completion.dataset_files,
    type=click.Path(
        allow_dash=True,
        dir_okay=False,
        writable=True
    )
)
@click.pass_obj
def upload_command(app, dataset_id, input_path):
    """Upload a resource file to a dataset.

    This command uploads a file to a dataset.
    The content of the uploaded file replaces the remote file resource.
    The name of the remote file resource is not changed.

    Warning: If the remote file resource is used in more than one dataset,
    the other datasets are also affected by this command.

    Warning: The content of the uploaded file is not tested, so uploading
    a json file to an xml dataset will result in errors.

    Datasets can be listed by using the 'cmemc dataset list' command.

    Example: cmemc dataset upload cmem:my-dataset new-file.csv
    """
    project_part, dataset_part = _validate_and_split_dataset_id(dataset_id)
    project = get_dataset(project_part, dataset_part)
    try:
        remote_file_name = project["data"]["parameters"]["file"]
    except KeyError as error:
        raise ValueError(
            "Dataset {} has no attached file resource to replace."
            .format(dataset_id)
        ) from error

    _upload_file_resource(
        app=app,
        project_id=project_part,
        local_file_name=input_path,
        remote_file_name=remote_file_name,
        replace=True
    )


@click.command(cls=CmemcCommand, name="inspect")
@click.argument(
    "dataset_id",
    type=click.STRING,
    autocompletion=completion.dataset_ids
)
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON."
)
@click.pass_obj
def inspect_command(app, dataset_id, raw):
    """Display meta data of a dataset."""
    app.echo_debug(
        "Dataset ID is {}"
        .format(dataset_id)
    )
    project_part, dataset_part = _validate_and_split_dataset_id(dataset_id)
    project = get_dataset(project_part, dataset_part)
    if raw:
        app.echo_info_json(project)
    else:
        table = _get_metadata_table(project)
        app.echo_info_table(
            table,
            headers=["Key", "Value"]
        )


# pylint: disable-msg=too-many-locals,too-many-arguments
@click.command(cls=CmemcCommand, name="create")
@click.argument(
    "DATASET_FILE",
    required=False,
    autocompletion=completion.dataset_files,
    type=click.Path(
        allow_dash=False,
        readable=True,
        exists=True
    )
    # TODO: Allow dash here / enable creation of file resources from stdin.
)
@click.option(
    "--type", "-t", "dataset_type",
    multiple=False,
    type=click.STRING,
    autocompletion=completion.dataset_types,
    help="The dataset type of the dataset to create. Example types are 'csv',"
         "'json' and 'eccencaDataPlatform' (-> Knowledge Graph)."
)
@click.option(
    "--project", "project_id",
    type=click.STRING,
    autocompletion=completion.project_ids,
    help="The project, where you want to create the dataset in. If there is "
         "only one project in the workspace, this option can be omitted."
)
@click.option(
    "--parameter", "-p",
    type=(str, str),
    autocompletion=completion.dataset_parameter,
    multiple=True,
    help="A set of key/value pairs. Each dataset type has different "
         "parameters (such as charset, arraySeparator, ignoreBadLines, ...). "
         "In order to get a list of possible parameter, use the"
         "'--help-parameter' option."
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace remote file resources in case there "
         "already exists a file with the same name."
)
@click.option(
    "--id", "dataset_id",
    type=click.STRING,
    help="The dataset ID of the dataset to create. The dataset ID will be "
         "automatically created in case it is not present."
)
@click.option(
    "--help-types",
    is_flag=True,
    help="Lists all possible dataset types on given Corporate Memory "
         "instance. Note that this option already needs access to the "
         "instance."
)
@click.option(
    "--help-parameter",
    is_flag=True,
    help="Lists all possible (optional and mandatory) parameter for a dataset "
         "type. Note that this option already needs access to the instance."
)
@click.pass_obj
def create_command(
        app, dataset_file, replace,
        project_id, dataset_id, dataset_type, parameter,
        help_parameter, help_types
):
    """Create a dataset.

    Datasets are created in projects and can have associated file
    resources. Each dataset has a type (such as 'csv') and a list of
    parameter which can change or specify the dataset behaviour.

    To get more information on possible dataset types and parameter on these
    types, use the '--help-types' and '--help-parameter' options.

    Example: cmemc dataset create --project my-project --type csv my-file.csv
    """
    if help_types:
        _show_type_list(app)
        return

    # transform the parameter list of tuple to a dictionary
    parameter_dict = {}
    for key, value in parameter:
        parameter_dict[key] = value

    dataset_type = _check_or_set_dataset_type(
        app,
        parameter_dict=parameter_dict,
        dataset_type=dataset_type,
        dataset_file=dataset_file
    )

    if help_parameter:
        _show_parameter_list(app, dataset_type=dataset_type)
        return

    dataset_type, plugin = _check_or_select_dataset_type(app, dataset_type)

    parameter_dict = _extend_parameter_with_metadata(
        app,
        parameter_dict=parameter_dict,
        dataset_type=dataset_type,
        dataset_file=dataset_file
    )

    project_id = _check_or_select_project(app, project_id)

    # file required but not given
    if "file" in plugin["required"] \
            and not dataset_file \
            and "file" not in parameter_dict:
        raise ValueError(
            "The dataset type {} is file based, so you need to specify a "
            "file with the create command."
            .format(dataset_type)
        )

    # file required and given
    # dataset_file = file path from the command line
    # parameter_dict["file"] = local name in DI
    if "file" in plugin["required"] and dataset_file:
        # add file parameter for the project if needed
        if "file" not in parameter_dict:
            parameter_dict["file"] = os.path.basename(dataset_file)
        _upload_file_resource(
            app=app,
            project_id=project_id,
            local_file_name=dataset_file,
            remote_file_name=parameter_dict["file"],
            replace=replace
        )

    # create dataset resource
    app.echo_info(
        "Create a new dataset {}:".format(project_id),
        nl=False
    )
    created_dataset = create_dataset(
        dataset_id=dataset_id, project_id=project_id,
        dataset_type=dataset_type, parameter=parameter_dict,
        metadata=_get_metadata_out_of_parameter(parameter_dict)
    )
    app.echo_info(
        "{} ... ".format(json.loads(created_dataset)["id"]),
        nl=False
    )
    app.echo_success("done")


@click.group(cls=CmemcGroup)
def dataset():
    """List, create, delete, inspect datasets.

    This command group allows for managing workspace datasets as well as
    dataset file resources. Datasets can be created and deleted.
    File resources can be uploaded and downloaded.
    Details of dataset parameter can be listed with inspect.

    Datasets are identified with a combined key of the project ID and the
    project internal dataset ID (e.g: my-project:my-dataset). To get a list
    of datasets, use the list command.
    """


dataset.add_command(list_command)
dataset.add_command(delete_command)
dataset.add_command(download_command)
dataset.add_command(upload_command)
dataset.add_command(inspect_command)
dataset.add_command(create_command)
