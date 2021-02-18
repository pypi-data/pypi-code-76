import os
import time
from urllib import parse as parseurl

import requests

from .project import get_upload_files, uploadfile2project
from .user import show_user
from .utils import error_exit, exec_command, logger


def get_scan_id(apikey, baseurl, project_id):
    """
    Get the most recent scan id of the user or the project if project_id is provided
    :param project_id: Integer, Nullable, return most recent scan id if null.
    :return: Integer, scan id.
    """
    api = "/v1/scans/"

    # if no project id, return user's most recent scan id
    if not project_id:
        headers = {
            "Authorization": "Token " + apikey,
            "Content-Type": "application/json; charset=utf-8",
        }
        url = parseurl.urljoin(baseurl, api)
        result = requests.get(url=url, headers=headers)
        if result.status_code not in [200, 201]:
            error_exit(
                "can not get the most recent project info, please try again or check your project id"
            )
        user_id = show_user(apikey, baseurl)["user_id"]
        for scan in result.json()["results"]:
            if scan["owner"] == user_id:
                return scan["id"]
        error_exit(f"Not found the most recent scan for user {user_id}")

    # if project id not null, try find the project and return its latest scan id
    api = "/v1/projects/"
    endpoint = parseurl.urljoin(api, project_id)
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, endpoint)
    result = requests.get(url=url, headers=headers)
    if result.status_code not in [200, 201]:
        error_exit(
            f"can not get the project (id: {project_id}) info, please try again or check your project id"
        )

    if "lastScan" not in result.json():
        error_exit(
            f"the latest scan not found in project {project_id}. Please try again or check your project id."
        )

    logger.debug(result.json())
    return result.json()["lastScan"]["id"]


def create_scan(project_id, scan_type, branch, apikey, baseurl):
    """
    Create new scan.
    :param project_id: Integer
    :param scan_type: utils.ScanType
    :param branch: String, branch name for git project, upload_file_id for upload project
    :return: Integer, scan id.
    """
    api = "/v1/projects/%s/scans/"
    endpoint = api % (project_id)
    url = parseurl.urljoin(baseurl, endpoint)
    payload = {"scan_type": scan_type, "branch": branch}
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    r = requests.post(url=url, headers=headers, json=payload)
    if r.status_code not in [200, 201]:
        error_exit("failed to create scan")
    scan_id = r.json().get("project").get("lastScan").get("id")
    return {"scan_id": scan_id}


def scan_upload_proj(file, apikey, baseurl, version, scan_type, project_id):
    """
    Upload file and create scan. Support Binary scan and upload zip source code file scan.
    :param file: String, path of upload file
    :param version: String, version of the upload file
    :param scan_type: ScanType, source_code or binary
    :param project_id: Integer, id of the project
    :return: Dict, info about the scan
    """
    user_id = show_user(apikey, baseurl)["user_id"]

    logger.info("Uploading file...")
    uploadfile2project(file, user_id, project_id, version, apikey, baseurl)

    file_info = get_upload_files(apikey, baseurl, project_id)
    upload_file_id = file_info[0]["id"]
    logger.info("Sending scan request...")
    scan_info = create_scan(project_id, scan_type, upload_file_id, apikey, baseurl)
    logger.info("Start scan...")
    return scan_info["scan_id"], project_id


def scan_latest_version(apikey, baseurl, scan_type, project_id):
    file_info = get_upload_files(apikey, baseurl, project_id)
    if not file_info:
        error_exit("No upload file info found.")
    upload_file_id = file_info[0]["id"]

    logger.info("Sending scan request...")
    r = create_scan(project_id, scan_type, upload_file_id, apikey, baseurl)
    return r["scan_id"], project_id


# refactor
def scan_sourcecode(folderpath, scantistoken, baseurl):
    scan_id = "N.A."

    os.environ["SCANTISTTOKEN"] = scantistoken
    os.environ["SCANTIST_IMPORT_URL"] = f"{baseurl}/ci-scan/"

    tail_path, basename = os.path.split(folderpath.rstrip("/\\"))
    # remove /scan/ in directory
    sbd_path = os.path.join(
        os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],
        "scantist-bom-detect.jar",
    )

    logger.info("Generating dependency tree in bom detect...")
    cmd = (
        "java -jar -Xmx1024m %s "
        "-repo_name %s "
        "-working_dir %s "
        "-build_time %s "
        "-depth 3" % (sbd_path, basename, folderpath, int(time.time()))
    )
    logger.debug(f"bom-detect cmd: {cmd}")
    # get scan id from output
    result = exec_command(cmd)
    cmd_output = result["output"].decode("utf-8").splitlines()
    logger.debug(result)
    for line in cmd_output:
        if " - scan_id:" in line:
            try:
                scan_id_index = line.index(" - scan_id:") + 11
                scan_id = line[scan_id_index:]
            except:
                logger.info(f"\nfailed to find scan : {folderpath}")
                return {"scan_id": scan_id}
    if scan_id == "N.A.":
        error_exit(f"error getting scan id: {result['error'].decode('utf-8')}")

    logger.info("Start scan...")
    return scan_id


# def scan_source_code_list(zip_paths, scantist_token, baseurl):
#     """
#     Read the txt file which includes a list of path directs to source code zip and batch process projects.
#     :return:
#     """
#     project_paths = read_paths(zip_paths)
#
#     if not os.path.exists(os.path.dirname(zip_paths)):
#         error_exit("for batch source code scan, please specify a valid txt file")
#
#     for path in project_paths:
#         try:
#             scan_sourcecode(path, scantist_token, baseurl)
#         except Exception:
#             continue
