from schema import Schema, And, Or, Use, Optional
from typing import Any, Dict, List
from datetime import datetime
from dateutil import parser

is_datetime_string = lambda date: isinstance(parser.parse(date), datetime)

def validate_datapackage_minimal(package: Dict):

    package_schema = Schema({
        'title': And(str, len),
        Optional('license'): And(str, len),
        Optional('description'): And(str, len),
        Optional('author'): And(str, len),
        Optional('issued'): And(Use(is_datetime_string)),
        Optional("modified"): And(Use(is_datetime_string)),
        Optional("language"): Or(str,[str]),
        Optional('keywords'): Or(str,[str]),
        Optional("keyword"): Or(str,[str]),
        Optional("publisher"): object,
        Optional("distribution"): [object],
        Optional("type"): str,
        Optional("theme"): str,
        Optional("team"): str,
        Optional("identifier"): str,
        Optional("landingPage"): str
        })

    return   Schema(package_schema).validate(package)

def validate_datapackage_dcat2(package: Dict):

    package_schema = Schema({
        'title': And(str, len),
        'description': And(str, len),
        'issued': And(Use(is_datetime_string)),
        "modified": And(Use(is_datetime_string)),
        "language": Or(str,[str]),
        "keyword": Or(str,[str]),
        "publisher": object,
        "distribution": [object],
        Optional("type"): And(Use(str)),
        Optional("theme"): And(Use(str)),
        Optional("identifier"): And(Use(str)),
        Optional("landingPage"): And(Use(str))
        })

    return   Schema(package_schema).validate(package)