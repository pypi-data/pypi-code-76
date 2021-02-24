from gracie_dictionary_api import GracieBaseAPI


class tasksController(GracieBaseAPI):
    """Tasks Controller"""

    _controller_name = "tasksController"

    def bulkDelete(self, ids):
        """

        Args:
            ids: (array): List of task ids to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/task/bulkDelete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def cancel(self, id):
        """

        Args:
            id: (string): Id of task to cancel

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/task/cancel'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): Id of task to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/task/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteCompleted(self, **kwargs):
        """

        Args:
            typeId: (string): Limit deletion of completed tasks to those of the specified task type id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'typeId': {'name': 'typeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/task/deleteCompleted'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            includeParameters: (boolean): Include task parameters in results
            includeResult: (boolean): Include task results in results
            limit: (integer): Limit the number of returned tasks
            offset: (integer): Starting offset of returned list
            orderAsc: (boolean): Return list of tasks sorted in ascending order
            orderBy: (string): Sort order of returned tasks, one of [STATUS, CREATED_AT, ENDED_AT, TYPE]
            typeId: (string): Limits returned tasks to those of the specified task type id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'includeParameters': {'name': 'includeParameters', 'required': False, 'in': 'query'}, 'includeResult': {'name': 'includeResult', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/task/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of task to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/task/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
