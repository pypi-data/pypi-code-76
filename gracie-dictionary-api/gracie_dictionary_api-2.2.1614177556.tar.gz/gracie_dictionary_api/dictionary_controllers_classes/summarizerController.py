from gracie_dictionary_api import GracieBaseAPI


class summarizerController(GracieBaseAPI):
    """Summarizer Controller"""

    _controller_name = "summarizerController"

    def summarize(self, maxSentences, text, **kwargs):
        """

        Args:
            languageId: (string): Id of language to use for processing, default is to auto-detect language
            maxSentences: (integer): Maximum number of sentences to return in summary
            text: (type): Text to summarize

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'maxSentences': {'name': 'maxSentences', 'required': True, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'body'}}
        parameters_names_map = {}
        api = '/summarize'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
