from gracie_dictionary_api import GracieBaseAPI


class searchController(GracieBaseAPI):
    """Search Controller"""

    _controller_name = "searchController"

    def processFile(self, file, **kwargs):
        """

        Args:
            file: (file): File to process
            filterFields: (string): Specify the specific fields to return in the results
            idfScoreMin: (number): Minimal IDF score for words to pass to result. [0, Double.MAX_VALUE]
            includeKeywordsReport: (boolean): Include a keywords report in the results
            languageId: (string): Language Id of text to process, defulat is to auto-detect language
            logging: (boolean): Enable logging for individual rules
            minRelevance: (integer): Minimal relevance value for entity to pass to result. [0, 100%]
            pipelineId: (string): Rules pipeline Id to use for processing, default uses the default pipeline
            stopAfterChunkNum: (integer): Only process up to the specified number of file chunks, default is all
            typeId: (string): How close the current text is to expected topic and topic-type. Closeness is evaluated by doc2vec model and entities. [0,1]. The bigger the value the bigger is confidence.

        Consumes:
            multipart/form-data

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'file': {'name': 'file', 'required': True, 'in': 'formData'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'idfScoreMin': {'name': 'idfScoreMin', 'required': False, 'in': 'query'}, 'includeKeywordsReport': {'name': 'includeKeywordsReport', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'minRelevance': {'name': 'min-relevance', 'required': False, 'in': 'query'}, 'pipelineId': {'name': 'pipelineId', 'required': False, 'in': 'query'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'query'}, 'typeId': {'name': 'typeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {'minRelevance': 'min-relevance'}
        api = '/search/processFile'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def processText(self, text, **kwargs):
        """

        Args:
            filterFields: (string): Specify the specific fields to return in the results, default includes all fields
            includeKeywordsReport: (boolean): Add keywords report for skillsets to result.
            languageId: (string): Language for results, default to user language
            logging: (boolean): Enable logging for individual rules
            minRelevance: (integer): Minimum relevance required for discovered entities
            minRelevance: (number): Miniumum IDF score to report on
            pipelineId: (string): Rules pipeline to process the text. If it is unset then default pipeline is used.
            stopAfterChunkNum: (integer): Only process up to the specified number of file chunks, default is all
            text: (type): Text to process
            typeId: (string): Optional Id of expected topic type

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'includeKeywordsReport': {'name': 'includeKeywordsReport', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'minRelevance': {'name': 'min-relevance', 'required': False, 'in': 'query'}, 'pipelineId': {'name': 'pipelineId', 'required': False, 'in': 'query'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}, 'typeId': {'name': 'typeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {'minRelevance': 'min-relevance'}
        api = '/search/processText'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
