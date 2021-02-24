from gracie_dictionary_api import GracieBaseAPI


class usersController(GracieBaseAPI):
    """Users Controller"""

    _controller_name = "usersController"

    def add(self, login, password, typeId, **kwargs):
        """

        Args:
            description: (string): Optional description of new user
            enabled: (boolean): Enable/disable new user
            languageId: (string): Id of new user's language, default is English
            login: (string): Login name of new user
            password: (string): Password for new user
            typeId: (string): Id of user type to assign to new user

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'login': {'name': 'login', 'required': True, 'in': 'query'}, 'password': {'name': 'password', 'required': True, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            description: (string): New description for user
            enabled: (boolean): Enable/disable user
            id: (string): Id of user to edit
            languageId: (string): Id of new language for user
            login: (string): New login name for user
            password: (string): New password for user

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'login': {'name': 'login', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
        """

        Args:
            id: (string): Id of user to remove

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """

        Args:
            id: (string): Id of existing user to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def whoAmI(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/whoAmI'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
