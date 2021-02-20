from modular_message_bot.config.config_collection import DictConfigProvider
from modular_message_bot.config.constants import LOCALE_ALL, SCHEDULER_TIMEZONE_CFG_KEY


def build_default_config(priority: int) -> DictConfigProvider:
    # fmt: off
    config = {
        SCHEDULER_TIMEZONE_CFG_KEY: "utc",
        LOCALE_ALL: "en_US.utf8"
    }
    # fmt: on
    return DictConfigProvider(config, "Default config dict provider", priority)
