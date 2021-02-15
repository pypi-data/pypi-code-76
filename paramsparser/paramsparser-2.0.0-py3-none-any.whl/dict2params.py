from paramsparser.json2params import Json2Params

class Dict2Params(Json2Params):
    def __init__(self, params:dict) -> None:
        super(Dict2Params, self).__init__(params=params)
