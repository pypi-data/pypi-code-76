from gracie_dictionary_api import GracieBaseAPI


class abbreviationController(GracieBaseAPI):
    """Abbreviation Controller"""

    _controller_name = "abbreviationController"

    def addAbbreviation(self, abbreviationText, categoryName, **kwargs):
        """

        Args:
            abbreviationText: (string): Text of abbreviation to be added, should end in "."
            categoryName: (string): Name of category
            languageId: (string): Language id for new abbreviation in a category, default to user language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'abbreviationText': {'name': 'abbreviationText', 'required': True, 'in': 'query'}, 'categoryName': {'name': 'categoryName', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/abbreviation/addAbbreviation'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def addCategory(self, name, **kwargs):
        """

        Args:
            languageId: (string): Language id for new abbreviation category, default to user language
            name: (string): Name of new category

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/abbreviation/addCategory'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteAbbreviation(self, abbreviationText, categoryName, **kwargs):
        """

        Args:
            abbreviationText: (string): Text of abbreviation to delete
            categoryName: (string): Name of category
            languageId: (string): Language id of abbreviation from a category to delete, default to user language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'abbreviationText': {'name': 'abbreviationText', 'required': True, 'in': 'query'}, 'categoryName': {'name': 'categoryName', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/abbreviation/deleteAbbreviation'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteCategory(self, name, **kwargs):
        """

        Args:
            languageId: (string): Language id of abbreviation category to delete, default to user language
            name: (string): Name of category to delete

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/abbreviation/deleteCategory'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def listAbbreviations(self, categoryName, **kwargs):
        """

        Args:
            categoryName: (string): Name of category to list
            languageId: (string): Language id for results, default to user language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'categoryName': {'name': 'categoryName', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/abbreviation/listAbbreviations'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def listCategories(self, **kwargs):
        """

        Args:
            languageId: (string): Language id of results, default to user language

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/abbreviation/listCategories'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
