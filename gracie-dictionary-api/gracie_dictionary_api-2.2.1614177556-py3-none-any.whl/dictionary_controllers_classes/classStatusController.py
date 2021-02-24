from gracie_dictionary_api import GracieBaseAPI


class classStatusController(GracieBaseAPI):
    """Class Status Controller"""

    _controller_name = "classStatusController"

    def list(self, **kwargs):
        """

        Args:
            languageId: (string): Language id for results, default to user language
            scope: (string): Class scope to retrieve:  All, Skills, TopicDictionaries, GeoDictionaries, Profiles, ClusterSets, Pipelines

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'scope': {'name': 'scope', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classStatus/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            classId: (string): Id of class { dictionaryId, topicTypeId, skillId, profileId } to retrieve
            languageId: (string): Language id for results, default to user language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'classId': {'name': 'classId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classStatus/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
