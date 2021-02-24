from gracie_feeds_api import GracieBaseAPI


class tasksController(GracieBaseAPI):
    """Tasks Controller"""

    _controller_name = "tasksController"

    def cancel(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/cancel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            includeMessage: (boolean): includeMessage
            includeParameters: (boolean): includeParameters
            maxNumber: (integer): maxNumber
            offset: (integer): offset
            taskTypeId: (string): taskTypeId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'includeMessage': {'name': 'includeMessage', 'required': False, 'in': 'query'}, 'includeParameters': {'name': 'includeParameters', 'required': False, 'in': 'query'}, 'maxNumber': {'name': 'maxNumber', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'taskTypeId': {'name': 'taskTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeAllCompletedTasks(self, **kwargs):
        """

        Args:
            taskTypeId: (string): taskTypeId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'taskTypeId': {'name': 'taskTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/removeAllCompletedTasks'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
