from schema import Schema, And, Or, Use, Optional
from typing import Any, Dict, List
from datetime import datetime
from dateutil import parser

is_datetime_string = lambda date: isinstance(parser.parse(date), datetime)

def validate_datapackage_minimal(package: Dict):

    package_schema = Schema({
        'title': And(str, len),
        'description': And(str, len),
        'author': And(str, len),
        })

    return   Schema(package_schema).validate(package)

def validate_datapackage_dcat2(package: Dict):

    package_schema = Schema({
        'type': And(str, len),
        'title': And(str, len),
        'description': And(str, len),
        'issued': And(Use(is_datetime_string)),
        "modified": And(Use(is_datetime_string)),
        "language": Or(str,[str]),
        "keyword": Or(str,[str]),
        "publisher": And(str, len),
        "distribution": [object]
        })

    return   Schema(package_schema).validate(package)