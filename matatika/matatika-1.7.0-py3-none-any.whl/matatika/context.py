"""context module"""

import json
from pathlib import Path
from matatika.exceptions import (
    ContextExistsError,
    ContextDoesNotExistError,
    NoDefaultContextSetError
)


MATATIKA_DIR = '.matatika'
FILE = 'contexts.json'

DEFAULT = 'default'
CONTEXTS = 'contexts'
TEMPLATE = {
    DEFAULT: None,
    CONTEXTS: {}
}


class MatatikaContext():
    """Class to handle read/write operations to a contexts file"""

    def __init__(self):
        matatika_dir = Path.joinpath(Path.home(), MATATIKA_DIR)
        Path.mkdir(matatika_dir, exist_ok=True)
        self.contexts_file = Path.joinpath(matatika_dir, FILE)

        # create the templated file if it doesn't already exist
        if not Path.exists(self.contexts_file):
            with open(self.contexts_file, 'x') as contexts_file:
                json.dump(TEMPLATE, contexts_file)

    def _read_json(self) -> dict:

        with open(self.contexts_file, 'r') as contexts_file:
            contexts = json.load(contexts_file)
            return contexts

    def _write_json(self, contexts: dict) -> None:

        with open(self.contexts_file, 'w') as contexts_file:
            json.dump(contexts, contexts_file)

    def get_context(self, context_name: str) -> dict:
        """Returns the context 'context_name"""

        contexts = self._read_json()
        self._check_context_exists(context_name, contexts)

        return contexts[CONTEXTS][context_name]

    def get_all_contexts(self) -> dict:
        """Returns all contexts"""

        return self._read_json()[CONTEXTS]

    def create_context(self, context_name: str, variables: dict) -> None:
        """Creates a context in the contexts file"""

        contexts = self._read_json()
        self._check_context_does_not_exist(context_name, contexts)

        contexts[CONTEXTS].update({context_name: variables})
        self._write_json(contexts)

    def delete_context(self, context_name: str) -> None:
        """Deletes the context 'context_name', if it exists"""

        contexts = self._read_json()
        self._check_context_exists(context_name, contexts)

        contexts[CONTEXTS].pop(context_name)
        self._write_json(contexts)

    def get_default_context(self) -> tuple:
        """Gets the default context 'context_name', if it exists"""

        contexts = self._read_json()
        default_context_name = contexts[DEFAULT]

        if default_context_name is None:
            raise NoDefaultContextSetError

        return default_context_name, contexts[CONTEXTS][default_context_name]

    def set_default_context(self, context_name: str) -> None:
        """Sets the context 'context_name' as the default, if it exists"""

        contexts = self._read_json()

        if context_name is not None:
            self._check_context_exists(context_name, contexts)

        default_context = {"default": context_name}
        contexts.update(default_context)
        self._write_json(contexts)

    def update_default_context_variables(self, context_vars: dict) -> None:
        """Updates a context in the contexts file"""

        default_context_name, _default_context_vars = self.get_default_context()
        contexts = self._read_json()
        self._check_context_exists(default_context_name, contexts)

        for var_name, var_value in context_vars.items():
            contexts[CONTEXTS][default_context_name].update(
                {var_name: var_value})
        self._write_json(contexts)

    @staticmethod
    def _check_context_exists(context_name: str, contexts: dict) -> None:

        if context_name not in contexts[CONTEXTS]:
            raise ContextDoesNotExistError(context_name)

    @staticmethod
    def _check_context_does_not_exist(context_name: str, contexts: dict) -> None:

        if context_name in contexts[CONTEXTS]:
            raise ContextExistsError(context_name)
