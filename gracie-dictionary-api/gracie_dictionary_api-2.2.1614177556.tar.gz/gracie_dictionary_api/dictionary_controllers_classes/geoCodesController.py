from gracie_dictionary_api import GracieBaseAPI


class geoCodesController(GracieBaseAPI):
    """Geo Codes Controller"""

    _controller_name = "geoCodesController"

    def add(self, **kwargs):
        """

        Args:
            code: (string): New geo code to add
            entityId: (string): Id of geo entity to retrieve assigned code from
            typeId: (string): typeId of code to retrieve. See typesList API for list of available types.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'code': {'name': 'code', 'required': False, 'in': 'query'}, 'entityId': {'name': 'entityId', 'required': False, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            entityId: (string): Id of geo entity to retrieve assigned code from
            typeId: (string): typeId of code to retrieve. See typesList API for list of available types.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': False, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, **kwargs):
        """

        Args:
            codeId: (string): Existing geo code id to remove.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'codeId': {'name': 'codeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            codeId: (string): Existing geo code id to retrieve.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'codeId': {'name': 'codeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geo-codes/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def typesList(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/geo-codes/typesList'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
