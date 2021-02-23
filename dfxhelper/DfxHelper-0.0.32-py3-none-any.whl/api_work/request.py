from dfx_utils.api_work.settings import ApiSetting


class Request:
    def __init__(self, session, setting: ApiSetting):
        """
        :session: requests.session or aiohttp.ClientSession instance
        """
        self.session = session
        self.setting = setting

    def post_sync(self):
        param, header, data = self.setting()
        return self.session.post(self.setting.request_url, params=param, headers=header, json=data, verify=False)

    async def post_async(self):
        param, header, data = self.setting()
        return await self.session.post(self.setting.request_url, params=param, headers=header, json=data, ssl=False)

    def get_sync(self):
        param, header, data = self.setting()
        return self.session.get(self.setting.request_url, params=param, headers=header, json=data, verify=False)

    async def get_async(self):
        param, header, data = self.setting()
        return await self.session.get(self.setting.request_url, params=param, headers=header, json=data, ssl=False)

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __call__(self, sync=True):
        method_f = getattr(self, f'{self.setting.method}_{"sync" if sync else "async"}', None)
        if method_f:
            return method_f()
        else:
            raise Exception(f'method error {self.setting.method}')
