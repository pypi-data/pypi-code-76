import os
import time
from datetime import datetime
from urllib import parse as parseurl

import requests
from command_tool.utils.team import show_teams
from command_tool.utils.user import show_user
from command_tool.utils.utils import error_exit, logger


def get_projects(apikey, baseurl):
    """
    Get all user's projects information through API and return in JSON format.
    :return: JSON, list of projects information
    """
    api = "/v1/projects/"
    endpoint = api
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, endpoint)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit(result.text)
    return result.json()


def show_projects(apikey, baseurl):
    """
    Display user's projects information on console.
    """
    projects_info = get_projects(apikey, baseurl)

    logger.info("Project list:")
    for proj in projects_info["results"]:
        logger.info(
            f"\tname: {proj['name']}\towner_name: {proj['owner_name']},\tid: {proj['id']}\tteam: {proj['team']}\torg_id: {proj['org_id']}"
        )


def get_proj_id(apikey, baseurl, scan_id):
    """
    Get project id through scan id.
    :param scan_id: Integer, scantist scan id
    :return:
    """
    endpoint = "/v1/scans/%s/" % scan_id
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }

    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit(result.text)

    return result.json()["project"]


def _uploadfile(local_file, user, project_id, apikey, baseurl):
    """
    Upload local file for binary scan
    :param local_file: String, path of local file
    :param user: Integer, scantist user id
    :param project_id: Integer, project id for uploading file
    :return: referer, download link, file name and size and modified time.
    """
    api = "/v1/upload/"
    endpoint = api

    referer = "%s/u/%s/org/%s/projects/%s" % (baseurl, user, user, project_id)
    headers = {"Authorization": "Token " + apikey, "referer": referer}
    url = parseurl.urljoin(baseurl, endpoint)
    filename = os.path.basename(local_file)

    if len(filename) > 100:  # limitation of file name length is 70
        filename = os.path.splitext(filename)[0][:70] + os.path.splitext(filename)[1]

    files = {"file": (filename, open(local_file, "rb"), "multipart/form-data")}
    r = requests.post(url, headers=headers, files=files)

    if r.status_code not in [200, 201]:
        error_exit("project|_uploadfile|Fail to upload file.")
        logger.debug("upload_response=%s" % r.text)

    download_link = r.json().get("file").split("/")[-1]
    file_name = local_file.split("/")[len(local_file.split("/")) - 1]
    file_size = os.path.getsize(local_file) / (1024 * 1024)
    file_modified = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug("Successfully upload %s MB file %s." % (file_size, file_name))
    return referer, download_link, file_name, file_size, file_modified


def uploadfile2project(local_file, user, project_id, version, apikey, baseurl):
    """
    Upload file to specific project
    :param local_file: String, path of local file
    :param user: Integer, scantist user id
    :param project_id: Integer, target project id
    :param version: String, version of the project
    :return:
    """
    referer, download_link, file_name, file_size, file_modified = _uploadfile(
        local_file, user, project_id, apikey, baseurl
    )

    headers = {"Authorization": "Token " + apikey, "referer": referer}
    payload = {
        "download_link": download_link,
        "filename": file_name,
        "file_size": file_size,
        "file_modified": file_modified,
        "version": version,
    }

    endpoint = "/v1/projects/%s/uploads/" % (project_id)
    url = parseurl.urljoin(baseurl, endpoint)
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code not in [200, 201]:
        error_exit(f"failed to upload file, error={r.text}, payload={payload}")
    logger.debug(r.json())
    return r.json()


def get_upload_files(apikey, baseurl, project_id):
    """
    show upload files of the project
    :param project_id: the scantist project id
    :return: List, a list of information about uploaded files
    """
    endpoint = "/v1/projects/%s/uploads/" % (project_id)
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, endpoint)
    result = requests.get(url=url, headers=headers)
    if result.status_code != 200:
        logger.error("show_users|failed|err=%s", url)
        error_exit(result.json())
    return result.json()["results"]


def create_project(project_name, org_id, apikey, baseurl):
    """
    create a new project
    :param project_name: String, name of the project
    :param org_id: Integer, id of the organization the project belongs to
    :return: project id
    """
    if len(project_name) > 50:
        logger.info("Project name over limit(50). Will trim to 50 chars.")
        project_name = project_name[:50]

    rst = _create_project(
        project_name=project_name,
        org_id=org_id,
        description="",
        url="",
        download_url="",
        provider="upload",
        apikey=apikey,
        baseurl=baseurl,
    )

    project_id = rst["id"]
    logger.info("project create successfully!")
    return project_id


def _create_project(
    project_name, org_id, description, url, download_url, provider, apikey, baseurl
):
    result = show_teams(apikey, baseurl)

    if not result.get("results") or len(result.get("results", [])) == 0:
        error_exit("no team found.")

    team_id = 0
    for team in result.get("results"):
        # Currently the command line tool does not support user assign org and team, will take default team in default org
        if team["organization"] == org_id and team["user_role"] == "default":
            team_id = team["id"]
            logger.debug(f"_create_project|team={team}")
            break

    if not team_id:
        error_exit(f"no valid team for org_id={org_id}")

    payload = {
        "name": project_name,
        "fullname": project_name,
        "description": description,
        "url": url,
        "download_url": download_url,
        "provider": provider,
        "team": team_id,
        "external_id": project_name + time.time().hex(),
    }

    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }

    endpoint = "/v1/orgs/%s/projects/" % org_id
    url = parseurl.urljoin(baseurl, endpoint)
    logger.info(f"url={url}, payload={payload}")
    r = requests.post(url=url, json=payload, headers=headers)
    if r.status_code != 201:
        error_exit(f"_create_project|failed|status={r.status_code},error={r.text}")
    return r.json()


def set_proj(apikey, baseurl, project_id, project_name, file):
    """
    Set project name. Creat project if no project with the same name found, otherwise, get the project id.
    :param apikey:
    :param baseurl:
    :param project_id:
    :param project_name:
    :param file:
    :return:
    """
    org_id = show_user(apikey, baseurl)["default_org"]

    if not project_id:
        if not project_name:
            file_name = os.path.split(file)[1]
            project_name = file_name.split(".")[0]

        # check if the project exist
        projects_info = get_projects(apikey, baseurl)
        for project_info in projects_info["results"]:
            if project_info["name"] == project_name and project_info["provider"] == "upload":
                project_id = project_info["id"]

        # not existing project
        if not project_id:
            project_id = create_project(project_name, org_id, apikey, baseurl)

    return project_id, project_name
