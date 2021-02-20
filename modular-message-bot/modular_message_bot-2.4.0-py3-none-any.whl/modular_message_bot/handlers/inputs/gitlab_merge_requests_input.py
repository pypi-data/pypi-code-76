"""
# Gitlab Pull Requests Input Module
Calls Gitlab looking for merge requests for a list of projects
This is a wrapper around https://docs.gitlab.com/ee/api/merge_requests.html#list-project-merge-requests

jq-vars test:
`cat tests/component-resources/response-gitlab-merge-requests-23648575.json | jq -r ". | map([.web_url] | join(\"\"))
| join(\"\n\")"`

Example Simple Input:
```yaml
- code: gitlab_merge_requests
  parameters:
    project-ids:
      - 23648646 # public - 0 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-0
      - 23648520 # public - 1 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-1
      - 23648575 # public - 2 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-2
    request-args:
      headers:
        PRIVATE-TOKEN: "$[GITLAB_TOKEN]"
    jq-vars:
      pr_count: "length"
      pr_details: ". | map([.web_url] | join(\"\")) | join(\"\n\")"
```

Example Advanced Input:
```yaml
- code: gitlab_merge_requests
  parameters:
    url: https://gitlab.example.com/api
    project-ids:
      - 23648646 # public - 0 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-0
      - 23648520 # public - 1 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-1
      - 23648575 # public - 2 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-2
    get:
      state: opened
    request-args:
      headers:
        PRIVATE-TOKEN: "$[GITLAB_TOKEN]"
    jq-vars:
      pr_count: "length"
      pr_details: ". | map([.references.full, \" - \", .title, \" - by \", .author.name, \" - \", .web_url]
       | join(\"\")) | join(\"\n\")"
    jq-var-join: ""
```
"""

import logging
from urllib.parse import urlencode

from requests import get as requests_get

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVarCollection
from modular_message_bot.utils.jq_util import jq_filter_data

logger = logging.getLogger(__name__)


class GitlabMergeRequestsInput(AbstractSimpleInputHandler):
    url = "https://gitlab.com/api"

    @classmethod
    def get_code(cls) -> str:
        return "gitlab_merge_requests"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        url_prefix = parameters.get("url", self.url)
        get_params = parameters.get("get", {"state": "opened"})
        request_args = parameters.get("request-args", {})
        jq_vars = parameters.get("jq-vars", {})
        jq_var_join = parameters.get("jq-var-join", "")
        project_ids = parameters.get("project-ids", [])

        # Loop repos and have a look for open PRs
        responses = []
        for project_id in project_ids:
            url = f"{url_prefix}/v4/projects/{project_id}/merge_requests?{urlencode(get_params)}"
            response = requests_get(url, **request_args)
            if response.status_code != 200:
                raise Exception(f"{self.get_code()} failed '{str(response.status_code)}'\n'{str(response.content)}'")
            responses += response.json()
        logger.debug(f"{self.get_code()} found {len(responses)} total responses")

        # Filter data (JQ)
        for key, value in jq_filter_data(jq_vars, jq_var_join, responses).items():
            job_run_vars_collection.interpolate(key, value, self.get_code())
