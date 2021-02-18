import ioc
import uvicorn

import frf
from frf import AnonymousResource
from frf import get_asgi_application


class TemplateService:

    async def render_to_string(self, template_name, ctx):
        return template_name


class SinglePageApplication(AnonymousResource):

    @frf.spa('dashboard.html.j2')
    async def dashboard(self):
        return {}


app = get_asgi_application(allowed_hosts=['*'])
app.add_resource(SinglePageApplication)


if __name__ == '__main__':
    ioc.provide('TemplateService', TemplateService())
    ioc.provide('APIMetadataService', frf.services.APIMetadataService())
    uvicorn.run(app, host="127.0.0.1", port=8000)
