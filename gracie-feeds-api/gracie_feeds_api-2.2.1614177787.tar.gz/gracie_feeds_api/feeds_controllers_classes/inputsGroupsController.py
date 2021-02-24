from gracie_feeds_api import GracieBaseAPI


class inputsGroupsController(GracieBaseAPI):
    """InputGroups is a manager for inputs."""

    _controller_name = "inputsGroupsController"

    def add(self, name, projectId, **kwargs):
        """Create new inputsGroup for project.

        Args:
            description: (string): Description. Any text.
            isRunning: (boolean): isRunning
            name: (string): name
            projectId: (string): projectId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputsGroups/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, inputsGroupId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): Description. Any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            name: (string): name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputsGroups/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, projectId):
        """Return the list of inputsGroups for project.

        Args:
            projectId: (string): projectId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputsGroups/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, inputsGroupId):
        """Remove existing inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputsGroups/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, inputsGroupId):
        """Return the inputsGroup with specified ID.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputsGroups/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def status(self, inputsGroupId, isRunning):
        """Set status for existing inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputsGroups/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
