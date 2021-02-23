import os

from flask import Flask

from reusingintent.server.celery.init import celery
from reusingintent.server.celery.utils import configure_celery
from reusingintent.server.paths import DATABASE_ROOT
from reusingintent.server.routes.install_routes import installRoutes

app = Flask(__name__)


def checkAndInitalizeDatabaseFolder():
    if not os.path.exists(DATABASE_ROOT):
        os.mkdir(DATABASE_ROOT)


def start_server():
    checkAndInitalizeDatabaseFolder()
    installRoutes(app)
    configure_celery(celery, app)
    app.run(host="0.0.0.0")
