import base64
import csv
import os
import time
from urllib import parse as parseurl

import requests
from command_tool.utils.scan_result import get_scan_issue_detail, get_scan_issue_list
from command_tool.utils.utils import error_exit, logger


def check_scan(scan_id, project_id, apikey, baseurl):
    api = "v1/projects/%s/scans/%s/"
    endpoint = api % (project_id, scan_id)
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    result = requests.get(url=url, headers=headers)
    if result.status_code not in [200, 201]:
        return {"error": "failed to get scan"}
    return result.json().get("status"), result.json().get("scan_percentage")
    # async with session.get(url=url, headers=headers) as r:
    #     if r.status not in [200, 201]:
    #         return {"error": "failed to get scan"}
    #     scan_status = await r.json()
    #     return scan_status.get("status")


def get_report(scan_id, apikey, baseurl, report_format, output_path, project_id=None):
    # source code scan with bom detect
    if project_id is None:
        generate_report(scan_id, apikey, baseurl)
        return download_report(scan_id, apikey, baseurl, report_format, output_path)

    generate_report(scan_id, apikey, baseurl)
    download_report(scan_id, apikey, baseurl, report_format, output_path)

    # async with aiohttp.ClientSession() as session:
    #     is_download = False
    #     while not is_download:
    #         task = [check_scan(scan_id, project_id, apikey, baseurl, session)]
    #         for f in asyncio.as_completed(task, timeout=1800):
    #             status = await f
    #             if not status:
    #                 continue
    #
    #             if status == "finished":
    #
    #                 is_download = True


def generate_report(scan_id, apikey, baseurl):
    generate_component_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/library-versions/generate/" % scan_id
    )
    generate_vulnerability_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/issues/generate/" % scan_id
    )
    generate_licenses_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/licenseissues/generate/" % scan_id
    )
    generate_list = [
        generate_component_url,
        generate_vulnerability_url,
        generate_licenses_url,
    ]
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }

    for generate_url in generate_list:
        response = requests.post(generate_url, headers=headers)
        if response.status_code not in [200, 201]:
            error_exit("failed to generate report")
        logger.info(f"Starting generate report...")
        time.sleep(5)


def generate_remediation_report(baseurl, apikey, scan_id, output_folder):
    logger.info("Start generating remediation report...")
    scan_issue_list = get_scan_issue_list(baseurl, apikey, scan_id)
    with open(
        os.path.join(output_folder, f"scan-{scan_id}-remediation-report.csv"),
        "w",
        newline="",
    ) as f:
        header = [
            "scan_issue_id",
            "source_version",
            "remediation_version",
            "patch_version",
        ]
        writer = csv.writer(f)
        writer.writerow(header)
        for scan_issue in scan_issue_list:
            scan_issue_info = get_scan_issue_detail(baseurl, apikey, scan_issue["id"])
            line = [
                scan_issue_info["id"],
                scan_issue_info["library_version"],
                scan_issue_info["recommendation"]["fixed_library_version"]
                if scan_issue_info["recommendation"]
                else "",
                scan_issue_info["fixed_library_version"]["version_number"]
                if scan_issue_info["fixed_library_version"]
                else "",
            ]
            writer.writerow(line)
    logger.info(f"Successfully generating remediation report in {output_folder}...")


def download_report(scan_id, apikey, baseurl, report_format, output_path=None):
    download_component_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/library-versions/export/" % scan_id
    )
    download_vulnerability_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/issues/export/" % scan_id
    )
    download_licenses_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/licenseissues/export/" % scan_id
    )
    download_dict = {
        "component": download_component_url,
        "vulnerability": download_vulnerability_url,
        "licenses": download_licenses_url,
    }
    length = len(download_dict)

    header = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    query = {"report_format": report_format, "language": "english"}

    while length > 0:
        for key, url in download_dict.items():
            if url == "finished":
                continue

            download_link = check_generate(url, header, query)

            if not download_link:
                time.sleep(5)
                continue

            length -= 1
            download_dict[key] = "finished"

            response = requests.get(download_link)

            if response.status_code == 200:
                with open(
                    os.path.join(
                        output_path,
                        f"scan-{scan_id}-{key}.csv"
                        if report_format == "csv"
                        else f"scan-{scan_id}-{key}.pdf",
                    ),
                    "wb",
                ) as f:
                    f.write(response.content)
    logger.info(f"Successful download scan report!")


def check_generate(url, header, query):
    response = requests.get(url, headers=header, params=query)
    if response.status_code not in [200, 201]:
        return None

    download_link = response.json()["download_link"]
    return download_link
