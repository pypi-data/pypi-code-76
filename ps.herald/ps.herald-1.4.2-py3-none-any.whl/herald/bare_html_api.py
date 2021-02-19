from datetime import datetime, timedelta
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

# from werkzeug.exceptions import abort

import sqlalchemy

from ps.basic import Config
from ps.herald import __version__
from ps.herald.model import Log
from ps.herald.database import get_session


bp = Blueprint("bare_html_api", __name__)


@bp.route("/rm_logs", methods=["GET"])
def rm_logs():
    session = get_session()
    Config.logger.debug(
        "got request to rm logentries", extra={"package_version": __version__}
    )
    # 30 days before Today
    start_date = str(datetime.now() - timedelta(days=30))
    deleted = session.query(Log).filter(Log.created < start_date).delete()
    Config.logger.debug(
        f"deleted {deleted} Logs ", extra={"package_version": __version__}
    )

    session.commit()
    return redirect(url_for("bare_html_api.index"))


@bp.route("/", methods=["GET", "POST"])
def index():
    session = get_session()
    Config.logger.debug("got request", extra={"package_version": __version__})
    if request.method == "POST":
        set_search_params(request)

    pids = session.query(Log.produkt_id).distinct().all() + [("not_selected",)]
    pid_options = [
        isset(row[0], SEARCH_ATTRIBUTES["PRODUKT_ID"]) for row in pids
    ]
    sids = session.query(Log.system_id).distinct().all() + [("not_selected",)]
    system_id_options = [
        isset(row[0], SEARCH_ATTRIBUTES["SYSTEM_ID"]) for row in sids
    ]
    sub_sids = session.query(Log.sub_system_id).distinct().all() + [
        ("not_selected",)
    ]
    sub_system_id_options = [
        isset(row[0], SEARCH_ATTRIBUTES["SUB_SYSTEM_ID"]) for row in sub_sids
    ]
    sub_sub_sids = session.query(Log.sub_sub_system_id).distinct().all() + [
        ("not_selected",)
    ]
    sub_sub_system_id_options = [
        isset(row[0], SEARCH_ATTRIBUTES["SUB_SUB_SYSTEM_ID"])
        for row in sub_sub_sids
    ]
    u1s = session.query(Log.user_spec_1).distinct().all() + [("not_selected",)]
    user_spec_1_id_options = [
        isset(row[0], SEARCH_ATTRIBUTES["USER_SPEC_1"]) for row in u1s
    ]
    u2s = session.query(Log.user_spec_2).distinct().all() + [("not_selected",)]
    user_spec_2_id_options = [
        isset(row[0], SEARCH_ATTRIBUTES["USER_SPEC_2"]) for row in u2s
    ]

    pattern = SEARCH_ATTRIBUTES["pattern"]
    starting_at = SEARCH_ATTRIBUTES["starting_at"]
    notify_level = SEARCH_ATTRIBUTES["notify_level"]
    max_rows = SEARCH_ATTRIBUTES["max_rows"]
    old_row_first = SEARCH_ATTRIBUTES["old_row_first"]

    query_obj = session.query(Log)
    if SEARCH_ATTRIBUTES["PRODUKT_ID"] != "not_selected":
        query_obj = query_obj.filter(
            Log.produkt_id == SEARCH_ATTRIBUTES["PRODUKT_ID"]
        )
    if SEARCH_ATTRIBUTES["SYSTEM_ID"] != "not_selected":
        query_obj = query_obj.filter(
            Log.system_id == SEARCH_ATTRIBUTES["SYSTEM_ID"]
        )
    if SEARCH_ATTRIBUTES["SUB_SYSTEM_ID"] != "not_selected":
        query_obj = query_obj.filter(
            Log.sub_system_id == SEARCH_ATTRIBUTES["SUB_SYSTEM_ID"]
        )
    if SEARCH_ATTRIBUTES["SUB_SUB_SYSTEM_ID"] != "not_selected":
        query_obj = query_obj.filter(
            Log.sub_sub_system_id == SEARCH_ATTRIBUTES["SUB_SUB_SYSTEM_ID"]
        )
    if SEARCH_ATTRIBUTES["USER_SPEC_1"] != "not_selected":
        query_obj = query_obj.filter(
            Log.user_spec_1 == SEARCH_ATTRIBUTES["USER_SPEC_1"]
        )
    if SEARCH_ATTRIBUTES["USER_SPEC_2"] != "not_selected":
        query_obj = query_obj.filter(
            Log.user_spec_2 == SEARCH_ATTRIBUTES["USER_SPEC_2"]
        )
    if SEARCH_ATTRIBUTES["pattern"] != "not_selected":
        query_obj = query_obj.filter(
            Log.message.like("%%%s%%" % (SEARCH_ATTRIBUTES["pattern"]))
            | Log.funcname.like("%%%s%%" % (SEARCH_ATTRIBUTES["pattern"]))
            | Log.module.like("%%%s%%" % (SEARCH_ATTRIBUTES["pattern"]))
        )
    if SEARCH_ATTRIBUTES["starting_at"] != "not_selected":
        query_obj = query_obj.filter(
            Log.created >= SEARCH_ATTRIBUTES["starting_at"]
        )
    if SEARCH_ATTRIBUTES["notify_level"] != "not_selected":
        query_obj = query_obj.filter(
            Log.levelno >= int(SEARCH_ATTRIBUTES["notify_level"])
        )
    if SEARCH_ATTRIBUTES["old_row_first"] == "asc":
        ordered_by_expr = sqlalchemy.sql.expression.asc(Log.created)
    else:
        ordered_by_expr = sqlalchemy.sql.expression.desc(Log.created)

    if SEARCH_ATTRIBUTES["max_rows"] != "not_selected":
        records = (
            query_obj.order_by(ordered_by_expr)
            .limit(int(SEARCH_ATTRIBUTES["max_rows"]))
            .all()
        )
    else:
        records = query_obj.order_by(ordered_by_expr).all()

    k = locals()
    k.pop("self", None)
    return render_template("bare_html_api/index.html", **k)
    # return render_template("index.html" )

    return "Hello, World!"


@bp.route("/hello")
def hello():
    return "Hello, World!"


@bp.route("/hello_to_ps_basic_logger")
def hello_to_ps_basic_logger():
    Config.logger.info("Hello World called")
    return "Hello, World!"


AVAILABLE_SEARCH_ATTRIBUTES = [
    "PRODUKT_ID",
    "SYSTEM_ID",
    "SUB_SYSTEM_ID",
    "SUB_SUB_SYSTEM_ID",
    "USER_SPEC_1",
    "USER_SPEC_2",
    "pattern",
    "starting_at",
    "notify_level",
    "max_rows",
    "old_row_first",
    "max_rows",
]

SEARCH_ATTRIBUTES = {}
for attribute in AVAILABLE_SEARCH_ATTRIBUTES:
    SEARCH_ATTRIBUTES[attribute] = "not_selected"
SEARCH_ATTRIBUTES["max_rows"] = "50"


def set_search_params(request):
    for attribute in AVAILABLE_SEARCH_ATTRIBUTES:
        new_value = request.form[attribute].strip()
        if new_value != "not_selected" and new_value != "":
            SEARCH_ATTRIBUTES[attribute] = new_value
        else:
            SEARCH_ATTRIBUTES[attribute] = "not_selected"


def isset(param1, param2):
    if str(param1) == str(param2):
        return {"value": param1, "selected": True}
    return {"value": param1, "selected": False}
