# get the version number defined in setup.py
import pkg_resources
__version__ = pkg_resources.get_distribution("ps.herald").version

import os
from ps.basic import Config

from flask import Flask

# graphql
from flask_graphql import GraphQLView as View
from ps.herald.graph_ql.schema import schema
# needed to integrate java_script/angular apps
from flask_cors import CORS


def create_app(name, have_config_file=False, test_config=None):
    # create and configure the app
    here = os.path.dirname(os.path.realpath(__file__))
    app = Flask(
        name,
        instance_relative_config=True,
        template_folder=os.path.join(here, "templates"),
        static_folder=os.path.join(here, "static"),
    )

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        if app.config["TESTING"]:
            Config.reset_singleton()

    CORS(app)

    # initialize ps.basic and the database file used by flask
    Config.Basic(name, have_config_file=have_config_file)
    app.config["DATABASE"] = Config.herald_sqlite_filename
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True

    # initialize the database used 
    from . import database
    database.init_app(app)

    # add the "bare_html" access to ps_herald
    from . import bare_html_api
    app.register_blueprint(bare_html_api.bp)
    app.add_url_rule("/", endpoint="index")

    # add the "angular" access to ps_herald
    from . import angular_api
    app.register_blueprint(angular_api.bp, url_prefix="/angular")

    # Add graphQl support 
    #https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tips/#querying
    from ps.herald.model import Base
    from ps.herald.database import get_session
    with app.app_context():
        session = get_session()
        Base.query = session.query_property()
    app.add_url_rule(
        "/graph_ql",
        view_func=View.as_view("graphql", graphiql=True, schema=schema))

    return app
