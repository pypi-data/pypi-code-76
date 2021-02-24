from gracie_feeds_api import GracieBaseAPI


class dashboardsController(GracieBaseAPI):
    """Dashboards Controller"""

    _controller_name = "dashboardsController"

    def list(self, projectId, **kwargs):
        """Return list of dashboards for selected project.

        Args:
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy
            projectId: (string): projectId
            updateInterval: (string): updateInterval

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'updateInterval': {'name': 'updateInterval', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dashboards/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, id, **kwargs):
        """Return dashboard by ID.

        Args:
            id: (string): id
            updateInterval: (string): updateInterval

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'updateInterval': {'name': 'updateInterval', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dashboards/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
