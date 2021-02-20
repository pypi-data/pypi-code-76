"""
# Github PR Input Module
Calls Github looking for Pulls (PRs) for a list of repositories
This is a wrapper around https://docs.github.com/en/free-pro-team@latest/rest/reference/pulls

jq-vars test:
`cat tests/component-resources/response-github-pr-jeremy-test-org-2---test-repo-2a.json
 | jq -r ". | map([.html_url] | join(\"\")) | join(\"\n\")"`

Example Simple Input:
```yaml
- code: github_prs
  parameters:
    auth-user: $[GITHUB_COM_USERNAME]
    auth-token: $[GITHUB_COM_TOKEN]
    repos:
      - group-name/repository-one
      - group-name/repository-two
      - group-name/repository-three
      - group-name/repository-four
    jq-vars:
      pr_details: ". | map([.html_url] | join(\"\")) | join(\"\n\")"
```

Example Advanced Input:
```yaml
- code: github_prs
  parameters:
    auth-user: $[GITHUB_COM_USERNAME]
    auth-token: $[GITHUB_COM_TOKEN]
    repos:
      - jeremy-test-org-1/test-repo-1a
      - jeremy-test-org-1/test-repo-1b
      - jeremy-test-org-2/test-repo-2a
      - jeremy-test-org-2/test-repo-2b
    get:
      state: open
    headers:
       Something: Else
    jq-vars:
      pr_count: "length"
      pr_details: ". | map([.head.repo.full_name, \" - \", .title, \" - by \", .user.login, \" - \", .html_url]
       | join(\"\")) | join(\"\n\")"
    jq-var-join: ""
```
"""
import logging
from urllib.parse import urlencode

from requests import get as requests_get
from requests.auth import HTTPBasicAuth

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVarCollection
from modular_message_bot.utils.jq_util import jq_filter_data

logger = logging.getLogger(__name__)


class GithubPrsInput(AbstractSimpleInputHandler):
    url = "https://api.github.com"

    @classmethod
    def get_code(cls) -> str:
        return "github_prs"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        url_prefix = parameters.get("url", self.url)
        get_params = parameters.get("get", {"state": "open"})
        jq_vars = parameters.get("jq-vars", {})
        jq_var_join = parameters.get("jq-var-join", "")
        auth_user = parameters.get("auth-user", "")
        auth_token = parameters.get("auth-token", "")
        repos = parameters.get("repos", [])
        headers = parameters.get("headers", {})

        # Loop repos and have a look for open PRs
        responses = []
        headers["Accept"] = "application/vnd.github.v3+json"
        args = {"headers": headers}
        if auth_user != "" or auth_token != "":
            args["auth"] = HTTPBasicAuth(auth_user, auth_token)
        for repo in repos:
            url = f"{url_prefix}/repos/{repo}/pulls?{urlencode(get_params)}"
            response = requests_get(url, **args)
            if response.status_code != 200:
                raise Exception(f"{self.get_code()} failed '{str(response.status_code)}'\n'{str(response.content)}'")
            responses += response.json()
        logger.debug(f"{self.get_code()} found {len(responses)} total responses")

        # Filter data (JQ)
        for key, value in jq_filter_data(jq_vars, jq_var_join, responses).items():
            job_run_vars_collection.interpolate(key, value, self.get_code())
