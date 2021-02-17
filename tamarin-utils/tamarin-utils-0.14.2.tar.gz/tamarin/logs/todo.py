from ..multiprocessing import Todo
from ..sentry.commands import SentryCommand
from ..elasticsearch.commands import ElasticSearchCommand
from .commands import ReportCommand
from ..lamagram.commands import LamagramCommand


class LogToDo(Todo):
    def __init__(self, response, status_code, index, doc, args, headers, params):
        sentry_cmd = SentryCommand(response, status_code)
        elastic_cmd = ElasticSearchCommand(response, status_code, index, doc, args, headers, params)
        report_cmd = ReportCommand(index, status_code, response)
        commands = [sentry_cmd, elastic_cmd, report_cmd]
        super(LogToDo, self).__init__(commands)


class LamagramToDo(Todo):
    def __init__(self, chat_id, text, status_code):
        lamagram_cmd = LamagramCommand(chat_id, text, status_code)
        commands = [lamagram_cmd]
        super(LamagramToDo, self).__init__(commands)
