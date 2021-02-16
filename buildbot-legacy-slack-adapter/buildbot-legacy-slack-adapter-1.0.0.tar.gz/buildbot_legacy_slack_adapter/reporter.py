from datetime import timezone

from twisted.internet import defer
from twisted.python import log
from buildbot import config
from buildbot.util import httpclientservice
from buildbot.util import service
from buildbot.process.results import statusToString
from buildbot.process.results import worst_status
from buildbot.reporters.http import HttpStatusPushBase


class SlackStatusPush(HttpStatusPushBase):

    name = "SlackStatusPush"

    def _get_worst_step(self, build):
        worst_result, worst_step = 0, 0
        for idx, step in enumerate(build['steps']):
            if worst_status(worst_result, step['results']) == step['results']:
                worst_result = step['results']
                worst_step = idx
        return build['steps'][worst_step]['number']

    def _get_error_log_url(self, build):
        return f"{build['url']}/steps/{self._get_worst_step(build)}/logs/stdio"

    def _datetime_to_timestamp(self, datetime):
        return int(datetime.replace(tzinfo=timezone.utc).timestamp())

    def _format_slack_notification(self, build):
        return {
            "attachments": [
                {
                    "color": "cc0000",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": (
                                    f"A builder experienced a failure (*"
                                    f"{statusToString(build['results'])}*)"
                                )
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Builder name*\n{build['builder']['name']}"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Error log*\n{self._get_error_log_url(build)}"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": (
                                        f"*Started on*\n<!date^"
                                        f"{self._datetime_to_timestamp(build['started_at'])}"
                                        f"^{{date_short}} at {{time}}|January 1st, 1900 at 0:01 AM>"
                                    )
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": (
                                        f"*Started on*\n<!date^"
                                        f"{self._datetime_to_timestamp(build['complete_at'])}"
                                        f"^{{date_short}} at {{time}}|January 1st, 1900 at 0:01 AM>"
                                    )
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def checkConfig(self, serverUrl, **kwargs):
        if not isinstance(kwargs.get('results'), (type(None), list)):
            config.error("results must be a list or None")
        HttpStatusPushBase.checkConfig(self, **kwargs)

    @defer.inlineCallbacks
    def reconfigService(self, serverUrl, results=None, **kwargs):
        yield HttpStatusPushBase.reconfigService(self, **kwargs)
        self.results = results
        self._http = yield httpclientservice.HTTPClientService.getService(
            self.master, serverUrl)

    @defer.inlineCallbacks
    def startService(self):
        yield service.BuildbotService.startService(self)

        startConsuming = self.master.mq.startConsuming
        self._buildCompleteConsumer = yield startConsuming(
            self.buildFinished,
            ('builds', None, 'finished'))

    def stopService(self):
        self._buildCompleteConsumer.stopConsuming()

    def filterBuilds(self, build):
        is_monitored_builder, is_monitored_result = True, True
        if self.builders is not None:
            is_monitored_builder = build['builder']['name'] in self.builders
        if self.results is not None:
            is_monitored_result = statusToString(build['results']) in self.results
        return is_monitored_builder and is_monitored_result

    @defer.inlineCallbacks
    def send(self, build):
        response = yield self._http.post("", json=self._format_slack_notification(build))
        if response.code != 200:
            log.msg("%s: unable to upload status: %s" %
                    (response.code, response.content))
