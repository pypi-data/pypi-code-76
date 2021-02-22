from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

from lilili import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)

from .db.defs import Session
from .db.helpers import query_library_by_name

webapp = Flask(__title__)
webapp.config["JSON_AS_ASCII"] = False


@webapp.route("/")
def root():
    return jsonify(
        {
            "name": __title__,
            "description": __description__,
            "version": __version__,
            "author": f"{__author__} <{__author_email__}>",
            "license": __license__,
            "copyright": __copyright__,
            "homepage": __url__,
        }
    )


@webapp.route("/search")
def get_search_result():
    raise NotImplementedError


@webapp.route("/libraries")
def get_libraries():
    name = request.args.get("name", None)
    if name is None:
        raise BadRequest("Parameter `name` is required.")

    session = Session()
    libraries = query_library_by_name(session, name)
    session.close()

    return jsonify({"name": name, "libraries": libraries})


@webapp.after_request
def edit_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@webapp.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": e.name, "details": e.description}), e.code
