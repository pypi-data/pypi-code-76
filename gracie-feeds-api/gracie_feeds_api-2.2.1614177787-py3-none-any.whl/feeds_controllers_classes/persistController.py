from gracie_feeds_api import GracieBaseAPI


class persistController(GracieBaseAPI):
    """Persist Controller"""

    _controller_name = "persistController"

    def add(self, dbHostname, dbName, dbPassword, dbPortNumber, dbType, dbUsername, name, **kwargs):
        """Create new persist instance.

        Args:
            dbHostname: (string): dbHostname
            dbName: (string): dbName
            dbPassword: (string): dbPassword
            dbPortNumber: (integer): dbPortNumber
            dbType: (string): dbType
            dbUsername: (string): dbUsername
            enabled: (boolean): enabled
            name: (string): name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dbHostname': {'name': 'dbHostname', 'required': True, 'in': 'query'}, 'dbName': {'name': 'dbName', 'required': True, 'in': 'query'}, 'dbPassword': {'name': 'dbPassword', 'required': True, 'in': 'query'}, 'dbPortNumber': {'name': 'dbPortNumber', 'required': True, 'in': 'query'}, 'dbType': {'name': 'dbType', 'required': True, 'in': 'query'}, 'dbUsername': {'name': 'dbUsername', 'required': True, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """Remove existing persist instance.

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """Edit existing persist instance.

        Args:
            dbHostname: (string): dbHostname
            dbName: (string): dbName
            dbPassword: (string): dbPassword
            dbPortNumber: (integer): dbPortNumber
            dbUsername: (string): dbUsername
            enabled: (boolean): enabled
            id: (string): id
            name: (string): name

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'dbHostname': {'name': 'dbHostname', 'required': False, 'in': 'query'}, 'dbName': {'name': 'dbName', 'required': False, 'in': 'query'}, 'dbPassword': {'name': 'dbPassword', 'required': False, 'in': 'query'}, 'dbPortNumber': {'name': 'dbPortNumber', 'required': False, 'in': 'query'}, 'dbUsername': {'name': 'dbUsername', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def enableES(self, enabled):
        """Enable/Disable persist to ElasticSearch

        Args:
            enabled: (boolean): enabled

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/enableES'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self):
        """Return the list of persist instances"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/persist/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """Return a persist instance

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
