from modular_message_bot.config.config_collection import ConfigCollection
from modular_message_bot.string_interpolator import StringInterpolator


class ConfigInterpolator(object):
    def __init__(
        self, dynamic_config_string_interpolator: StringInterpolator, config: ConfigCollection,
    ):
        self.string_interpolator = dynamic_config_string_interpolator
        self.config = config

    def interpolate(self, contents: str) -> str:
        content_keys = self.string_interpolator.get_keys(contents)
        config_keys = self.config.get_keys()
        for content_key in content_keys:
            if content_key in config_keys:
                replacement = self.config.get_or_fail(content_key)
                contents = self.string_interpolator.interpolate(contents, content_key, replacement)
        return contents

    def interpolate_item(self, item):
        if isinstance(item, dict):
            return self.interpolate_dict(item)
        if isinstance(item, list):
            return self.interpolate_list(item)
        if isinstance(item, str):
            return self.interpolate(item)
        return item

    def interpolate_list(self, items: list) -> list:
        interpolated_items = []
        for item in items:
            interpolated_items.append(self.interpolate_item(item))
        return interpolated_items

    def interpolate_dict(self, dictionary: dict) -> dict:
        interpolated_dict = {}
        for key, value in dictionary.items():
            interpolated_dict[self.interpolate_item(key)] = self.interpolate_item(value)
        return interpolated_dict
