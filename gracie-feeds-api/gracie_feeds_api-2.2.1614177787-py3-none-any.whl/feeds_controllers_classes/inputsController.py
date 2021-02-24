from gracie_feeds_api import GracieBaseAPI


class inputsController(GracieBaseAPI):
    """Inputs management."""

    _controller_name = "inputsController"

    def amazonProductReviewsAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            amazonProductId: (string): Amazon product id for collecting reviews. Accept list of id's separated by commas
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'amazonProductId': {'name': 'amazonProductId', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/amazonProductReviews/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def amazonProductReviewsEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            amazonProductId: (string): Amazon product id for collecting reviews. Accept list of id's separated by commas
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'amazonProductId': {'name': 'amazonProductId', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/amazonProductReviews/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def amazonProductReviewsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/amazonProductReviews/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def amazonProductReviewsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/amazonProductReviews/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def amazonProductReviewsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/amazonProductReviews/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def amazonProductReviewsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/amazonProductReviews/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistCommunityAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/community/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistCommunityEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/community/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistCommunityList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/community/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistCommunityRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/community/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistCommunityRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/community/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistCommunityStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/community/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistEventsAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            artFilm: (boolean): artFilm
            bundleDuplicates: (boolean): bundleDuplicates
            career: (boolean): career
            charitable: (boolean): charitable
            competition: (boolean): competition
            dance: (boolean): dance
            description: (string): description
            festFair: (boolean): festFair
            fitnessHealth: (boolean): fitnessHealth
            foodDrink: (boolean): foodDrink
            free: (boolean): free
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            kidFriendly: (boolean): kidFriendly
            literary: (boolean): literary
            locationKey: (string): locationKey
            music: (boolean): music
            outdoor: (boolean): outdoor
            postedToday: (boolean): postedToday
            query: (string): query
            sale: (boolean): sale
            searchTitlesOnly: (boolean): searchTitlesOnly
            singles: (boolean): singles
            tech: (boolean): tech

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'artFilm': {'name': 'artFilm', 'required': False, 'in': 'query'}, 'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'career': {'name': 'career', 'required': False, 'in': 'query'}, 'charitable': {'name': 'charitable', 'required': False, 'in': 'query'}, 'competition': {'name': 'competition', 'required': False, 'in': 'query'}, 'dance': {'name': 'dance', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'festFair': {'name': 'festFair', 'required': False, 'in': 'query'}, 'fitnessHealth': {'name': 'fitnessHealth', 'required': False, 'in': 'query'}, 'foodDrink': {'name': 'foodDrink', 'required': False, 'in': 'query'}, 'free': {'name': 'free', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'kidFriendly': {'name': 'kidFriendly', 'required': False, 'in': 'query'}, 'literary': {'name': 'literary', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'music': {'name': 'music', 'required': False, 'in': 'query'}, 'outdoor': {'name': 'outdoor', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'sale': {'name': 'sale', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'singles': {'name': 'singles', 'required': False, 'in': 'query'}, 'tech': {'name': 'tech', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/events/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistEventsEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            artFilm: (boolean): artFilm
            bundleDuplicates: (boolean): bundleDuplicates
            career: (boolean): career
            charitable: (boolean): charitable
            competition: (boolean): competition
            dance: (boolean): dance
            description: (string): description
            festFair: (boolean): festFair
            fitnessHealth: (boolean): fitnessHealth
            foodDrink: (boolean): foodDrink
            free: (boolean): free
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            kidFriendly: (boolean): kidFriendly
            literary: (boolean): literary
            locationKey: (string): locationKey
            music: (boolean): music
            outdoor: (boolean): outdoor
            postedToday: (boolean): postedToday
            query: (string): query
            sale: (boolean): sale
            searchTitlesOnly: (boolean): searchTitlesOnly
            singles: (boolean): singles
            tech: (boolean): tech

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'artFilm': {'name': 'artFilm', 'required': False, 'in': 'query'}, 'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'career': {'name': 'career', 'required': False, 'in': 'query'}, 'charitable': {'name': 'charitable', 'required': False, 'in': 'query'}, 'competition': {'name': 'competition', 'required': False, 'in': 'query'}, 'dance': {'name': 'dance', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'festFair': {'name': 'festFair', 'required': False, 'in': 'query'}, 'fitnessHealth': {'name': 'fitnessHealth', 'required': False, 'in': 'query'}, 'foodDrink': {'name': 'foodDrink', 'required': False, 'in': 'query'}, 'free': {'name': 'free', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'kidFriendly': {'name': 'kidFriendly', 'required': False, 'in': 'query'}, 'literary': {'name': 'literary', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'music': {'name': 'music', 'required': False, 'in': 'query'}, 'outdoor': {'name': 'outdoor', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'sale': {'name': 'sale', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'singles': {'name': 'singles', 'required': False, 'in': 'query'}, 'tech': {'name': 'tech', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/events/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistEventsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/events/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistEventsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/events/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistEventsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/events/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistEventsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/events/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistForsaleAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            conditionExcellent: (boolean): conditionExcellent
            conditionFair: (boolean): conditionFair
            conditionGood: (boolean): conditionGood
            conditionLikeNew: (boolean): conditionLikeNew
            conditionNew: (boolean): conditionNew
            conditionSalvage: (boolean): conditionSalvage
            cryptocurrencyOk: (boolean): cryptocurrencyOk
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            makeAndModel: (string): makeAndModel
            milesFromZip: (integer): milesFromZip
            modelYearMax: (integer): modelYearMax
            modelYearMin: (integer): modelYearMin
            odometerMax: (integer): odometerMax
            odometerMin: (integer): odometerMin
            postedToday: (boolean): postedToday
            priceMax: (integer): priceMax
            priceMin: (integer): priceMin
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'conditionExcellent': {'name': 'conditionExcellent', 'required': False, 'in': 'query'}, 'conditionFair': {'name': 'conditionFair', 'required': False, 'in': 'query'}, 'conditionGood': {'name': 'conditionGood', 'required': False, 'in': 'query'}, 'conditionLikeNew': {'name': 'conditionLikeNew', 'required': False, 'in': 'query'}, 'conditionNew': {'name': 'conditionNew', 'required': False, 'in': 'query'}, 'conditionSalvage': {'name': 'conditionSalvage', 'required': False, 'in': 'query'}, 'cryptocurrencyOk': {'name': 'cryptocurrencyOk', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'makeAndModel': {'name': 'makeAndModel', 'required': False, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'modelYearMax': {'name': 'modelYearMax', 'required': False, 'in': 'query'}, 'modelYearMin': {'name': 'modelYearMin', 'required': False, 'in': 'query'}, 'odometerMax': {'name': 'odometerMax', 'required': False, 'in': 'query'}, 'odometerMin': {'name': 'odometerMin', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'priceMax': {'name': 'priceMax', 'required': False, 'in': 'query'}, 'priceMin': {'name': 'priceMin', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/forSale/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistForsaleEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            conditionExcellent: (boolean): conditionExcellent
            conditionFair: (boolean): conditionFair
            conditionGood: (boolean): conditionGood
            conditionLikeNew: (boolean): conditionLikeNew
            conditionNew: (boolean): conditionNew
            conditionSalvage: (boolean): conditionSalvage
            cryptocurrencyOk: (boolean): cryptocurrencyOk
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            makeAndModel: (string): makeAndModel
            milesFromZip: (integer): milesFromZip
            modelYearMax: (integer): modelYearMax
            modelYearMin: (integer): modelYearMin
            odometerMax: (integer): odometerMax
            odometerMin: (integer): odometerMin
            postedToday: (boolean): postedToday
            priceMax: (integer): priceMax
            priceMin: (integer): priceMin
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'conditionExcellent': {'name': 'conditionExcellent', 'required': False, 'in': 'query'}, 'conditionFair': {'name': 'conditionFair', 'required': False, 'in': 'query'}, 'conditionGood': {'name': 'conditionGood', 'required': False, 'in': 'query'}, 'conditionLikeNew': {'name': 'conditionLikeNew', 'required': False, 'in': 'query'}, 'conditionNew': {'name': 'conditionNew', 'required': False, 'in': 'query'}, 'conditionSalvage': {'name': 'conditionSalvage', 'required': False, 'in': 'query'}, 'cryptocurrencyOk': {'name': 'cryptocurrencyOk', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'makeAndModel': {'name': 'makeAndModel', 'required': False, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'modelYearMax': {'name': 'modelYearMax', 'required': False, 'in': 'query'}, 'modelYearMin': {'name': 'modelYearMin', 'required': False, 'in': 'query'}, 'odometerMax': {'name': 'odometerMax', 'required': False, 'in': 'query'}, 'odometerMin': {'name': 'odometerMin', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'priceMax': {'name': 'priceMax', 'required': False, 'in': 'query'}, 'priceMin': {'name': 'priceMin', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/forSale/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistForsaleList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/forSale/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistForsaleRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/forSale/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistForsaleRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/forSale/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistForsaleStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/forSale/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistGigsAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isPaid: (boolean): isPaid
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isPaid': {'name': 'isPaid', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/gigs/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistGigsEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isPaid: (boolean): isPaid
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isPaid': {'name': 'isPaid', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/gigs/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistGigsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/gigs/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistGigsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/gigs/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistGigsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/gigs/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistGigsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/gigs/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistHousingAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bathroomsMax: (integer): bathroomsMax
            bathroomsMin: (integer): bathroomsMin
            bedroomsMax: (integer): bedroomsMax
            bedroomsMin: (integer): bedroomsMin
            bundleDuplicates: (boolean): bundleDuplicates
            catsOk: (boolean): catsOk
            description: (string): description
            dogsOk: (boolean): dogsOk
            ft2Max: (integer): ft2Max
            ft2Min: (integer): ft2Min
            furnished: (boolean): furnished
            hasImage: (boolean): hasImage
            housingTypeApartment: (boolean): housingTypeApartment
            housingTypeAssistedLiving: (boolean): housingTypeAssistedLiving
            housingTypeCondo: (boolean): housingTypeCondo
            housingTypeCottageCabin: (boolean): housingTypeCottageCabin
            housingTypeDuplex: (boolean): housingTypeDuplex
            housingTypeFlat: (boolean): housingTypeFlat
            housingTypeHouse: (boolean): housingTypeHouse
            housingTypeInLaw: (boolean): housingTypeInLaw
            housingTypeLand: (boolean): housingTypeLand
            housingTypeLoft: (boolean): housingTypeLoft
            housingTypeManufactured: (boolean): housingTypeManufactured
            housingTypeTownhouse: (boolean): housingTypeTownhouse
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            laundryLaundryInBldg: (boolean): laundryLaundryInBldg
            laundryLaundryOnSite: (boolean): laundryLaundryOnSite
            laundryNoLaundryOnSite: (boolean): laundryNoLaundryOnSite
            laundryWdHookups: (boolean): laundryWdHookups
            laundryWdInUnit: (boolean): laundryWdInUnit
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            noSmoking: (boolean): noSmoking
            parkingAttachedGarage: (boolean): parkingAttachedGarage
            parkingCarport: (boolean): parkingCarport
            parkingDetachedGarage: (boolean): parkingDetachedGarage
            parkingNoParking: (boolean): parkingNoParking
            parkingOffStreetParking: (boolean): parkingOffStreetParking
            parkingStreetParking: (boolean): parkingStreetParking
            parkingValetParking: (boolean): parkingValetParking
            postedToday: (boolean): postedToday
            priceMax: (integer): priceMax
            priceMin: (integer): priceMin
            privateBath: (boolean): privateBath
            privateRoom: (boolean): privateRoom
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            wheelchairAccess: (boolean): wheelchairAccess
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bathroomsMax': {'name': 'bathroomsMax', 'required': False, 'in': 'query'}, 'bathroomsMin': {'name': 'bathroomsMin', 'required': False, 'in': 'query'}, 'bedroomsMax': {'name': 'bedroomsMax', 'required': False, 'in': 'query'}, 'bedroomsMin': {'name': 'bedroomsMin', 'required': False, 'in': 'query'}, 'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'catsOk': {'name': 'catsOk', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'dogsOk': {'name': 'dogsOk', 'required': False, 'in': 'query'}, 'ft2Max': {'name': 'ft2Max', 'required': False, 'in': 'query'}, 'ft2Min': {'name': 'ft2Min', 'required': False, 'in': 'query'}, 'furnished': {'name': 'furnished', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'housingTypeApartment': {'name': 'housingTypeApartment', 'required': False, 'in': 'query'}, 'housingTypeAssistedLiving': {'name': 'housingTypeAssistedLiving', 'required': False, 'in': 'query'}, 'housingTypeCondo': {'name': 'housingTypeCondo', 'required': False, 'in': 'query'}, 'housingTypeCottageCabin': {'name': 'housingTypeCottageCabin', 'required': False, 'in': 'query'}, 'housingTypeDuplex': {'name': 'housingTypeDuplex', 'required': False, 'in': 'query'}, 'housingTypeFlat': {'name': 'housingTypeFlat', 'required': False, 'in': 'query'}, 'housingTypeHouse': {'name': 'housingTypeHouse', 'required': False, 'in': 'query'}, 'housingTypeInLaw': {'name': 'housingTypeInLaw', 'required': False, 'in': 'query'}, 'housingTypeLand': {'name': 'housingTypeLand', 'required': False, 'in': 'query'}, 'housingTypeLoft': {'name': 'housingTypeLoft', 'required': False, 'in': 'query'}, 'housingTypeManufactured': {'name': 'housingTypeManufactured', 'required': False, 'in': 'query'}, 'housingTypeTownhouse': {'name': 'housingTypeTownhouse', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'laundryLaundryInBldg': {'name': 'laundryLaundryInBldg', 'required': False, 'in': 'query'}, 'laundryLaundryOnSite': {'name': 'laundryLaundryOnSite', 'required': False, 'in': 'query'}, 'laundryNoLaundryOnSite': {'name': 'laundryNoLaundryOnSite', 'required': False, 'in': 'query'}, 'laundryWdHookups': {'name': 'laundryWdHookups', 'required': False, 'in': 'query'}, 'laundryWdInUnit': {'name': 'laundryWdInUnit', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'noSmoking': {'name': 'noSmoking', 'required': False, 'in': 'query'}, 'parkingAttachedGarage': {'name': 'parkingAttachedGarage', 'required': False, 'in': 'query'}, 'parkingCarport': {'name': 'parkingCarport', 'required': False, 'in': 'query'}, 'parkingDetachedGarage': {'name': 'parkingDetachedGarage', 'required': False, 'in': 'query'}, 'parkingNoParking': {'name': 'parkingNoParking', 'required': False, 'in': 'query'}, 'parkingOffStreetParking': {'name': 'parkingOffStreetParking', 'required': False, 'in': 'query'}, 'parkingStreetParking': {'name': 'parkingStreetParking', 'required': False, 'in': 'query'}, 'parkingValetParking': {'name': 'parkingValetParking', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'priceMax': {'name': 'priceMax', 'required': False, 'in': 'query'}, 'priceMin': {'name': 'priceMin', 'required': False, 'in': 'query'}, 'privateBath': {'name': 'privateBath', 'required': False, 'in': 'query'}, 'privateRoom': {'name': 'privateRoom', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'wheelchairAccess': {'name': 'wheelchairAccess', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/housing/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistHousingEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bathroomsMax: (integer): bathroomsMax
            bathroomsMin: (integer): bathroomsMin
            bedroomsMax: (integer): bedroomsMax
            bedroomsMin: (integer): bedroomsMin
            bundleDuplicates: (boolean): bundleDuplicates
            catsOk: (boolean): catsOk
            description: (string): description
            dogsOk: (boolean): dogsOk
            ft2Max: (integer): ft2Max
            ft2Min: (integer): ft2Min
            furnished: (boolean): furnished
            hasImage: (boolean): hasImage
            housingTypeApartment: (boolean): housingTypeApartment
            housingTypeAssistedLiving: (boolean): housingTypeAssistedLiving
            housingTypeCondo: (boolean): housingTypeCondo
            housingTypeCottageCabin: (boolean): housingTypeCottageCabin
            housingTypeDuplex: (boolean): housingTypeDuplex
            housingTypeFlat: (boolean): housingTypeFlat
            housingTypeHouse: (boolean): housingTypeHouse
            housingTypeInLaw: (boolean): housingTypeInLaw
            housingTypeLand: (boolean): housingTypeLand
            housingTypeLoft: (boolean): housingTypeLoft
            housingTypeManufactured: (boolean): housingTypeManufactured
            housingTypeTownhouse: (boolean): housingTypeTownhouse
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            laundryLaundryInBldg: (boolean): laundryLaundryInBldg
            laundryLaundryOnSite: (boolean): laundryLaundryOnSite
            laundryNoLaundryOnSite: (boolean): laundryNoLaundryOnSite
            laundryWdHookups: (boolean): laundryWdHookups
            laundryWdInUnit: (boolean): laundryWdInUnit
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            noSmoking: (boolean): noSmoking
            parkingAttachedGarage: (boolean): parkingAttachedGarage
            parkingCarport: (boolean): parkingCarport
            parkingDetachedGarage: (boolean): parkingDetachedGarage
            parkingNoParking: (boolean): parkingNoParking
            parkingOffStreetParking: (boolean): parkingOffStreetParking
            parkingStreetParking: (boolean): parkingStreetParking
            parkingValetParking: (boolean): parkingValetParking
            postedToday: (boolean): postedToday
            priceMax: (integer): priceMax
            priceMin: (integer): priceMin
            privateBath: (boolean): privateBath
            privateRoom: (boolean): privateRoom
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            wheelchairAccess: (boolean): wheelchairAccess
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bathroomsMax': {'name': 'bathroomsMax', 'required': False, 'in': 'query'}, 'bathroomsMin': {'name': 'bathroomsMin', 'required': False, 'in': 'query'}, 'bedroomsMax': {'name': 'bedroomsMax', 'required': False, 'in': 'query'}, 'bedroomsMin': {'name': 'bedroomsMin', 'required': False, 'in': 'query'}, 'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'catsOk': {'name': 'catsOk', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'dogsOk': {'name': 'dogsOk', 'required': False, 'in': 'query'}, 'ft2Max': {'name': 'ft2Max', 'required': False, 'in': 'query'}, 'ft2Min': {'name': 'ft2Min', 'required': False, 'in': 'query'}, 'furnished': {'name': 'furnished', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'housingTypeApartment': {'name': 'housingTypeApartment', 'required': False, 'in': 'query'}, 'housingTypeAssistedLiving': {'name': 'housingTypeAssistedLiving', 'required': False, 'in': 'query'}, 'housingTypeCondo': {'name': 'housingTypeCondo', 'required': False, 'in': 'query'}, 'housingTypeCottageCabin': {'name': 'housingTypeCottageCabin', 'required': False, 'in': 'query'}, 'housingTypeDuplex': {'name': 'housingTypeDuplex', 'required': False, 'in': 'query'}, 'housingTypeFlat': {'name': 'housingTypeFlat', 'required': False, 'in': 'query'}, 'housingTypeHouse': {'name': 'housingTypeHouse', 'required': False, 'in': 'query'}, 'housingTypeInLaw': {'name': 'housingTypeInLaw', 'required': False, 'in': 'query'}, 'housingTypeLand': {'name': 'housingTypeLand', 'required': False, 'in': 'query'}, 'housingTypeLoft': {'name': 'housingTypeLoft', 'required': False, 'in': 'query'}, 'housingTypeManufactured': {'name': 'housingTypeManufactured', 'required': False, 'in': 'query'}, 'housingTypeTownhouse': {'name': 'housingTypeTownhouse', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'laundryLaundryInBldg': {'name': 'laundryLaundryInBldg', 'required': False, 'in': 'query'}, 'laundryLaundryOnSite': {'name': 'laundryLaundryOnSite', 'required': False, 'in': 'query'}, 'laundryNoLaundryOnSite': {'name': 'laundryNoLaundryOnSite', 'required': False, 'in': 'query'}, 'laundryWdHookups': {'name': 'laundryWdHookups', 'required': False, 'in': 'query'}, 'laundryWdInUnit': {'name': 'laundryWdInUnit', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'noSmoking': {'name': 'noSmoking', 'required': False, 'in': 'query'}, 'parkingAttachedGarage': {'name': 'parkingAttachedGarage', 'required': False, 'in': 'query'}, 'parkingCarport': {'name': 'parkingCarport', 'required': False, 'in': 'query'}, 'parkingDetachedGarage': {'name': 'parkingDetachedGarage', 'required': False, 'in': 'query'}, 'parkingNoParking': {'name': 'parkingNoParking', 'required': False, 'in': 'query'}, 'parkingOffStreetParking': {'name': 'parkingOffStreetParking', 'required': False, 'in': 'query'}, 'parkingStreetParking': {'name': 'parkingStreetParking', 'required': False, 'in': 'query'}, 'parkingValetParking': {'name': 'parkingValetParking', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'priceMax': {'name': 'priceMax', 'required': False, 'in': 'query'}, 'priceMin': {'name': 'priceMin', 'required': False, 'in': 'query'}, 'privateBath': {'name': 'privateBath', 'required': False, 'in': 'query'}, 'privateRoom': {'name': 'privateRoom', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'wheelchairAccess': {'name': 'wheelchairAccess', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/housing/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistHousingList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/housing/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistHousingRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/housing/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistHousingRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/housing/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistHousingStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/housing/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistJobsAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            employmentTypeContract: (boolean): employmentTypeContract
            employmentTypeEmployeesChoice: (boolean): employmentTypeEmployeesChoice
            employmentTypeFullTime: (boolean): employmentTypeFullTime
            employmentTypePartTime: (boolean): employmentTypePartTime
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            internship: (boolean): internship
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            nonProfit: (boolean): nonProfit
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            telecommute: (boolean): telecommute
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'employmentTypeContract': {'name': 'employmentTypeContract', 'required': False, 'in': 'query'}, 'employmentTypeEmployeesChoice': {'name': 'employmentTypeEmployeesChoice', 'required': False, 'in': 'query'}, 'employmentTypeFullTime': {'name': 'employmentTypeFullTime', 'required': False, 'in': 'query'}, 'employmentTypePartTime': {'name': 'employmentTypePartTime', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'internship': {'name': 'internship', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'nonProfit': {'name': 'nonProfit', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'telecommute': {'name': 'telecommute', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/jobs/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistJobsEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            employmentTypeContract: (boolean): employmentTypeContract
            employmentTypeEmployeesChoice: (boolean): employmentTypeEmployeesChoice
            employmentTypeFullTime: (boolean): employmentTypeFullTime
            employmentTypePartTime: (boolean): employmentTypePartTime
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            internship: (boolean): internship
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            nonProfit: (boolean): nonProfit
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            telecommute: (boolean): telecommute
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'employmentTypeContract': {'name': 'employmentTypeContract', 'required': False, 'in': 'query'}, 'employmentTypeEmployeesChoice': {'name': 'employmentTypeEmployeesChoice', 'required': False, 'in': 'query'}, 'employmentTypeFullTime': {'name': 'employmentTypeFullTime', 'required': False, 'in': 'query'}, 'employmentTypePartTime': {'name': 'employmentTypePartTime', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'internship': {'name': 'internship', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'nonProfit': {'name': 'nonProfit', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'telecommute': {'name': 'telecommute', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/jobs/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistJobsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/jobs/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistJobsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/jobs/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistJobsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/jobs/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistJobsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/jobs/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistLocations(self):
        """Return Craigslist RSS locations list."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/craigslist/locations'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistResumesAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/resumes/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistResumesEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/resumes/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistResumesList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/resumes/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistResumesRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/resumes/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistResumesRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/resumes/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistResumesStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/resumes/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistServicesAdd(self, inputName, inputsGroupId, locationKey, **kwargs):
        """Create new input for inputsGroup.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/services/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistServicesEdit(self, inputId, locationKey, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            bundleDuplicates: (boolean): bundleDuplicates
            description: (string): description
            hasImage: (boolean): hasImage
            includeNearbyAreas: (boolean): includeNearbyAreas
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            locationKey: (string): locationKey
            milesFromZip: (integer): milesFromZip
            postedToday: (boolean): postedToday
            query: (string): query
            searchTitlesOnly: (boolean): searchTitlesOnly
            zipCode: (string): zipCode

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'bundleDuplicates': {'name': 'bundleDuplicates', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'hasImage': {'name': 'hasImage', 'required': False, 'in': 'query'}, 'includeNearbyAreas': {'name': 'includeNearbyAreas', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'locationKey': {'name': 'locationKey', 'required': True, 'in': 'query'}, 'milesFromZip': {'name': 'milesFromZip', 'required': False, 'in': 'query'}, 'postedToday': {'name': 'postedToday', 'required': False, 'in': 'query'}, 'query': {'name': 'query', 'required': False, 'in': 'query'}, 'searchTitlesOnly': {'name': 'searchTitlesOnly', 'required': False, 'in': 'query'}, 'zipCode': {'name': 'zipCode', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/services/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistServicesList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/services/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistServicesRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/services/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistServicesRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/services/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def craigslistServicesStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/craigslist/services/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def ebaySearchAdd(self, inputName, inputsGroupId, keywords, **kwargs):
        """Create new input for inputsGroup.

        Args:
            buyerPostalCode: (string): Buyer postal code to sort.
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            keywords: (string): Keywords for search.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'buyerPostalCode': {'name': 'buyerPostalCode', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'keywords': {'name': 'keywords', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/ebaySearch/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def ebaySearchEdit(self, inputId, keywords, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            buyerPostalCode: (string): Buyer postal code to sort.
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            keywords: (string): Keywords for search.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'buyerPostalCode': {'name': 'buyerPostalCode', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'keywords': {'name': 'keywords', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/ebaySearch/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def ebaySearchList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/ebaySearch/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def ebaySearchRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/ebaySearch/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def ebaySearchRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/ebaySearch/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def ebaySearchStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/ebaySearch/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def homedepotProductReviewsAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            homedepotProductId: (string): Home Depot product id for collecting reviews
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'homedepotProductId': {'name': 'homedepotProductId', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/homedepotProductReviews/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def homedepotProductReviewsEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            homedepotProductId: (string): Home Depot product id for collecting reviews
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'homedepotProductId': {'name': 'homedepotProductId', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/homedepotProductReviews/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def homedepotProductReviewsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/homedepotProductReviews/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def homedepotProductReviewsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/homedepotProductReviews/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def homedepotProductReviewsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/homedepotProductReviews/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def homedepotProductReviewsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/homedepotProductReviews/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def inputTypesList(self):
        """Return the list of input types."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/inputTypesList'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def lowesProductReviewsAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            lowesProductUrl: (string): Lowes product url for collecting reviews

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'lowesProductUrl': {'name': 'lowesProductUrl', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/lowesProductReviews/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def lowesProductReviewsEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            lowesProductUrl: (string): Lowes product url for collecting reviews

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'lowesProductUrl': {'name': 'lowesProductUrl', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/lowesProductReviews/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def lowesProductReviewsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/lowesProductReviews/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def lowesProductReviewsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/lowesProductReviews/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def lowesProductReviewsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/lowesProductReviews/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def lowesProductReviewsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/lowesProductReviews/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchAdd(self, category, inputName, inputsGroupId, searchQuery, **kwargs):
        """Create new input for inputsGroup.

        Args:
            category: (string): category
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            language: (string): language
            searchQuery: (string): searchQuery
            timeRange: (string): timeRange

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'category': {'name': 'category', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'language': {'name': 'language', 'required': False, 'in': 'query'}, 'searchQuery': {'name': 'searchQuery', 'required': True, 'in': 'query'}, 'timeRange': {'name': 'timeRange', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/metasearch/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchEdit(self, category, inputId, searchQuery, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            category: (string): category
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            language: (string): language
            searchQuery: (string): searchQuery
            timeRange: (string): timeRange

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'category': {'name': 'category', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'language': {'name': 'language', 'required': False, 'in': 'query'}, 'searchQuery': {'name': 'searchQuery', 'required': True, 'in': 'query'}, 'timeRange': {'name': 'timeRange', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/metasearch/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/metasearch/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchParameters(self):
        """Return Metasearch parameters."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/metasearch/parameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/metasearch/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/metasearch/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def metasearchStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/metasearch/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchAdd(self, inputName, inputsGroupId, searchQuery, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            limit: (integer): Limit.
            maxCommentsCount: (integer): Maximum amount of comments to retrieve
            maxCommentsDepth: (integer): Maximum comments depth
            searchQuery: (string): Search query.
            sort: (string): Sort.
            timeWindow: (string): Time window.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'maxCommentsCount': {'name': 'maxCommentsCount', 'required': False, 'in': 'query'}, 'maxCommentsDepth': {'name': 'maxCommentsDepth', 'required': False, 'in': 'query'}, 'searchQuery': {'name': 'searchQuery', 'required': True, 'in': 'query'}, 'sort': {'name': 'sort', 'required': False, 'in': 'query'}, 'timeWindow': {'name': 'timeWindow', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/search/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchEdit(self, inputId, searchQuery, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            limit: (integer): Limit.
            maxCommentsCount: (integer): Maximum amount of comments to retrieve
            maxCommentsDepth: (integer): Maximum comments depth
            searchQuery: (string): Search query.
            sort: (string): Sort.
            timeWindow: (string): Time window.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'maxCommentsCount': {'name': 'maxCommentsCount', 'required': False, 'in': 'query'}, 'maxCommentsDepth': {'name': 'maxCommentsDepth', 'required': False, 'in': 'query'}, 'searchQuery': {'name': 'searchQuery', 'required': True, 'in': 'query'}, 'sort': {'name': 'sort', 'required': False, 'in': 'query'}, 'timeWindow': {'name': 'timeWindow', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/search/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/search/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchParameters(self):
        """Return Reddit search parameters list."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/reddit/search/parameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/search/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/search/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSearchStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/search/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSubredditAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            maxCommentsCount: (integer): Maximum amount of comments to retrieve
            maxCommentsDepth: (integer): Maximum comments depth
            subreddit: (string): Subreddit

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'maxCommentsCount': {'name': 'maxCommentsCount', 'required': False, 'in': 'query'}, 'maxCommentsDepth': {'name': 'maxCommentsDepth', 'required': False, 'in': 'query'}, 'subreddit': {'name': 'subreddit', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/subreddit/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSubredditEdit(self, inputId, subreddit, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            maxCommentsCount: (integer): Maximum amount of comments to retrieve
            maxCommentsDepth: (integer): Maximum comments depth
            subreddit: (string): Subreddit

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'maxCommentsCount': {'name': 'maxCommentsCount', 'required': False, 'in': 'query'}, 'maxCommentsDepth': {'name': 'maxCommentsDepth', 'required': False, 'in': 'query'}, 'subreddit': {'name': 'subreddit', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/subreddit/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSubredditList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/subreddit/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSubredditRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/subreddit/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSubredditRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/subreddit/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def redditSubredditStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/reddit/subreddit/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            maxRssArticleComments: (integer): Maximum amount of comments returned for each RSS article
            maxRssWatchArticleCommentsMs: (integer): Maximum amount of milliseconds to monitor comments for RSS article
            rssFeedKey: (string): rssFeedKey

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'maxRssArticleComments': {'name': 'maxRssArticleComments', 'required': False, 'in': 'query'}, 'maxRssWatchArticleCommentsMs': {'name': 'maxRssWatchArticleCommentsMs', 'required': False, 'in': 'query'}, 'rssFeedKey': {'name': 'rssFeedKey', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            maxRssArticleComments: (integer): Maximum amount of comments returned for each RSS article
            maxRssWatchArticleCommentsMs: (integer): Maximum amount of milliseconds to monitor comments for RSS article
            rssFeedKey: (string): rssFeedKey

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'maxRssArticleComments': {'name': 'maxRssArticleComments', 'required': False, 'in': 'query'}, 'maxRssWatchArticleCommentsMs': {'name': 'maxRssWatchArticleCommentsMs', 'required': False, 'in': 'query'}, 'rssFeedKey': {'name': 'rssFeedKey', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssParameters(self):
        """Return RSS parameters list."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/rss/parameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssStatistics(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/statistics'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rss/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            categories: (array): List of categories. Choose feeds with at least one match. Empty list processed as all possible variants.
            countries: (array): List of countries. Choose feeds with at least one match. Empty list processed as all possible variants.
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            languages: (array): List of languages. Choose feeds with at least one match. Empty list processed as all possible variants.
            maxRssArticleComments: (integer): Maximum amount of comments returned for each RSS article
            maxRssWatchArticleCommentsMs: (integer): Maximum amount of milliseconds to monitor comments for RSS article

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'categories': {'name': 'categories', 'required': False, 'in': 'query'}, 'countries': {'name': 'countries', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'languages': {'name': 'languages', 'required': False, 'in': 'query'}, 'maxRssArticleComments': {'name': 'maxRssArticleComments', 'required': False, 'in': 'query'}, 'maxRssWatchArticleCommentsMs': {'name': 'maxRssWatchArticleCommentsMs', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            categories: (array): List of categories. Choose feeds with at least one match. Empty list processed as all possible variants.
            countries: (array): List of countries. Choose feeds with at least one match. Empty list processed as all possible variants.
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            languages: (array): List of languages. Choose feeds with at least one match. Empty list processed as all possible variants.
            maxRssArticleComments: (integer): Maximum amount of comments returned for each RSS article
            maxRssWatchArticleCommentsMs: (integer): Maximum amount of milliseconds to monitor comments for RSS article

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'categories': {'name': 'categories', 'required': False, 'in': 'query'}, 'countries': {'name': 'countries', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'languages': {'name': 'languages', 'required': False, 'in': 'query'}, 'maxRssArticleComments': {'name': 'maxRssArticleComments', 'required': False, 'in': 'query'}, 'maxRssWatchArticleCommentsMs': {'name': 'maxRssWatchArticleCommentsMs', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleParameters(self):
        """Return RSS bundle parameters list."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/rssBundle/parameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleStatistics(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/statistics'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def rssBundleStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/rssBundle/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterAdd(self, inputName, inputsGroupId, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            twitterTracks: (string): twitterTracks
            twitterUsers: (string): twitterUsers

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'twitterTracks': {'name': 'twitterTracks', 'required': False, 'in': 'query'}, 'twitterUsers': {'name': 'twitterUsers', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            twitterTracks: (string): twitterTracks
            twitterUsers: (string): twitterUsers

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'twitterTracks': {'name': 'twitterTracks', 'required': False, 'in': 'query'}, 'twitterUsers': {'name': 'twitterUsers', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchAdd(self, inputName, inputsGroupId, searchQuery, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            geocodeLatitude: (number): geocodeLatitude
            geocodeLongitude: (number): geocodeLongitude
            geocodeRadius: (number): geocodeRadius
            geocodeUnit: (string): geocodeUnit
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            lang: (string): lang
            locale: (string): locale
            resultType: (string): resultType
            searchQuery: (string): searchQuery

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'geocodeLatitude': {'name': 'geocodeLatitude', 'required': False, 'in': 'query'}, 'geocodeLongitude': {'name': 'geocodeLongitude', 'required': False, 'in': 'query'}, 'geocodeRadius': {'name': 'geocodeRadius', 'required': False, 'in': 'query'}, 'geocodeUnit': {'name': 'geocodeUnit', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'lang': {'name': 'lang', 'required': False, 'in': 'query'}, 'locale': {'name': 'locale', 'required': False, 'in': 'query'}, 'resultType': {'name': 'resultType', 'required': False, 'in': 'query'}, 'searchQuery': {'name': 'searchQuery', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/search/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchEdit(self, inputId, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            geocodeLatitude: (number): geocodeLatitude
            geocodeLongitude: (number): geocodeLongitude
            geocodeRadius: (number): geocodeRadius
            geocodeUnit: (string): geocodeUnit
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            lang: (string): lang
            locale: (string): locale
            resultType: (string): resultType
            searchQuery: (string): searchQuery

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'geocodeLatitude': {'name': 'geocodeLatitude', 'required': False, 'in': 'query'}, 'geocodeLongitude': {'name': 'geocodeLongitude', 'required': False, 'in': 'query'}, 'geocodeRadius': {'name': 'geocodeRadius', 'required': False, 'in': 'query'}, 'geocodeUnit': {'name': 'geocodeUnit', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'lang': {'name': 'lang', 'required': False, 'in': 'query'}, 'locale': {'name': 'locale', 'required': False, 'in': 'query'}, 'resultType': {'name': 'resultType', 'required': False, 'in': 'query'}, 'searchQuery': {'name': 'searchQuery', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/search/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/search/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchParameters(self):
        """Return RSS bundle parameters list."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/twitter/search/parameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/search/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/search/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterSearchStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/search/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def twitterStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/twitter/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerAdd(self, inputName, inputsGroupId, processPagesVia, seed, **kwargs):
        """Create new input for inputsGroup.

        Args:
            acceptLanguage: (string): Custom acceptLanguage.
            cookie: (string): Custom cookie.
            crawlDelay: (number): Wait this many seconds between each URL crawled from a single IP address. Specify the number of seconds as an integer or floating-point number (e.g., crawlDelay=0.25).
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            maxHops: (integer): Limit the depth of your crawl.
            maxRounds: (integer): Specify the maximum number of crawl repeats. By default (maxRounds=0) repeating crawls will continue indefinitely.
            maxToCrawl: (integer): Specify max pages to spider. Default: 100,000.
            maxToProcess: (integer): Specify max pages to process through "processPagesVia" parameter. Default: 100,000.
            obeyRobots: (boolean): Ignore a site's robots.txt instructions.
            onlyProcessIfNew: (boolean): By default repeat crawls will only process new (previously unprocessed) pages.
            pageProcessPatterns: (array): Specify strings to limit pages processed to those whose HTML contains any of the content strings.
            processPagesVia: (string): The Analyze API automatically identifies and extracts articles, images and product pages.
            referer: (string): Custom referer.
            repeat: (number): Specify the number of days as a floating-point (e.g. repeat=7.0) to repeat this crawl. By default crawls will not be repeated.
            restrictDomain: (boolean): Allow limited crawling across subdomains/domains.
            seed: (string): Seed URL.
            urlCrawlPatterns: (array): Only crawl URLs that contain any of these text strings (one per line).
            urlCrawlRegEx: (string): Only crawl URLs matching the regular expression..
            urlProcessPatterns: (array): Only process URLs that contain any of the text strings (one per line).
            urlProcessRegEx: (string): Only process URLs matching the regular expression.
            useCanonical: (boolean): Skip pages with a differing canonical URL.
            useProxies: (boolean): Force proxy IPs.
            userAgent: (string): Custom User Agent.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'acceptLanguage': {'name': 'acceptLanguage', 'required': False, 'in': 'query'}, 'cookie': {'name': 'cookie', 'required': False, 'in': 'query'}, 'crawlDelay': {'name': 'crawlDelay', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'maxHops': {'name': 'maxHops', 'required': False, 'in': 'query'}, 'maxRounds': {'name': 'maxRounds', 'required': False, 'in': 'query'}, 'maxToCrawl': {'name': 'maxToCrawl', 'required': False, 'in': 'query'}, 'maxToProcess': {'name': 'maxToProcess', 'required': False, 'in': 'query'}, 'obeyRobots': {'name': 'obeyRobots', 'required': False, 'in': 'query'}, 'onlyProcessIfNew': {'name': 'onlyProcessIfNew', 'required': False, 'in': 'query'}, 'pageProcessPatterns': {'name': 'pageProcessPatterns', 'required': False, 'in': 'query'}, 'processPagesVia': {'name': 'processPagesVia', 'required': True, 'in': 'query'}, 'referer': {'name': 'referer', 'required': False, 'in': 'query'}, 'repeat': {'name': 'repeat', 'required': False, 'in': 'query'}, 'restrictDomain': {'name': 'restrictDomain', 'required': False, 'in': 'query'}, 'seed': {'name': 'seed', 'required': True, 'in': 'query'}, 'urlCrawlPatterns': {'name': 'urlCrawlPatterns', 'required': False, 'in': 'query'}, 'urlCrawlRegEx': {'name': 'urlCrawlRegEx', 'required': False, 'in': 'query'}, 'urlProcessPatterns': {'name': 'urlProcessPatterns', 'required': False, 'in': 'query'}, 'urlProcessRegEx': {'name': 'urlProcessRegEx', 'required': False, 'in': 'query'}, 'useCanonical': {'name': 'useCanonical', 'required': False, 'in': 'query'}, 'useProxies': {'name': 'useProxies', 'required': False, 'in': 'query'}, 'userAgent': {'name': 'userAgent', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerEdit(self, inputId, seed, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            acceptLanguage: (string): Custom acceptLanguage.
            cookie: (string): Custom cookie.
            crawlDelay: (number): Wait this many seconds between each URL crawled from a single IP address. Specify the number of seconds as an integer or floating-point number (e.g., crawlDelay=0.25).
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            maxHops: (integer): Limit the depth of your crawl.
            maxRounds: (integer): Specify the maximum number of crawl repeats. By default (maxRounds=0) repeating crawls will continue indefinitely.
            maxToCrawl: (integer): Specify max pages to spider. Default: 100,000.
            maxToProcess: (integer): Specify max pages to process through "processPagesVia" parameter. Default: 100,000.
            obeyRobots: (boolean): Ignore a site's robots.txt instructions.
            onlyProcessIfNew: (boolean): By default repeat crawls will only process new (previously unprocessed) pages.
            pageProcessPatterns: (array): Specify strings to limit pages processed to those whose HTML contains any of the content strings.
            processPagesVia: (string): The Analyze API automatically identifies and extracts articles, images and product pages.
            referer: (string): Custom referer.
            repeat: (number): Specify the number of days as a floating-point (e.g. repeat=7.0) to repeat this crawl. By default crawls will not be repeated.
            restrictDomain: (boolean): Allow limited crawling across subdomains/domains.
            seed: (string): Seed URL.
            urlCrawlPatterns: (array): Only crawl URLs that contain any of these text strings (one per line).
            urlCrawlRegEx: (string): Only crawl URLs matching the regular expression..
            urlProcessPatterns: (array): Only process URLs that contain any of the text strings (one per line).
            urlProcessRegEx: (string): Only process URLs matching the regular expression.
            useCanonical: (boolean): Skip pages with a differing canonical URL.
            useProxies: (boolean): Force proxy IPs.
            userAgent: (string): Custom User Agent.

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'acceptLanguage': {'name': 'acceptLanguage', 'required': False, 'in': 'query'}, 'cookie': {'name': 'cookie', 'required': False, 'in': 'query'}, 'crawlDelay': {'name': 'crawlDelay', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'maxHops': {'name': 'maxHops', 'required': False, 'in': 'query'}, 'maxRounds': {'name': 'maxRounds', 'required': False, 'in': 'query'}, 'maxToCrawl': {'name': 'maxToCrawl', 'required': False, 'in': 'query'}, 'maxToProcess': {'name': 'maxToProcess', 'required': False, 'in': 'query'}, 'obeyRobots': {'name': 'obeyRobots', 'required': False, 'in': 'query'}, 'onlyProcessIfNew': {'name': 'onlyProcessIfNew', 'required': False, 'in': 'query'}, 'pageProcessPatterns': {'name': 'pageProcessPatterns', 'required': False, 'in': 'query'}, 'processPagesVia': {'name': 'processPagesVia', 'required': False, 'in': 'query'}, 'referer': {'name': 'referer', 'required': False, 'in': 'query'}, 'repeat': {'name': 'repeat', 'required': False, 'in': 'query'}, 'restrictDomain': {'name': 'restrictDomain', 'required': False, 'in': 'query'}, 'seed': {'name': 'seed', 'required': True, 'in': 'query'}, 'urlCrawlPatterns': {'name': 'urlCrawlPatterns', 'required': False, 'in': 'query'}, 'urlCrawlRegEx': {'name': 'urlCrawlRegEx', 'required': False, 'in': 'query'}, 'urlProcessPatterns': {'name': 'urlProcessPatterns', 'required': False, 'in': 'query'}, 'urlProcessRegEx': {'name': 'urlProcessRegEx', 'required': False, 'in': 'query'}, 'useCanonical': {'name': 'useCanonical', 'required': False, 'in': 'query'}, 'useProxies': {'name': 'useProxies', 'required': False, 'in': 'query'}, 'userAgent': {'name': 'userAgent', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerParameters(self):
        """Return Website Crawler parameters."""

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/parameters'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def websiteCrawlerStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/websiteCrawler/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def wordpressAdd(self, inputName, inputsGroupId, wordpressBlogUrl, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            wordpressBlogUrl: (string): WordPress blog URL

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'wordpressBlogUrl': {'name': 'wordpressBlogUrl', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/wordpress/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def wordpressEdit(self, inputId, wordpressBlogUrl, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            wordpressBlogUrl: (string): WordPress blog URL

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'wordpressBlogUrl': {'name': 'wordpressBlogUrl', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/wordpress/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def wordpressList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/wordpress/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def wordpressRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/wordpress/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def wordpressRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/wordpress/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def wordpressStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/wordpress/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def yelpBusinessReviewsAdd(self, inputName, inputsGroupId, yelpBusinessesSearchLocation, **kwargs):
        """Create new input for inputsGroup.

        Args:
            description: (string): description
            inputName: (string): Can be any text.
            inputsGroupId: (string): inputsGroupId
            isRunning: (boolean): isRunning
            yelpBusinessesSearchLocation: (string): Required if either latitude or longitude is not provided. Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.
            yelpBusinessesSearchMaxNumberOfBusinessesToFetch: (integer): Max number of businesses to fetch per businesses search
            yelpBusinessesSearchRadius: (integer): Optional. Search radius in meters. The max value is 40000 meters (25 miles).
            yelpBusinessesSearchTerm: (string): Optional. Search term (e.g. "food", "restaurants"). If term isnt included we search everything. The term keyword also accepts business names such as "Starbucks".

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputName': {'name': 'inputName', 'required': True, 'in': 'query'}, 'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'yelpBusinessesSearchLocation': {'name': 'yelpBusinessesSearchLocation', 'required': True, 'in': 'query'}, 'yelpBusinessesSearchMaxNumberOfBusinessesToFetch': {'name': 'yelpBusinessesSearchMaxNumberOfBusinessesToFetch', 'required': False, 'in': 'query'}, 'yelpBusinessesSearchRadius': {'name': 'yelpBusinessesSearchRadius', 'required': False, 'in': 'query'}, 'yelpBusinessesSearchTerm': {'name': 'yelpBusinessesSearchTerm', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/yelpBusinessReviews/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def yelpBusinessReviewsEdit(self, inputId, yelpBusinessesSearchLocation, **kwargs):
        """Edit existing inputsGroup for project.

        Args:
            description: (string): description
            inputId: (string): inputId
            isRunning: (boolean): isRunning
            yelpBusinessesSearchLocation: (string): Required if either latitude or longitude is not provided. Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.
            yelpBusinessesSearchMaxNumberOfBusinessesToFetch: (integer): Max number of businesses to fetch per businesses search
            yelpBusinessesSearchRadius: (integer): Optional. Search radius in meters. The max value is 40000 meters (25 miles).
            yelpBusinessesSearchTerm: (string): Optional. Search term (e.g. "food", "restaurants"). If term isnt included we search everything. The term keyword also accepts business names such as "Starbucks".

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'description': {'name': 'description', 'required': False, 'in': 'query'}, 'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'yelpBusinessesSearchLocation': {'name': 'yelpBusinessesSearchLocation', 'required': True, 'in': 'query'}, 'yelpBusinessesSearchMaxNumberOfBusinessesToFetch': {'name': 'yelpBusinessesSearchMaxNumberOfBusinessesToFetch', 'required': False, 'in': 'query'}, 'yelpBusinessesSearchRadius': {'name': 'yelpBusinessesSearchRadius', 'required': False, 'in': 'query'}, 'yelpBusinessesSearchTerm': {'name': 'yelpBusinessesSearchTerm', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/yelpBusinessReviews/edit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def yelpBusinessReviewsList(self, inputsGroupId):
        """Return the list of inputs for inputsGroup.

        Args:
            inputsGroupId: (string): inputsGroupId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputsGroupId': {'name': 'inputsGroupId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/yelpBusinessReviews/list'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def yelpBusinessReviewsRemove(self, inputId):
        """Remove existing input.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/yelpBusinessReviews/remove'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def yelpBusinessReviewsRetrieve(self, inputId):
        """Return the input with specified ID.

        Args:
            inputId: (string): inputId

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/yelpBusinessReviews/retrieve'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)

    def yelpBusinessReviewsStatus(self, inputId, isRunning):
        """Set existing input status for project.

        Args:
            inputId: (string): inputId
            isRunning: (boolean): isRunning

        Consumes:
            application/json

        Returns:
            application/json;charset=UTF-8
        """

        all_api_parameters = {'inputId': {'name': 'inputId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/inputs/yelpBusinessReviews/status'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._process_api(self._controller_name, api, actions, params, data, consumes)
