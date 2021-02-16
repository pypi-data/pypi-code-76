class OrderlyWebResponseError(Exception):
    def __init__(self, response):
        self.response = response
        json = response.json()
        msg = "An OrderlyWeb error occurred"
        if "errors" in json and len(json["errors"]) > 0:
            error = json["errors"][0]
            if "message" in error:
                msg = error["message"]
            elif "code" in error:
                msg = error["code"]

        super(Exception, self).__init__(msg)
