from gracie_dictionary_api import GracieBaseAPI


class infoController(GracieBaseAPI):
    """Info Controller"""

    _controller_name = "infoController"

    def retrieve(self):
        """"""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/info/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
