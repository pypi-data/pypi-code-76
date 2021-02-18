from urllib import parse as parseurl

import requests
from command_tool.utils.utils import error_exit, logger


def get_scan_library_versions_overview(scan_id, apikey, baseurl):
    api = f"/v1/scans/{scan_id}/library-versions/overview/"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit("Fail to get scan components information")

    logger.debug(f"[get_scan_library_versions_overview]\n{result.json()}")
    return result.json()["library_count"], result.json()["vulnerable_libraries_count"]


def get_scan_issues_overview(scan_id, apikey, baseurl):
    api = f"/v1/scans/{scan_id}/issues/?limit=99999&page=1"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit("Fail to get scan vulnerability information")

    return len(result.json()["results"])


def get_scan_license_overview(scan_id, apikey, baseurl):
    api = f"/v1/scans/{scan_id}/licenseissues/?limit=99999&page=1"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit("Fail to get scan license issue information")

    return len(result.json()["results"])


def get_scan_summary(scan_id, apikey, baseurl):
    (
        scan_components_count,
        scan_vul_components_count,
    ) = get_scan_library_versions_overview(scan_id, apikey, baseurl)
    scan_vulnerability_count = get_scan_issues_overview(scan_id, apikey, baseurl)
    scan_licenseissue_count = get_scan_license_overview(scan_id, apikey, baseurl)

    logger.info(
        f"scan_components_count : {scan_components_count}, scan_vul_components_count : {scan_vul_components_count}\nscan_vulnerability_count : {scan_vulnerability_count}, scan_licenseissue_count : {scan_licenseissue_count}"
    )


def get_scan_issue_detail(baseurl, apikey, scan_issue_id):
    api = f"/v1/issues/{scan_issue_id}"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit(f"Fail to get scan issue: {scan_issue_id} detail.")

    return result.json()


def get_scan_issue_list(baseurl, apikey, scan_id):
    api = f"v1/scans/{scan_id}/issues/"
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        logger.debug(
            f"scan_result|get_scan_issue_list| status_code: {result.status_code} message: {result.text}"
        )
        error_exit(f"Fail to get scan {scan_id} issue list.")

    return result.json()["results"]
