#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import os
import time
from datetime import datetime
from command_tool.utils.utils import (
    logger,
    error_exit,
    config,
    ScanType,
    zip_folder,
    get_upload_zip_file,
    debug_logger_level,
)
from command_tool.utils.user import show_user
from command_tool.utils.login import login, create_scantist_token
from command_tool.utils.project import show_projects, set_proj, get_proj_id
from command_tool.utils.scan import (
    scan_latest_version,
    scan_sourcecode,
    scan_upload_proj,
    get_scan_id,
)
from command_tool.utils.report import (
    get_report,
    check_scan,
    generate_remediation_report,
)
from command_tool.utils.scan_result import get_scan_summary

HELP_CONTENT = """
## Binary Scan
- scantist_cmd -t binary -f $local_file_path 

- optional parameter: 
        
        -r [csv|pdf|csv-remediation|pdf-remediation]: download scan report
        
        -v          : set the version of the project
        
        -n          : set the project name. if this parameter is null, will use file name as project name
        
        -j          : project id.
        
        -p          : report output path. Default path is current working directory.
        
file + version -> create new project, name by file.【if duplicate name project exist, will update the project】

file + version + project_name -> create new project, name by the project_name.

local_binary_file + version + project_id -> create new version of existing project.

project_id -> scan existing project.

## Source code scan
- scantist_cmd -t source_code -f $local_file_path 

- optional parameter :

        -r [csv|pdf|csv-remediation|pdf-remediation]: download scan report
        
        -p          : report output path. Default path is current working directory.
        
        -b          : trigger source code scan with bom-detect. Otherwise, upload file and remotely trigger build and scan.
         
## List user projects
- scantist_cmd -l


## Download scan result
Generate and download the most recent scan report if no $project_id given
- scantist_cmd -r [csv|pdf|csv-remediation|pdf-remediation]

- optional parameter:

        -j  : project id.
"""


def main():
    argv = sys.argv[1:]
    scan_type = ""
    local_file = ""
    version = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    opts = []
    list_projects = False
    report_format = ""
    args = []
    project_name = ""
    project_id = 0
    report_path = os.path.join(os.getcwd(), "report")
    is_bom_detect = False
    is_generate_remediation_report = False

    try:
        opts, args = getopt.getopt(
            argv,
            "hdblt:f:v:r:j:n:p:b:",
            [
                "scan_type=",
                "file_path=",
                "version=",
                "report_format=",
                "project_id=",
                "project_name=",
                "report_path=",
                "bom_detect=",
            ],
        )
    except Exception as e:
        error_exit(e)

    if len(args) == 0 and len(opts) == 0:
        logger.info(HELP_CONTENT)
        exit(0)

    for opt, arg in opts:
        if opt == "-h":
            logger.info(HELP_CONTENT)
            sys.exit()
        elif opt == "-d":
            debug_logger_level()
        elif opt in ("-t", "--scan_type"):
            scan_type = arg
        elif opt in ("-f", "--file"):
            local_file = arg
        elif opt in ("-v", "--version"):
            version = arg
        elif opt in ("-l", "--list_projects"):
            list_projects = True
        elif opt in ("-r", "--report"):
            if (
                arg != "csv"
                and arg != "pdf"
                and arg != "csv-remediation"
                and arg != "pdf-remediation"
            ):
                error_exit("Scan report only accept csv or pdf format.")
            report_format = arg.split("-")[0]
            if len(arg.split("-")) > 1:
                is_generate_remediation_report = True
        elif opt in ("-p", "--report_path"):
            report_path = arg
        elif opt in ("-j", "--project_id"):
            project_id = arg
        elif opt in ("-n", "--project_name"):
            project_name = arg
        elif opt in ("-b", "--bom_detect"):
            is_bom_detect = True

    baseurl = config.get("SCANTIST", "BASE_URL")
    scantist_token = config.get("SCANTIST", "SCANTIST_TOKEN")
    apikey = config.get("SCANTIST", "API_KEY")

    if not apikey or not baseurl:
        error_exit("Please using 'scantist_auth' command set up account first.")

    user_info = show_user(apikey, baseurl)
    logger.info(f"Hello! {user_info['user_name']}")

    # get apikey and scantist token
    if not scantist_token:
        logger.info("Generating scantist_token...")
        default_org_id = user_info["default_org"]
        scantist_token = create_scantist_token(apikey, baseurl, default_org_id)

    if list_projects:
        show_projects(apikey, baseurl)
        exit(0)

    scan_id = 0
    status = ""

    if scan_type:
        if scan_type == ScanType.BINARY:
            # Binary Scan
            if local_file:
                file = get_upload_zip_file(local_file)

                logger.info("Setting project info...")
                (project_id, project_name) = set_proj(
                    apikey, baseurl, project_id, project_name, file
                )
                logger.debug(f"project id: {project_id}, project name: {project_name}")
                (scan_id, project_id) = scan_upload_proj(
                    file, apikey, baseurl, version, ScanType.BINARY, project_id
                )
                logger.debug(f"project id: {project_id}, scan_id: {scan_id}")
            else:
                # scan the latest version if only provide project id
                if project_id:
                    logger.info(
                        "Only project id provided, will scan the latest version of the project."
                    )
                    (scan_id, project_id) = scan_latest_version(
                        apikey, baseurl, ScanType.BINARY, project_id
                    )
                    logger.debug(f"project id: {project_id}, scan_id: {scan_id}")
                else:
                    error_exit("Please provide either project id or file path.")
        elif scan_type == ScanType.SOURCE_CODE:
            if not local_file:
                error_exit("Missing required -f/--file. Please specify a file path.")

            # Source code bom_detect Scan and upload code scan
            if is_bom_detect:
                if not os.path.isdir(local_file):
                    error_exit(
                        "for bom_detect source code scan, please specify a valid folder path"
                    )

                scan_id = scan_sourcecode(local_file, scantist_token, baseurl)
            else:
                file = get_upload_zip_file(local_file)

                logger.info("Setting project info...")
                (project_id, project_name) = set_proj(
                    apikey, baseurl, project_id, project_name, file
                )

                (scan_id, project_id) = scan_upload_proj(
                    file, apikey, baseurl, version, ScanType.SOURCE_CODE, project_id
                )
            project_id = get_proj_id(apikey, baseurl, scan_id)

        percentage = 0
        while status != "finished" and status != "failed":
            status, scan_percentage = check_scan(scan_id, project_id, apikey, baseurl)
            if scan_percentage and scan_percentage != percentage:
                percentage = scan_percentage
                logger.info("scan percentage: " + str(percentage) + "%")
            time.sleep(5)
        logger.info(f"Scan {scan_id} completed!")

    # project_id does not exist in source code scan
    # scan_sourcecode finish means scan finish, no need to check scan status, thus no need project id.
    if (scan_type and report_format and status == "finished") or (
        not scan_type and report_format
    ):
        output_folder = os.path.join(
            report_path,
            os.path.splitext(os.path.basename(local_file))[0]
            if os.path.isfile(local_file)
            else os.path.basename(local_file) + "-report",
        )
        logger.info(f"report output folder: {output_folder}")

        if not os.path.exists(report_path):
            os.mkdir(report_path)

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        if scan_type:
            get_report(
                scan_id,
                apikey,
                baseurl,
                report_format,
                output_folder,
                project_id if project_id else None,
            )
            if is_generate_remediation_report:
                generate_remediation_report(baseurl, apikey, scan_id, output_folder)
        else:
            # download report for the latest scan
            logger.info("Getting the most recent scan id...")
            scan_id = get_scan_id(apikey, baseurl, project_id)
            logger.info(f"Generalize report for scan {scan_id}")
            get_report(scan_id, apikey, baseurl, report_format, output_folder)

    if status == "finished":
        get_scan_summary(scan_id, apikey, baseurl)
    elif status == "failed":
        logger.info(f"Scan Failed! Please check details on Scantist website")
