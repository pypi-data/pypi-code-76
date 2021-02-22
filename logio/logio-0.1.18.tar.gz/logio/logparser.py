# -*- coding: utf-8 -*-
from io import open
import re
import json
import copy
import datetime
import logging
from .rules import get_default_rules
from .rules import expend_vars

logger = logging.getLogger(__name__)

LOG_PARSER_TYPES = {}

def register_parser_type(name, klass):
    LOG_PARSER_TYPES[name] = klass

def unregister_parser_type(name):
    del LOG_PARSER_TYPES[name]

def get_parser_class(name):
    return LOG_PARSER_TYPES.get(name, None)

LOG_TRANSFORMERS = {}

def register_transformer_type(name, klass):
    LOG_TRANSFORMERS[name] = klass

def unregister_transformer_type(name):
    del LOG_TRANSFORMERS[name]

def get_transformer_class(name):
    return LOG_TRANSFORMERS.get(name, None)

class LogParser(object):

    def __init__(self, settings):
        self.settings = settings or {}
        # properties
        self.keep_not_matched_lines = self.settings.get("keeep-not-matched-lines", "") or ""
        self.transforms = self.settings.get("transforms", []) or []

    def do_keep_not_matched_line(self, info):
        with open(self.keep_not_matched_lines, "a", encoding="utf-8") as fobj:
            fobj.write(u"{0}\n".format(info["_line"]))
        logger.warn(u"Parse line failed: {0}".format(info["_line"]))

    @classmethod
    def init(cls, settings):
        parser_type = settings.get("type", "regex")
        parser_class = get_parser_class(parser_type)
        if not parser_class:
            return None
        return parser_class(settings)

    def line_handler(self, line):
        info = self.parse_line(line)
        if self.transforms:
            self.do_transform(info)
        return info

    def parse_line(self, line):
        return {
            "_line": line,
        }

    def do_transform(self, data):
        for transform_settings in self.transforms:
            try:
                field = transform_settings.get("field", None)
                transform_type = transform_settings.get("type", None)
                if transform_type:
                    transformer_class = get_transformer_class(transform_type)
                    if transformer_class:
                        data[field] = transformer_class(transform_settings).do_transform(data, field)
            except Exception:
                logger.exception("do transform failed.")

class Transformer(object):
    def __init__(self, settings):
        self.settings = settings or {}

    def do_transform(self, data, key):
        return data[key]

class StrftimeTransformer(Transformer):

    def __init__(self, settings):
        super().__init__(settings)
        self.strptime_template = self.settings.get("strptime", "%Y-%m-%d %H:%M:%S")
        self.strftime_template = self.settings.get("strftime", "%Y-%m-%d %H:%M:%S")
        self.use_timestamp = self.settings.get("timestamp", False)
    
    def do_transform(self, data, field):
        value = data[field]
        value = datetime.datetime.strptime(value, self.strptime_template)
        if self.use_timestamp:
            return value.timestamp()
        else:
            return value.strftime(self.strftime_template)

class Str2Number(Transformer):

    def __init__(self, settings):
        super().__init__(settings)

    def do_transform(self, data, field):
        value = data[field]
        if "." in value:
            return float(value)
        else:
            return int(value)

class ForceInt(Transformer):
    def do_transform(self, data, field):
        value = data[field]
        return int(value)

class ForceFloat(Transformer):
    def do_transform(self, data, field):
        value = data[field]
        return float(value)

class FormulaCompute(Transformer):

    def __init__(self, settings):
        super().__init__(settings)
        self.formula = self.settings.get("formula", "0")

    def do_transform(self, data, field):
        from sympy import sympify
        formula = self.formula.format(**data)
        return sympify(formula)

class JsonParser(LogParser):
    def parse_line(self, line, keep_not_matched_lines=None):
        try:
            data = json.loads(line)
            if isinstance(data, dict):
                data["_matched"] = True
            else:
                data = {
                    "_data": data,
                    "_matched": False,
                }
        except json.JSONDecodeError:
            data = {}
            data["_matched"] = False
        data["_line"] = line
        return data

class RegexParser(LogParser):
    
    def __init__(self, settings):
        super(RegexParser, self).__init__(settings)
        # properties
        self.use_default_rules = self.settings.get("use-default-rules", True)
        self.rules = self.get_rules()
        self.matches = self.get_matches()


    def get_rules(self):
        rule_map = {}
        if self.use_default_rules:
            rule_map.update(get_default_rules())
        rule_map.update(self.settings.get("rules", {}) or {})
        return expend_vars(rule_map)

    def get_matches(self):
        raw_matches = self.settings.get("matches", {})
        rule_map = copy.copy(self.rules)
        rule_map.update(raw_matches)
        rule_map = expend_vars(rule_map)
        match_items = []
        for match_name in raw_matches.keys():
            match_pattern = rule_map[match_name]
            match_items.append((match_name, match_pattern))
        return match_items

    def parse_line(self, line, keep_not_matched_lines=None):
        if keep_not_matched_lines is None:
            keep_not_matched_lines = self.keep_not_matched_lines
        data = {
            "_line": line,
        }
        matched = False
        if self.matches:
            for match_name, match_pattern in self.matches:
                try:
                    match = re.match(match_pattern, line)
                    if match:
                        matched = True
                        data["_matched_name"] = match_name
                        data.update(match.groupdict())
                        break
                except Exception as err:
                    msg = u"Error: regex match failed, match_name={0}，match_pattern={1}，error={2}。".format(
                        match_name,
                        match_pattern,
                        str(err),
                    )
                    logger.error(msg)
                    raise err
        data["_matched"] = matched
        if not matched and keep_not_matched_lines:
            self.do_keep_not_matched_line(data)
        return data


register_transformer_type("strftime", StrftimeTransformer)
register_transformer_type("str2number", Str2Number),
register_transformer_type("formula", FormulaCompute)
register_transformer_type("int", ForceInt)
register_transformer_type("float", ForceFloat)

register_parser_type("regex", RegexParser)
register_parser_type("json", JsonParser)
