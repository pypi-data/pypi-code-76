class APIHelperCallAPI:
    """
    The class is used to mock the call API which in turn calls the `requests`
    get, post, patch, put and delete methods
    """

    def __init__(self, body_json):
        """
        We initialize the class
        """
        self._json = body_json

    def json(self):
        """
        The method is called in the actual implementation to get the json
        form of the response object
        """
        return self._json

    def raise_for_status(self):
        return None


# Test constants
ASSET_LIST_GET = [{"id": 1, "name": "Asset_name", "edge_connectors": [1, 2]}]
TAG_LIST_GET = [{"id": 1, "name": "Tag1", "short_name": "Short Tag1", "edge_connector": 1, "asset": 1}]
TAG_DATA_POST = {"columns": [1], "index": [1,2,3], "data": [[2], [3], [4]], "count": 1, "offset": 0}
SINGLE_ASSET_GET = {"id": 2, "name": "Asset_name2", "edge_connectors": [1, 2]}
