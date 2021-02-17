from tamarin.command import Command
from .bot import Bot
from sentry_sdk import capture_exception
from .utils.functions import validate_status


class LamagramCommand(Command):
    def __init__(self, chat_id, text, status_code):
        super(LamagramCommand, self).__init__()
        self.chat_id = chat_id
        self.text = text
        self.status = status_code

    def execute(self):
        if validate_status(status_code=self.status):
            try:
                bot = Bot.get_instance()
                bot.send_code(self.chat_id, self.text)
            except Exception as e:
                capture_exception(e)
