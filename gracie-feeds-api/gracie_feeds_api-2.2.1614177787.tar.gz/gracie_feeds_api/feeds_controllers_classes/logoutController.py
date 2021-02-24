from gracie_feeds_api import GracieBaseAPI


class logoutController(GracieBaseAPI):
    """Logout Controller"""

    _controller_name = "logoutController"

    def doLogout(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/doLogout'
        actions = ['get']
        consumes = []
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
