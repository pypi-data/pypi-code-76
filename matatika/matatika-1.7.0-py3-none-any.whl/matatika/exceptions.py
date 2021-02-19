"""exceptions module"""

from dataclasses import dataclass


class MatatikaException(Exception):
    """Class to handle custom Matatika exceptions"""

    def __init__(self, message=None):

        super().__init__(message)
        self.message = message

    def __str__(self):

        return self.message


class NoDefaultContextSetError(MatatikaException):
    """Error to raise when no default context is set"""

    def __str__(self):

        msg = \
            "No default context is set\n" \
            "Set one using 'matatika context use' "\
            "(see 'matatika context use --help')"
        return msg


@dataclass
class ContextExistsError(MatatikaException):
    """Error to raise when a context exists"""

    name: str

    def __str__(self):

        msg = f"Context '{self.name}' already exists"
        return msg


@dataclass
class ContextDoesNotExistError(MatatikaException):
    """Error to raise when a context does not exists"""

    name: str

    def __str__(self):

        msg = f"Context '{self.name}' does not exist"
        return msg


@dataclass
class VariableNotSetError(MatatikaException):
    """Error to raise when a variable is not set in the default context"""

    variable: str

    def __post_init__(self):

        if self.variable == 'auth_token':
            self.set_cmd = "-a / --auth-token"
            self.set_env = "export AUTH_TOKEN=$VALUE"
            self.set_ctx = "matatika context update -a $AUTH_TOKEN"
        elif self.variable == 'endpoint_url':
            self.set_cmd = "-e / --endpoint-url"
            self.set_env = "export ENDPOINT_URL=$VALUE"
            self.set_ctx = "matatika context update -a $ENDPOINT_URL"
        elif self.variable == 'workspace_id':
            self.set_cmd = "-w / --workspace-id"
            self.set_env = "export WORKSPACE_ID=$VALUE"
            self.set_ctx = "matatika context update -w $WORKSPACE_ID"

    def __str__(self):

        msg = \
            f"Variable '{self.variable}' is not set\n" \
            f"Use '{self.set_cmd}' to provide a one-time command override\n" \
            f"Use '{self.set_env}' to set the variable in the system environment\n" \
            f"Use '{self.set_ctx}' to set the variable in the default context"
        return msg


class ResourceNotFoundError(MatatikaException):
    """Class to raise an exception when a resource is not found"""

    def __init__(self, resource_type: str, resource_id, endpoint_url):

        super().__init__()
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.endpoint_url = endpoint_url

    def __str__(self):

        msg = "{} {} does not exist within the current authorisation context: {}".format(
            self.resource_type.title(),
            self.resource_id,
            self.endpoint_url)
        return msg


class WorkspaceNotFoundError(ResourceNotFoundError):
    """Class to raise an exception when a workspace is not found"""

    def __init__(self, workspace_id, endpoint_url):

        super().__init__('workspace', workspace_id, endpoint_url)


class DatasetNotFoundError(ResourceNotFoundError):
    """Class to raise an exception when a dataset is not found"""

    def __init__(self, dataset_id, endpoint_url):

        super().__init__('dataset', dataset_id, endpoint_url)
