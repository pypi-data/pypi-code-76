import os
import logging
import configparser
from functools import cached_property

import discord

dbb_logger = logging.getLogger("discord-base-bots")
logging.getLogger("discord-base-bots").addHandler(logging.NullHandler())
# To turn off logging: logging.getLogger("discord-base_bots").propagate = False


class BaseBot(discord.Client):

    bot_name = None
    hot_word = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # command string: function object
        # "roll": self.roll
        self.commands = {
            "reload": self.__load_config,
            "help": self.help
        }

        self.__load_config()

    def update_commands(self, commands):
        self.commands.update(commands)

    @cached_property
    def config(self):
        config = configparser.ConfigParser()
        config.read('bot.ini')
        return config

    async def __load_config(self, *args):
        """Reload the bots config.

        Ensure that hotwords are reloaded, then calls users fucntionality.
        """
        self.configure_hot_words(self.config.hot_words.split(","))
        self.load_config()

    def __configure_hot_words(self, hot_words):
        """Set a list of hot words

        Args:
            hot_words (list): the hot words to set.
        """
        self.hot_words = hot_words
        self.hot_words.extend([self.bot_name, self.hot_word])

    async def on_ready(self):
        dbb_logger.debug(f'{self.bot_name} online')

    async def on_message(self, message):
        """Gets messages and filters for this bot, activates response if available."""
        active = False
        for word in self.hot_words:
            if message.content.lower().strip("@").startswith(word.lower()):
                active = True
                break
        if active:
            activation_phrase, command_and_data = message.content.split(sep=None, maxsplit=1)
            command = None
            command_content = None
            for command_name, command_func in self.commands.items():
                if command_and_data.lower().startswith(command_name):
                    command = command_func
                    command_content = command_and_data.split(command_name, maxsplit=1)[-1].strip()
                    break
            if command is not None:
                try:
                    await command(command_content, message)
                except Exception as e:
                    dbb_logger.exception("Failed executing command")

    async def help(self, command, message):
        """Provide help to users wanting to use this bot."""
        await message.channel.send(f"Hot words to activate this bot: {', '.join(self.hot_words)}")
        await message.channel.send(f"Available commands: {', '.join(self.commands.keys())}")

    def load_config(self):
        """Load config values and do stuff with them.

        This method is called when the bot is initialized and when you ask it to reload it's config via chat.
        """
        pass


def run_bot(bot_class, dotenv_path=None):
    if dotenv_path:
        if os.path.exists(dotenv_path):
            import dotenv
            dotenv.load_dotenv(dotenv_path=dotenv_path)
        else:
            raise ValueError(f"{dotenv_path} file not found")

    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("DISCORD_TOKEN not found in environment variables")

    intents = discord.Intents.default()
    intents.members = True

    client = bot_class(intents=intents)
    client.run(token)


if __name__ == "__main__":
    from pathlib import Path

    class SimpleBot(BaseBot):
        bot_name = "SimpleBot"
        hot_word = "simplebot"

    run_bot(SimpleBot, Path(".env").resolve())
