import uvicorn
from frf import AnonymousResource
from frf import get_asgi_application


class Thing(AnonymousResource):

    async def retrieve(self, request, resource_id: int):
        return {

            "id": resource_id,
            "message": "Hello world!"
        }

    async def list(self):
        return [
            {"message": "First item in a list of Thing!"},
            {"message": "Second item in a list of Thing!"},
        ]


app = get_asgi_application(allowed_hosts=['*'])
app.add_resource(Thing)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
