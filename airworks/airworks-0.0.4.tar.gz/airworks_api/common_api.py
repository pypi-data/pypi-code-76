import json

from airworks_api.base_api import BaseApi


class CommonApi(BaseApi):
    base_url = "aw-airworks-frontend:30000"

    app_method = "GET"
    app_id = "1"
    app_url = "api_gateway/api/1/baymax"
    app_key = "1eaacd7e-7898-41f5-849e-67d5f290b1bf"
    app_secret = "847ed3d7-aed7-4271-8cd2-924a46efdb00"
    query_builder = """"""

    def api_response(
        self,
        country,
        id,
        page_size=100,
        page_num=1,
    ):
        return super(CommonApi, self).api_response(
            country=country,
            id=id,
            page_size=page_size,
            page_num=page_num,
            __query_builder__=self.query_builder,
        )


if __name__ == "__main__":
    api_result = CommonApi().api_response(
        country='中国',
        id=None,
        page_size=10,
    )
    print(json.dumps(api_result, indent=2, ensure_ascii=False))
