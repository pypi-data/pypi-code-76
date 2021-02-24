import json
import shutil
import time
from datetime import datetime, timezone
from fnmatch import fnmatch
from typing import List, BinaryIO, Dict

import confuse
import dateutil.parser
import requests
import timeago
import typer
from requests import Response
from requests.exceptions import HTTPError

from cci_cli.circle.exceptions import CircleCIException
from cci_cli.circle.workflow import SuccessStates, ErrorStates
from cci_cli.common import utils


class CircleCI:
    def __init__(self):
        try:
            config = utils.read_config()

            self.vcs = str(config["vcs"])
            self.organization = str(config["organization"])
            self.api_token = str(config["circle_token"])
        except confuse.ConfigError:
            utils.exit_cli(
                "Run `cci config setup ...` before trying to use the CLI.",
                status_code=1,
            )

        self.base_url = "https://circleci.com/api/v2"
        self.project_slug = f"project/{self.vcs}/{self.organization}"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Circle-Token": self.api_token,
        }

    def _get_request(self, url: str):
        response = requests.get(
            url=url,
            headers=self.headers,
        )
        self._raise_for_status_and_log_error_message(response)
        return response.json()

    def _post_request(self, url: str, params: dict):
        response = requests.post(
            url=url,
            json=params,
            headers=self.headers,
        )
        self._raise_for_status_and_log_error_message(response)
        return response.json()

    @staticmethod
    def _raise_for_status_and_log_error_message(response: Response):
        try:
            response.raise_for_status()
        except HTTPError:
            message = response.json().get("message")
            if message:
                typer.echo(f"Error message: {message}")
            raise

    def download_request(self, url: str, output_file: BinaryIO):
        with requests.get(url=url, headers=self.headers, stream=True) as response:
            total_bytes = response.headers["Content-Length"]
            yield 0, total_bytes
            shutil.copyfileobj(response.raw, output_file)
        yield total_bytes, total_bytes

    def list_pipelines(
        self, project_name: str, branch: str = None, after_pipeline_id: str = None
    ):
        url = f"{self.base_url}/{self.project_slug}/{project_name}/pipeline"
        if branch is not None:
            url += f"?branch={branch}"
        response = self._get_request(url)
        pipelines_list = response.get("items", list())
        output = []
        for pipeline in pipelines_list:
            pipeline_id = pipeline.get("id")
            # when after_pipeline_id is None this check is always False
            if pipeline_id == after_pipeline_id:
                break
            state = pipeline.get("state")
            branch = pipeline.get("vcs").get("branch")
            trigger_type = pipeline.get("trigger", {}).get("type")
            trigger_actor = pipeline.get("trigger", {}).get("actor", {}).get("login")
            project_slug = pipeline.get("project_slug")
            created_at = dateutil.parser.parse(pipeline.get("created_at"))
            created_time_ago = timeago.format(created_at, datetime.now(timezone.utc))
            url = f"https://app.circleci.com/pipelines/{project_slug}"
            output.append(
                [
                    pipeline_id,
                    created_time_ago,
                    state,
                    trigger_type,
                    trigger_actor,
                    branch,
                    url,
                ]
            )
        return output

    def _get_latest_pipeline(self, project_name):
        url = f"{self.base_url}/{self.project_slug}/{project_name}/pipeline"
        response = self._get_request(url)
        pipelines_list = response.get("items", list())
        return pipelines_list[0]

    def _get_pipeline_by_number(self, project_name, pipeline_number):
        url = f"{self.base_url}/{self.project_slug}/{project_name}/pipeline/{pipeline_number}"
        response = self._get_request(url)
        return response

    def read_artifacts_by_job_number(
        self, project_name, job_number, *artifact_patterns
    ):
        url = (
            f"{self.base_url}/{self.project_slug}/{project_name}/{job_number}/artifacts"
        )
        response = self._get_request(url)
        artifacts_list = response.get("items", list())
        output = []
        for artifact in artifacts_list:
            node_index = artifact.get("node_index")
            path = artifact.get("path")
            url = artifact.get("url")
            if not artifact_patterns or any(
                fnmatch(path, pattern) for pattern in artifact_patterns
            ):
                output.append([node_index, path, url])
        return output

    def read_pipeline_artifacts(self, pipeline_id, *artifact_patterns):
        workflows = self.get_workflows(pipeline_id)
        output = []
        for workflow in workflows:
            workflow_id = workflow.get("id")
            jobs = self.get_workflow_jobs(workflow_id)
            for job in jobs:
                job_number = job.get("job_number")
                if not job_number:
                    # Not started, error, etc.
                    continue
                job_name = job.get("name")
                project_name = job.get("project_slug").split("/")[-1]
                output.extend(
                    [
                        [job_name, job_number] + item
                        for item in self.read_artifacts_by_job_number(
                            project_name, job_number, *artifact_patterns
                        )
                    ]
                )
        return output

    def trigger(
        self, project_name: str, branch: str, tag: str = "", parameters: dict = None
    ):
        url = f"{self.base_url}/{self.project_slug}/{project_name}/pipeline"
        params = dict()
        if branch:
            params.update({"branch": branch})
        if tag:
            params.update({"tag": tag})
        if parameters is not None:
            params.update({"parameters": parameters})

        return self._post_request(url, params=params)

    def get_workflow(self, workflow_id: str) -> Dict:
        url = f"{self.base_url}/workflow/{workflow_id}"
        return self._get_request(url=url)

    def get_workflow_jobs(self, workflow_id: str) -> List:
        url = f"{self.base_url}/workflow/{workflow_id}/job"
        jobs = self._get_request(url=url)
        return jobs.get("items", [])

    def get_workflows(self, pipeline_id: str) -> List:
        url = f"{self.base_url}/pipeline/{pipeline_id}/workflow"
        workflows = self._get_request(url=url)
        return workflows.get("items", [])

    def approve_workflow(self, workflow_id: str, approval_request_id: str) -> Dict:
        url = f"{self.base_url}/workflow/{workflow_id}/approve/{approval_request_id}"
        return self._post_request(url=url, params={})

    def cancel_workflow(self, workflow_id: str) -> Dict:
        url = f"{self.base_url}/workflow/{workflow_id}/cancel"
        return self._post_request(url=url, params={})

    def rerun_workflow(self, workflow_id: str) -> Dict:
        url = f"{self.base_url}/workflow/{workflow_id}/rerun"
        return self._post_request(url=url, params={})

    @classmethod
    def get_workflow_url(cls, workflow):
        workflow_id = workflow["id"]
        pipeline_number = workflow["pipeline_number"]
        project_slug = workflow["project_slug"].replace("gh/", "github/").strip("/")
        return f"https://app.circleci.com/pipelines/{project_slug}/{pipeline_number}/workflows/{workflow_id}"

    def wait_for_workflows_creation(self, pipeline_id: str, timeout: int):
        now = time.time()
        timeout = now + (timeout * 60)
        workflows = []
        while time.time() <= timeout and len(workflows) == 0:
            workflows = self.get_workflows(pipeline_id)
            if len(workflows) > 0:
                break
            utils.show_progress()
            time.sleep(2)
        else:
            utils.exit_cli(
                "Timeout was reached. No workflow has started.", status_code=1
            )
        return workflows

    def wait_for_workflows_completion(self, pipeline_id: str, timeout: int):
        now = time.time()
        timeout = now + (timeout * 60)
        while time.time() <= timeout:
            workflows = self.get_workflows(pipeline_id)
            workflow_status = [workflow.get("status", None) for workflow in workflows]
            successful_workflows = list(
                map(lambda status: status in SuccessStates, workflow_status)
            )
            error_workflows = list(
                map(lambda status: status in ErrorStates, workflow_status)
            )
            if len(workflows) > 0 and all(successful_workflows):
                print(json.dumps(workflows, indent=4, sort_keys=True))
                utils.exit_cli(
                    "All workflows have successfully finished.", status_code=0
                )
            if len(workflows) > 0 and any(error_workflows):
                print(json.dumps(workflows, indent=4, sort_keys=True))
                utils.exit_cli(
                    "A workflow has finished with an error state.", status_code=1
                )
            utils.show_progress()
            time.sleep(2)
            continue
        else:
            utils.exit_cli("Timeout was reached.", status_code=1)

    def approve_on_hold_jobs(self, workflow_id: str):
        try:
            jobs = self.get_workflow_jobs(workflow_id)
        except HTTPError as e:
            raise CircleCIException(repr(e)) from e

        try:
            approval_request_id = next(
                job["approval_request_id"]
                for job in jobs
                if job["type"] == "approval" and job["status"] == "on_hold"
            )
        except StopIteration:
            raise CircleCIException("Error: No on_hold approval job found for workflow")

        self.approve_workflow(workflow_id, approval_request_id)
