from gracie_dictionary_api import GracieBaseAPI


class skillParametersController(GracieBaseAPI):
    """Skill Parameters Controller"""

    _controller_name = "skillParametersController"

    def edit(self, skillId, **kwargs):
        """

        Args:
            confidenceCurve: (string): New confidence curve parameters: {  // [0, 1]  double[21] confidenceNormalizationCurve,  // [0, max_double]  double bhattacharyyaDistance,  // [0, 1)  double validationSetQuality}
            languageId: (string): Id of language to edit within skill, default is caller's language
            normalizationHigherThreshold: (number): New upper normalization threshold
            normalizationLowerThreshold: (number): New lower normalization threshold
            skillId: (string): Id of skill to edit

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'confidenceCurve': {'name': 'confidenceCurve', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'normalizationHigherThreshold': {'name': 'normalizationHigherThreshold', 'required': False, 'in': 'query'}, 'normalizationLowerThreshold': {'name': 'normalizationLowerThreshold', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillParameters/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, skillId, **kwargs):
        """

        Args:
            languageId: (string): Language id to retrieve parameters for, default is caller's language
            skillId: (string): Id of skill to retrieve parameters for

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillParameters/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
