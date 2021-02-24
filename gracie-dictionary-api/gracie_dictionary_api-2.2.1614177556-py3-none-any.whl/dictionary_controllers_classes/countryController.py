from gracie_dictionary_api import GracieBaseAPI


class countryController(GracieBaseAPI):
    """Country Controller"""

    _controller_name = "countryController"

    def add(self, **kwargs):
        """

        Args:
            capital: (string): Name of the country's capital
            code: (string): Country codes are short alphabetic or numeric geographical codes (geocodes) developed to represent countries and dependent areas, for use in data processing and communications. https://en.wikipedia.org/wiki/Country_code
            continentId: (string): Id of the continent where the country is located
            currencyCode: (string): Country's currency code (https://en.wikipedia.org/wiki/ISO_4217)
            currencyName: (string): Country's currency name (https://en.wikipedia.org/wiki/ISO_4217)
            name: (string): Country name
            phoneCode: (string): Country's phone code (https://en.wikipedia.org/wiki/List_of_country_calling_codes)
            postalCodeFormat: (string): Country's postal code format (https://en.wikipedia.org/wiki/List_of_postal_codes)
            postalCodeRegExp: (string): Regex format to match Country's postal code
            topLevelDomain: (string): Country's top-level domain (TLD)

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'capital': {'name': 'capital', 'required': False, 'in': 'query'}, 'code': {'name': 'code', 'required': False, 'in': 'query'}, 'continentId': {'name': 'continentId', 'required': False, 'in': 'query'}, 'currencyCode': {'name': 'currency-code', 'required': False, 'in': 'query'}, 'currencyName': {'name': 'currency-name', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'phoneCode': {'name': 'phone-code', 'required': False, 'in': 'query'}, 'postalCodeFormat': {'name': 'postal-code-format', 'required': False, 'in': 'query'}, 'postalCodeRegExp': {'name': 'postal-code-reg-exp', 'required': False, 'in': 'query'}, 'topLevelDomain': {'name': 'top-level-domain', 'required': False, 'in': 'query'}}
        parameters_names_map = {'currencyCode': 'currency-code', 'currencyName': 'currency-name', 'phoneCode': 'phone-code', 'postalCodeFormat': 'postal-code-format', 'postalCodeRegExp': 'postal-code-reg-exp', 'topLevelDomain': 'top-level-domain'}
        api = '/country/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, **kwargs):
        """

        Args:
            id: (string): Id of existing country

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/country/delete'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """

        Args:
            capital: (string): Name of the country's capital
            continentId: (string): Id of the continent where the country is located
            currencyCode: (string): Country's currency code (https://en.wikipedia.org/wiki/ISO_4217)
            currencyName: (string): Country's currency name (https://en.wikipedia.org/wiki/ISO_4217)
            id: (string): Id of existing country
            name: (string): Country name
            phoneCode: (string): Country's phone code (https://en.wikipedia.org/wiki/List_of_country_calling_codes)
            postalCodeFormat: (string): Country's postal code format (https://en.wikipedia.org/wiki/List_of_postal_codes)
            postalCodeRegExp: (string): Regex format to match Country's postal code
            topLevelDomain: (string): Country's top-level domain (TLD)

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'capital': {'name': 'capital', 'required': False, 'in': 'query'}, 'continentId': {'name': 'continentId', 'required': False, 'in': 'query'}, 'currencyCode': {'name': 'currency-code', 'required': False, 'in': 'query'}, 'currencyName': {'name': 'currency-name', 'required': False, 'in': 'query'}, 'id': {'name': 'id', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'phoneCode': {'name': 'phone-code', 'required': False, 'in': 'query'}, 'postalCodeFormat': {'name': 'postal-code-format', 'required': False, 'in': 'query'}, 'postalCodeRegExp': {'name': 'postal-code-reg-exp', 'required': False, 'in': 'query'}, 'topLevelDomain': {'name': 'top-level-domain', 'required': False, 'in': 'query'}}
        parameters_names_map = {'currencyCode': 'currency-code', 'currencyName': 'currency-name', 'phoneCode': 'phone-code', 'postalCodeFormat': 'postal-code-format', 'postalCodeRegExp': 'postal-code-reg-exp', 'topLevelDomain': 'top-level-domain'}
        api = '/country/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            id: (string): Id of existing continent
            orderAsc: (string): true = ascending (default); false = descending
            orderBy: (boolean): Sort results by order: NAME, CONTINENT

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/country/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, **kwargs):
        """

        Args:
            id: (string): Id of existing country

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'id': {'name': 'id', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/country/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
