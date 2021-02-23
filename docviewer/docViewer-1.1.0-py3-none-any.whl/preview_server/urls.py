from tornado.web import StaticFileHandler
from . import config, web, websocket

raw_file_config = {'path': config.DOC_ROOT}

urlpatterns = [
    (r'/_raw/(.*)', StaticFileHandler, raw_file_config, 'raw-file'),
    (r'/lite-preview', web.LitePreview),
    (r'/ws/preview', websocket.Preview),
]
