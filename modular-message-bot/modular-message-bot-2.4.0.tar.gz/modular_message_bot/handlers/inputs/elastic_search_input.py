"""
# Elastic Search Input Module
You can query Elastic Search and preform a search query. This is a wrapper around
https://elasticsearch-py.readthedocs.io/en/7.10.0/api.html?highlight=search#elasticsearch.Elasticsearch.search
For example you could push the output to Slack

jq-vars test:
`cat tests/component-resources/response-elasticsearch.json | jq -r ". | .hits.hits
| map([._source.\"@timestamp\", ._source.docker.message] | join(\" - \")) | join(\"\n\")"`

Example Input:
```yaml
- code: elasticsearch
  parameters:
    connection:
      hosts:
        - host: "testelk"
          port: 9200
      http_auth:
        - "elastic"
        - "changeme"
    search:
      index: "docker-logs-*"
      q: "docker.message: error AND NOT docker.container_id: 81f0bb3014f1"
    jq-vars:
      number: ". | .hits.hits | length"
      details: ". | .hits.hits | map([._source.\"@timestamp\", ._source.docker.message] | join(\" - \")) | join(\"\n\")"
```
"""
from elasticsearch import Elasticsearch

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job import JobConfigSection
from modular_message_bot.models.job_run import JobRunVarCollection
from modular_message_bot.utils.jq_util import jq_filter_data


class ElasticSearchInput(AbstractSimpleInputHandler):
    # https://github.com/elastic/examples/tree/master/Miscellaneous/docker/full_stack_example
    docs_search_param = (
        "https://elasticsearch-py.readthedocs.io/en/7.10.0/api.html?highlight=search"
        "#elasticsearch.Elasticsearch.search"
    )

    @classmethod
    def get_code(cls) -> str:
        return "elasticsearch"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' input"

        required_param_keys = {"search": f". See {self.docs_search_param}"}

        # Required parameters
        for required_param_key, additional_details in required_param_keys.items():
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}{additional_details}"

        return super().validate_job_config(job_config)

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        connection: dict = parameters.get("connection", {})
        search: dict = parameters["search"]
        jq_vars: dict = parameters.get("jq-vars", {})
        jq_var_join: str = parameters.get("jq-var-join", "")

        es = Elasticsearch(**connection)
        es_results = es.search(**search)

        # Filter data (JQ)
        for key, value in jq_filter_data(jq_vars, jq_var_join, es_results).items():
            job_run_vars_collection.interpolate(key, value, self.get_code())
