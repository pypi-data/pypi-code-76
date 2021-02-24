from gracie_dictionary_api import GracieBaseAPI


class clusterGroupController(GracieBaseAPI):
    """Cluster Group Controller"""

    _controller_name = "clusterGroupController"

    def add(self, **kwargs):
        """

        Args:
            clusterSetId: (string): Id of the cluster set to assign
            iterations: (integer): The optimization process is run N times with different starting states and best clusterization result is returned.
            languageId: (string): Language for results, default to user language
            maxClusters: (integer): The clusterization routine will perform clusterization and find number of clusters between Min Clusters and Max clusters. With higher Max Clusters value the procedure will subdivide document set into finer clusters.
            maxKeywords: (integer): Limit of number of names found for the cluster.
            minClusters: (integer): The clusterization routine will perform clusterization and find number of clusters between Min Clusters and Max clusters. With higher Max Clusters value the procedure will subdivide document set into finer clusters.
            name: (string): New cluster group name
            seed: (integer): The seed makes clusterization result reproducible: clusterizing the same set of documents with the same seed will return same set of clusters.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterSetId': {'name': 'clusterSetId', 'required': False, 'in': 'query'}, 'iterations': {'name': 'iterations', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'maxClusters': {'name': 'maxClusters', 'required': False, 'in': 'query'}, 'maxKeywords': {'name': 'maxKeywords', 'required': False, 'in': 'query'}, 'minClusters': {'name': 'minClusters', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'seed': {'name': 'seed', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def clusterize(self, **kwargs):
        """

        Args:
            id: (string): Id of the cluster group
            iterations: (integer): The optimization process is run N times with different starting states and best clusterization result is returned.
            languageId: (string): Language for results, default to user language
            maxKeywords: (integer): Limit of number of names found for the cluster.
            minClusters: (integer): The clusterization routine will perform clusterization and find number of clusters between Min Clusters and Max clusters. With higher Max Clusters value the procedure will subdivide document set into finer clusters.
            minClusters: (integer): The clusterization routine will perform clusterization and find number of clusters between Min Clusters and Max clusters. With higher Max Clusters value the procedure will subdivide document set into finer clusters.
            seed: (integer): The seed makes clusterization result reproducible: clusterizing the same set of documents with the same seed will return same set of clusters.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'iterations': {'name': 'iterations', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'maxKeywords': {'name': 'maxKeywords', 'required': False, 'in': 'query'}, 'minClusters': {'name': 'minClusters', 'required': False, 'in': 'query'}, 'seed': {'name': 'seed', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/clusterize'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of the cluster group to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            clusterSetId: (string): Id of the cluster set
            limit: (integer): Max number of results
            offset: (integer): Start offset of results
            orderAsc: (boolean): true = ascending (default); false = descending
            orderBy: (string): Sort results by order: NAME

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'clusterSetId': {'name': 'clusterSetId', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of the cluster group

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
