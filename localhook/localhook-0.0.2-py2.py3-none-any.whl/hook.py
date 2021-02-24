import logging
from time import strftime

import click
from flask import Flask, jsonify, make_response, request
from flask.views import MethodView
from pyngrok import conf, ngrok
from rich.console import Console
from waitress import serve

console = Console(width=60)


class HookAPI(MethodView):
    def get(self):
        return make_response(jsonify({"about": "Local Hook"}), 200)

    def post(self):
        body = request.get_json()
        console.print(f"webhook arrived", style="bold white on blue", justify="center")
        console.print(body, style="frame")
        return make_response(jsonify(body), 200)


class LocalHook:
    def __init__(self, port=9090, auth_token=None, region="us") -> None:
        self.port = port
        self.auth_token = auth_token
        self.region = region

    def _get_public_url(self):

        conf.get_default().region = self.region

        if self.auth_token:
            ngrok.set_auth_token(self.auth_token)

        url = ngrok.connect(self.port).public_url
        return url

    def create_app(self):
        url = self._get_public_url()
        app = Flask(__name__)
        log = logging.getLogger("werkzeug")
        log.disabled = True
        app.config["BASE_URL"] = url
        app.add_url_rule("/", view_func=HookAPI.as_view("webhooks"))
        return app, url

    def listen(self):
        app, url = self.create_app()
        console.print(
            "Webhooks Delivered Locally", style="bold green", justify="center"
        )
        console.print(f" :tada: Ready to receive webhooks on terminal", ":thumbs_up:")
        console.print(f" :tada: Set your webhook URL as {url}")
        console.print(f" :tada: Traffic stats available on http://127.0.0.1:4040")
        serve(app, port=self.port, _quiet=True)


@click.command()
@click.option("--port", default=9090, help="server port")
@click.option("--auth_token", default=None, help="ngrok auth_token")
@click.option("--region", default="us", help="ngrok region")
def start(port, auth_token, region):
    hook = LocalHook(port=port, auth_token=auth_token, region=region)
    hook.listen()
