from gracie_dictionary_api import GracieBaseAPI


class briefController(GracieBaseAPI):
    """Brief Controller"""

    _controller_name = "briefController"

    def add(self, **kwargs):
        """

        Args:
            entityId: (string): Id of the entity to assign brief
            languageId: (string): Language id to assign new brief, default to user language
            text: (string): Brief text

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'text': {'name': 'text', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of the brief to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """

        Args:
            id: (string): Id of brief to edit
            text: (string): Brief text

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'text': {'name': 'text', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            entityId: (string): Id of the entity to list assigned briefs
            languageId: (string): Language for results, default to user language
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing brief to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
