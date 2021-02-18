"""Web dashboard for playing soundboard content."""

from flask import Flask
from flask.templating import render_template
from whitenoise import WhiteNoise

from sinusboard import client

app = Flask(__name__)


@app.route("/")
def index():
    """Route for the dashboard template."""
    return render_template("index.html", clips=client.CLIPS)


@app.route("/service-worker.js")
def service_worker():
    return app.send_static_file("service-worker.js")


@app.route("/play/<uuid:uuid>")
def play(uuid: str):
    return client.play_clip(uuid)


app.wsgi_app = WhiteNoise(app.wsgi_app, root="sinusboard/server/static/")