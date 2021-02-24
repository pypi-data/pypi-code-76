from gracie_feeds_api import GracieBaseAPI


class emailMonitorController(GracieBaseAPI):
    """Email Monitor Controller"""

    _controller_name = "emailMonitorController"

    def add(self, hostname, password, projectId, user, userId, **kwargs):
        """Create a new monitor instance

        Args:
            enabled: (boolean): enabled
            folder: (string): folder
            hostname: (string): hostname
            languageId: (string): languageId
            password: (string): password
            port: (integer): port
            privacyMode: (boolean): privacyMode
            projectId: (string): projectId
            protocol: (string): protocol
            user: (string): user
            userId: (string): userId
            userMetadata: (type): userMetadata

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'folder': {'name': 'folder', 'required': False, 'in': 'query'}, 'hostname': {'name': 'hostname', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': True, 'in': 'query'}, 'port': {'name': 'port', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'protocol': {'name': 'protocol', 'required': False, 'in': 'query'}, 'user': {'name': 'user', 'required': True, 'in': 'query'}, 'userId': {'name': 'userId', 'required': True, 'in': 'query'}, 'userMetadata': {'name': 'userMetadata', 'required': False, 'in': 'body'}}
        parameters_names_map = {}
        api = '/emailMonitor/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """Remove an existing monitor instance

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/emailMonitor/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """Edit an existing monitor instance

        Args:
            enabled: (boolean): enabled
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/emailMonitor/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self):
        """Return the list of monitor instances"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/emailMonitor/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id):
        """Return a monitor instance

        Args:
            id: (string): id

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/emailMonitor/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
