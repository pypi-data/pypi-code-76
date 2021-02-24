from gracie_dictionary_api import GracieBaseAPI


class geoEntitiesController(GracieBaseAPI):
    """Geo Entities Controller"""

    _controller_name = "geoEntitiesController"

    def add(self, **kwargs):
        """

        Args:
            adminCode: (string): Geo administration code
            alias: (string): Alias to assign to this geo-entity (not currently used)
            briefs: (string): Brief text used for semantic context disambiguation.
            countryId: (string): Id of existing country to assign
            featureCodeId: (string): Id of feature code of geo location
            latitude: (number): latitude of geo location
            longitude: (number): longitude of geo location
            names: (string): Names and aliases this geo location is know by
            parentId: (string): Parent id of feature code of geo location
            popularity: (integer): Popularity assigns additional weight to the relevance calculation. This allows artificially boosting a geo location results when there is not enough semantic context.
            population: (integer): Population of geo location

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'adminCode': {'name': 'adminCode', 'required': False, 'in': 'query'}, 'alias': {'name': 'alias', 'required': False, 'in': 'query'}, 'briefs': {'name': 'briefs', 'required': False, 'in': 'query'}, 'countryId': {'name': 'countryId', 'required': False, 'in': 'query'}, 'featureCodeId': {'name': 'featureCodeId', 'required': False, 'in': 'query'}, 'latitude': {'name': 'latitude', 'required': False, 'in': 'query'}, 'longitude': {'name': 'longitude', 'required': False, 'in': 'query'}, 'names': {'name': 'names', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'population': {'name': 'population', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, **kwargs):
        """

        Args:
            ids: (array): List of ids of existing geo-entity to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/bulkDelete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of existing geo-entity

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """

        Args:
            adminCode: (string): Geo administration code
            featureCodeId: (string): Id of feature code of geo location
            id: (string): Id of existing geo-entity
            latitude: (number): latitude of geo location
            longitude: (number): longitude of geo location
            parentId: (string): Parent id of feature code of geo location
            popularity: (integer): Popularity assigns additional weight to the relevance calculation. This allows artificially boosting a geo location results when there is not enough semantic context.
            population: (integer): Population of geo location

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'adminCode': {'name': 'adminCode', 'required': False, 'in': 'query'}, 'featureCodeId': {'name': 'featureCodeId', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': False, 'in': 'query'}, 'latitude': {'name': 'latitude', 'required': False, 'in': 'query'}, 'longitude': {'name': 'longitude', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'population': {'name': 'population', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            languageId: (string): Language for results, default to user language
            limit: (integer): Max number of results
            name: (string): Name of geo entities to list. Partial name search and wildchar "*" searchs are supported.
            offset: (integer): Start offset of results
            onlyMainNames: (boolean): Search by geo entity's mainName only
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME, POPULARITY, COUNTRY
            parentId: (string): Specifing a parentId will list only geo entities assiged to the parent

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def restore(self, **kwargs):
        """

        Args:
            ids: (string): Id of existing geo-entity to restore

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/restore'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing geo-entity

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
