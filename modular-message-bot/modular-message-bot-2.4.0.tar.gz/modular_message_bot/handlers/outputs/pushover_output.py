"""
# Pushover Output Module
Sends notifications to Pushover. This module is very similar to the docs (https://pushover.net/api)
Feature Maturity Status: Alpha
Note: We need to implement more features to be nicer to their API such as rate limiting the output. See:

Example Simple Output:
```yaml
- code: pushover
  parameters:
    token: "azGDORePK8gMaC0QOYAMyEEuzJnyUi"
    user: "uQiRzpo4DXghDmr9QzzfQu27cmVRsG"
    message: "Hello World!!!"
```

Example Advanced Output:
```yaml
- code: pushover
  parameters:
    token: "azGDORePK8gMaC0QOYAMyEEuzJnyUi"
    user: "uQiRzpo4DXghDmr9QzzfQu27cmVRsG"
    message: "Hello World!!!"
    device: droid2
    title: "Direct message from @someuser"
    url: "twitter://direct_message?screen_name=someuser"
    url_title: "Reply to @someuser"
    priority: "1"
    sound: incoming
    timestamp: "1331249662"
```

"""
import logging

from requests import post as request_post

from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractSimpleOutputHandler
from modular_message_bot.models.job import JobConfigSection

logger = logging.getLogger(__name__)


class PushoverOutput(AbstractSimpleOutputHandler):
    send_url = "https://api.pushover.net/1/messages.json"
    validation_url = "https://api.pushover.net/1/users/validate.json"
    docs_link = "https://pushover.net/api"
    required_parameter_keys = ["token", "user", "message"]
    optional_parameter_keys = [
        # "attachment",
        "device",
        "title",
        "url",
        "url_title",
        "priority",
        "sound",
        "timestamp",
    ]

    @classmethod
    def get_code(cls) -> str:
        return "pushover"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' output. Please see {self.docs_link}"
        for required_param_key in self.required_parameter_keys:
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}"
        return super().validate_job_config(job_config)

    def get_send_parameters(self, parameters: dict):
        send = {}
        for required_parameter_key in self.required_parameter_keys:
            send[required_parameter_key] = parameters.get(required_parameter_key)
        for optional_parameter_key in self.optional_parameter_keys:
            if optional_parameter_key in parameters.keys():
                send[optional_parameter_key] = parameters[optional_parameter_key]
        return send

    def run_output(self, parameters: dict):
        # Settings
        send = self.get_send_parameters(parameters)
        headers = {"Content-Type": "application/json"}
        logger.info("Sending pushover request")
        result = request_post(self.send_url, headers=headers, json=send)

        if str(result.status_code) != "200":
            raise Exception(f"ERROR: Response failure {str(result.status_code)}\n{str(result.content)}")
