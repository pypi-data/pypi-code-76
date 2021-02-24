from gracie_feeds_api import GracieBaseAPI


class loginController(GracieBaseAPI):
    """Login form."""

    _controller_name = "loginController"

    def login(self, login, password):
        """Login entry point.

        Args:
            login: (string): login
            password: (string): password

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'login': {'name': 'login', 'required': True, 'in': 'query'}, 'password': {'name': 'password', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/login'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
