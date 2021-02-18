"""Declares :class:`OIDCProvider`."""
import fastapi
import frf


class TokenEndpoint(frf.AnonymousResource):
    default_provider = 'default'

    async def list(self):
        return await self.retrieve('default')

    @frf.action(name='token', detail=True, methods=['post'])
    async def token(self, resource_id: str, request: fastapi.Request):
        pass



if __name__ == '__main__':
    import uvicorn
    app = frf.get_asgi_application(allowed_hosts=["*"])
    app.add_resource(TokenEndpoint, '')
    uvicorn.run(app, host="127.0.0.1", port=8000)
