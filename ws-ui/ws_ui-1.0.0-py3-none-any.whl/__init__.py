import asyncio
import sys
import time

from prompt_toolkit.application import Application as PTApplication
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import SearchToolbar, TextArea
from tornado.websocket import websocket_connect, WebSocketClosedError


class Application:
    help_text = 'Enter msg and press Enter to send message\n'

    def __init__(self, input_field_height=2, input_field_prompt='> '):
        self.ws = None
        self.output_field = TextArea(text=self.help_text)
        self.search_field = SearchToolbar()
        self.input_field = TextArea(
            height=input_field_height,
            prompt='',
            search_field=self.search_field,
            multiline=False,
            wrap_lines=False,
        )
        self.input_field.accept_handler = self.input_accept_handler
        self.container = HSplit([
            self.output_field,
            Window(height=1, char='-'), self.input_field, self.search_field
        ])
        self.kb = KeyBindings()
        self.load_key_bindings()
        self.tui = PTApplication(
            layout=Layout(self.container, focused_element=self.input_field),
            key_bindings=self.kb,
            mouse_support=True,
            full_screen=True,
        )

    def input_accept_handler(self, buff):
        if self.ws:
            asyncio.create_task(self.ws_write(self.input_field.text))
        else:
            self.update_output('websocket already closed')

    def update_output(self, output, msg_type='*'):
        current_time = time.strftime('%H:%M:%S')
        output = f'{msg_type} {[current_time]} {output}'
        new_text = self.output_field.text + '\n' + output
        self.output_field.buffer.document = Document(
            text=new_text,
            cursor_position=len(new_text),
        )

    async def ws_write(self, msg):
        try:
            await self.ws.write_message(msg)
            self.update_output(msg, '⬆️')
        except WebSocketClosedError:
            self.update_output('websocket already closed', 'x')
            self.ws = None

    def load_key_bindings(self):
        @self.kb.add('c-c')
        @self.kb.add('c-q')
        def _(event):
            event.app.exit()

    async def create_websocket(self, url):
        self.update_output(f'connecting to {url}')
        try:
            self.ws = await websocket_connect(url)
            self.update_output('connected', msg_type='👌')
            asyncio.create_task(self.ws_recv_and_output())
        except ConnectionError:
            self.update_output('connection refused')
        except Exception as err:
            msg = f'{type(err).__name__}: {err}'
            self.update_output(msg, msg_type='x')

    async def ws_recv_and_output(self):
        while True:
            msg = await self.ws.read_message()
            if msg is None:
                self.ws = None
                self.update_output('websocket is closed', 'x')
                break
            self.update_output(msg, msg_type='⬇️')

    async def close_websocket(self):
        if self.ws:
            await self.ws.close()
        self.ws = None

    async def main(self):
        try:
            url = sys.argv[1]
        except IndexError:
            sys.stderr.write('please provide websocket url\n')
            return
        await self.create_websocket(url)
        await self.tui.run_async()
