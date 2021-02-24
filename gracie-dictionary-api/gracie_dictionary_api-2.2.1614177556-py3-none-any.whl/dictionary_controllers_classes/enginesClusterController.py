from gracie_dictionary_api import GracieBaseAPI


class enginesClusterController(GracieBaseAPI):
    """Engines Cluster Controller"""

    _controller_name = "enginesClusterController"

    def clusterStatus(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engines/cluster/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def clusterWorkers(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engines/cluster/workers'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
