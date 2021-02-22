import os
import yaml

from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

dir_name = os.path.abspath(".") + "/test"


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


rules = {
        "operation-parameters": {
            "description": "Operation parameters are unique and non-repeating.",
            "message": "{error}",
            "formats": ["oas3", "oas2"],
            "severity": "Error",
            "query": "paths.*.(get, put, post, delete, options, head, patch, trace).parameters",
            "validator": {
                "func": "oasOpParams",
            }
        }
    }


def test_OpParams():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0.yml")
    # source["paths"]["/pets"]["get"]["operationId"] = "listPets"
    # source["paths"]["/pets"]["post"]["operationId"] = "listPets"

    document = Document(source, DocumentType.oas)
    linter.setRules(rules)

    diagResult = linter.run(document)
    assert len(diagResult) == 0


def test_OpParams_with_error():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0.yml")

    add_parameter = {
        "name": "tags",
        "in": "query",
        "description": "filter",
        "required": False,
        "style": "form",
        "schema": {
            "type": "string"
        }
    }

    source["paths"]["/pets"]["get"]["parameters"].append(add_parameter)

    document = Document(source, DocumentType.oas)
    linter.setRules(rules)

    diagResult = linter.run(document)
    assert len(diagResult) == 1
    assert diagResult[0].path == ['paths', '/pets', 'get', 'parameters']

    # assert len(diagResult) == 2
    # assert diagResult[0].path == ['paths', '/pets', 'get', 'operationId']
    # assert diagResult[1].path == ['paths', '/pets', 'post', 'operationId']
