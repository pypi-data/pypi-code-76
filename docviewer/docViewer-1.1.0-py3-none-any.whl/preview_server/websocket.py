from pathlib import Path

from tornado.ioloop import PeriodicCallback
import tornado.websocket

from docViewer.render import render_file


class BasePreview(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_file_callback = None

    @property
    def is_running(self):
        return self.ws_connection and not self.ws_connection.is_closing()

    def start_render_file_callback(self):
        self.last_render_time = 0
        self.render_file_callback = PeriodicCallback(
            self.render_file,
            1 * 1000,
        )
        self.render_file_callback.start()

    def stop_render_file_callback(self):
        if self.render_file_callback:
            self.render_file_callback.stop()
            self.render_file_callback = None

    async def open(self):
        filename = self.get_argument('filename', default=None)
        if not filename:
            await self.write_message('filename not provided')
            return self.close()
        self.filepath = Path(self.application.settings['DOC_ROOT'], filename)
        if not self.filepath.exists():
            await self.write_message('file not exists')
            return self.close()
        await self.write_message('start now')
        self.start_render_file_callback()

    def on_close(self):
        self.stop_render_file_callback()

    async def render_file(self):
        raise NotImplementedError()


class Preview(BasePreview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_file_callback = None

    async def render_file(self):
        if not self.is_running:
            return self.stop_render_file_callback()
        if not self.filepath.exists():
            self.write_message('file has been removed')
            self.close()
        update_time = self.filepath.stat().st_mtime
        if update_time > self.last_render_time:
            self.last_render_time = update_time
            rendered_content = render_file(self.filepath)
            await self.write_message(rendered_content)
