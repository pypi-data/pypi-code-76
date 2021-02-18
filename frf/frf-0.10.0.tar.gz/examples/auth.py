import uvicorn
from frf import Resource
from frf import get_asgi_application


class AuthenticatedThing(Resource):
    authentication_classes = [None]
    required_scopes = ['thing.get']
    allow_cookie_auth = True

    async def retrieve(self, request, resource_id: int):
        return {

            "id": resource_id,
            "message": "Hello world!",
            'claims': request.state.claims.as_dict()
        }

    async def list(self):
        return [
            {"message": "First item in a list of AuthenticatedThing!"},
            {"message": "Second item in a list of AuthenticatedThing!"},
        ]


app = get_asgi_application(allowed_hosts=['*'])
app.add_resource(AuthenticatedThing)

if __name__ == '__main__':
    uvicorn.run('auth:app', host="127.0.0.1", port=8000, reload=True)
