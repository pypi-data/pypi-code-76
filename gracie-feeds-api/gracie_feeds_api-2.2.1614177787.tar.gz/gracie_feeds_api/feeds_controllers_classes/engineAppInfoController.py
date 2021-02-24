from gracie_feeds_api import GracieBaseAPI


class engineAppInfoController(GracieBaseAPI):
    """Engine App Info Controller"""

    _controller_name = "engineAppInfoController"

    def retrieve(self):
        """Return EngineApp info."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engine-app/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def searchParameters(self):
        """Return info."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engine-app/searchParameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def system(self):
        """Return info."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engine-app/system'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
