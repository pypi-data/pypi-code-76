from datetime import datetime, timedelta
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

import sqlalchemy

from ps.basic import Config
from ps.herald import __version__
from ps.herald.model import Log
from ps.herald.database import get_session


bp = Blueprint("angular_api", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    session = get_session()
    return render_template("angular_api/index.html")


import sys, traceback


@bp.errorhandler(400)
def internal_error(exception):
    print("400 error caught")
    etype, value, tb = sys.exc_info()
    print(traceback.print_exception(etype, value, tb))


@bp.errorhandler(500)
def internal_error(exception):
    print("500 error caught")
    etype, value, tb = sys.exc_info()
    print(traceback.print_exception(etype, value, tb))


@bp.route("/list", methods=["GET"])
def list():
    session = get_session()
    query_parameters = request.args
    query_obj = session.query(Log)
    if query_parameters["system_id"] != "not_selected":
        query_obj = query_obj.filter(
            Log.system_id == query_parameters["system_id"]
        )
    if query_parameters["sub_system_id"] != "not_selected":
        query_obj = query_obj.filter(
            Log.sub_system_id == query_parameters["sub_system_id"]
        )
    if query_parameters["sub_sub_system_id"] != "not_selected":
        query_obj = query_obj.filter(
            Log.sub_sub_system_id == query_parameters["sub_sub_system_id"]
        )
    if query_parameters["user_spec_1"] != "not_selected":
        query_obj = query_obj.filter(
            Log.user_spec_1 == query_parameters["user_spec_1"]
        )
    if query_parameters["user_spec_2"] != "not_selected":
        query_obj = query_obj.filter(
            Log.user_spec_2 == query_parameters["user_spec_2"]
        )
    if query_parameters["produkt_id"] != "not_selected":
        query_obj = query_obj.filter(
            Log.produkt_id == query_parameters["produkt_id"]
        )
    if query_parameters["pattern"] != "not_selected":
        query_obj = query_obj.filter(
            Log.message.like("%%%s%%" % (query_parameters["pattern"]))
            | Log.funcname.like("%%%s%%" % (query_parameters["pattern"]))
            | Log.module.like("%%%s%%" % (query_parameters["pattern"]))
        )
    if query_parameters["starting_at"] != "not_selected":
        query_obj = query_obj.filter(
            Log.created >= query_parameters["starting_at"]
        )
    if query_parameters["notify_level"] != "not_selected":
        query_obj = query_obj.filter(
            Log.levelno >= int(query_parameters["notify_level"])
        )

    if query_parameters["order"] == "asc":
        ordered_by_expr = sqlalchemy.sql.expression.asc(Log.created)
    else:
        ordered_by_expr = sqlalchemy.sql.expression.desc(Log.created)

    if query_parameters["num_records"] != "not_selected":
        rows = (
            query_obj.order_by(ordered_by_expr)
            .limit(int(query_parameters["num_records"]))
            .all()
        )
    else:
        rows = query_obj.order_by(ordered_by_expr).all()

    k = [l.as_dict() for l in rows]
    return jsonify([l.as_dict() for l in rows])


@bp.route("/options", methods=["GET"])
def options():
    session = get_session()
    Config.logger.debug("got request", extra={"package_version": __version__})
    res = {}
    res["produkt_ids"] = [
        x[0] for x in session.query(Log.produkt_id).distinct().all()
    ]
    res["produkt_ids"].append("not_selected")
    res["system_ids"] = [
        x[0] for x in session.query(Log.system_id).distinct().all()
    ]
    res["system_ids"].append("not_selected")
    res["sub_system_ids"] = [
        x[0] for x in session.query(Log.sub_system_id).distinct().all()
    ]
    res["sub_system_ids"].append("not_selected")
    res["sub_sub_system_ids"] = [
        x[0] for x in session.query(Log.sub_sub_system_id).distinct().all()
    ]
    res["sub_sub_system_ids"].append("not_selected")
    res["user_spec_1s"] = [
        x[0] for x in session.query(Log.user_spec_1).distinct().all()
    ]
    res["user_spec_1s"].append("not_selected")
    res["user_spec_2s"] = [
        x[0] for x in session.query(Log.user_spec_2).distinct().all()
    ]
    res["user_spec_2s"].append("not_selected")

    return jsonify(res)


@bp.route("/hello")
def hello():
    msg = "Hello Angular World called"
    return msg


@bp.route("/hello_to_ps_basic_logger")
def hello_to_ps_basic_logger():
    msg = "Hello Angular World called"
    Config.logger.info(msg)
    return msg
