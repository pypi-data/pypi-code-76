from gracie_dictionary_api import GracieBaseAPI


class profileController(GracieBaseAPI):
    """Profile Controller"""

    _controller_name = "profileController"

    def accuracyTable(self, **kwargs):
        """

        Args:
            id: (string): The id of existing profile's accuracy table
            languageId: (string): Language for results, default to user language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/accuracyTable'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def accuracyTableCell(self, **kwargs):
        """

        Args:
            limit: (integer): Max number of results
            offset: (integer): Start offset of results
            orderAsc: (boolean): orderAsc
            orderBy: (string): orderBy
            profileAccuracyCellId: (string): Id of the profile accuracy cell to retrieve

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'profileAccuracyCellId': {'name': 'profileAccuracyCellId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/accuracyTableCell'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, **kwargs):
        """

        Args:
            name: (string): Name of new profile to add
            useDocumentVector: (boolean): If profile is set up to use document doc2vec vectors, then we add document vector to the feature vector.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'name': {'name': 'name', 'required': False, 'in': 'query'}, 'useDocumentVector': {'name': 'useDocumentVector', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile to edit
            useDocumentVector: (boolean): Use document vector

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'useDocumentVector': {'name': 'useDocumentVector', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME
            type: (string): Specify type of profile: POWER_PROFILE, SKILL_PLUS_PLUS

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'type': {'name': 'type', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing profile

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def test(self, files, **kwargs):
        """

        Args:
            files: (array): The format is TSV: https://en.wikipedia.org/wiki/Tab-separated_valuesFirst field is the label, which is a name of profile-class. The label is followed by a single tab character. The text is listed after a tab. Tab and newline characters are removed from the text before it's dumped to a file.
            id: (string): Id of existing profile to test
            languageId: (string): Language for results, default to user language

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'files': {'name': 'files', 'required': True, 'in': 'formData'}, 'id': {'name': 'id', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/test'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
