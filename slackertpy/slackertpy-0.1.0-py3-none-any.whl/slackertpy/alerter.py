import json
import requests
from typing import Dict
import logging

from slackertpy.level import Level

logging.basicConfig(level=logging.ERROR)


class Alerter:
    def __init__(self, webhook_url: str, level: Level = Level.INFO):
        self.url = webhook_url
        self._level = level

    def set_level(self, level: Level) -> None:
        self._level = level

    def debug(self, content: Dict) -> None:
        if self._level < Level.DEBUG:
            return

        self._post_to_slack(content)

    def info(self, content: Dict) -> None:
        if self._level < Level.INFO:
            return

        self._post_to_slack(content)

    def error(self, content: Dict) -> None:
        self._post_to_slack(content)

    def _post_to_slack(self, content):
        if not content:
            raise ValueError("Message content cannot be empty.")

        headers = {'Content-Type': 'application/json'}
        data = json.dumps(content)
        r = requests.post(self.url, headers=headers, data=data)
        if r.status_code != 200:
            print(f"Slack message sending unsuccessful (Code {r.status_code}, "
                  f"Message {r.text}).")
