import os
import yaml
import json
from urllib.parse import urljoin
import logging

import requests
from fastutils import fsutils
from fastutils import dictutils
from fastutils import logutils
from fastutils import sysutils

logger = logging.getLogger(__name__)

def load_config(config_path):
    settings = {
        "cronfile-for-agent": "/etc/cron.d/django-crontab-agent",
        "cronfile-for-schedules": "/etc/cron.d/django-crontab-schedules",
        "schedules": "/etc/django-crontab-agent/schedules/",
        "django-crontab-agent-command": "django-crontab-agent",
        "schedule-exec-command": "{django_crontab_agent_command} exec -c {config} {schedule} >> /dev/null 2>&1",
        "cronjob-for-agent": "* * * * * root {django_crontab_agent_command} sync -c {config} >> /dev/null 2>&1",
        "logfile": "/var/log/django-crontab-agent.log",
        "loglevel": "DEBUG",
        "server-codes-file": "/etc/django-crontab-agent/server-code.txt",
        "schedule-task-codes-file": "/etc/django-crontab-agent/schedule-task-codes.txt",
        "workspace": "/tmp/",
        "server-address": None,
        "server-name": None,
        "server-aclkey": None,
    }
    settings["config"] = os.path.abspath(config_path)
    custom_settings = yaml.safe_load(fsutils.readfile(config_path, default="{}"))
    if custom_settings and isinstance(custom_settings, dict):
        settings.update(custom_settings)
    return settings

def do_schedule_exec(config, schedule):
    settings = load_config(config)
    logutils.setup(**settings)
    workspace = settings["workspace"]

    schedules_root = settings["schedules"]
    filepath = os.path.join(schedules_root, schedule)
    schedule_settings = json.loads(fsutils.readfile(filepath, default="{}"))

    workspace = os.path.join(workspace, schedule)
    script = schedule_settings["script"]
    code, stdout, stderr = sysutils.execute_script(script, workspace)
    logger.info("schedule {} execute result: code={}, stdout={}, stderr={}".format(schedule, code, stdout, stderr))
    reportRunResult(settings, schedule, code, stdout, stderr)

def do_install(config):
    settings = load_config(config)
    logutils.setup(**settings)
    cronfile_for_agent_file = settings["cronfile-for-agent"]
    config = settings["config"]
    django_crontab_agent_command = settings["django-crontab-agent-command"]
    cronjob_for_agent = settings["cronjob-for-agent"] + "\n"
    text = cronjob_for_agent.format(django_crontab_agent_command=django_crontab_agent_command, config=config)
    fsutils.write(cronfile_for_agent_file, text)
    logger.info("cronfile-for-agent: {} updated...".format(cronfile_for_agent_file))
    do_sync(config)

def do_reset_crontfile(config):
    settings = load_config(config)
    logutils.setup(**settings)
    local_server_codes_file = settings["server-codes-file"]
    local_server_codes_json = fsutils.readfile(local_server_codes_file, default="{}")
    local_server_codes = json.loads(local_server_codes_json)
    do_schedules_cronfile_update(settings, list(local_server_codes.keys()))
    logger.info("cronfile-for-schedules: {} updated...".format(settings["cronfile-for-schedules"]))

def do_sync(config):
    """Do agent settings sync from manager server.
    """
    settings = load_config(config)
    logutils.setup(**settings)
    server_codes = {}

    try:
        logger.info("Calling api to get server settings...")
        server_codes = getServerSettings(settings)
    except Exception as error:
        logger.exception("getServerSettings failed, settings={}".format(settings))
        os.sys.exit(1)

    local_server_codes_file = settings["server-codes-file"]
    local_server_codes_json = fsutils.readfile(local_server_codes_file, default="{}")
    local_server_codes = json.loads(local_server_codes_json)

    created_key, updated_keys, deleted_keys = dictutils.diff(local_server_codes, server_codes)

    for schedule_uid in created_key:
        do_schedule_update(settings, schedule_uid)
    for schedule_uid in updated_keys:
        do_schedule_update(settings, schedule_uid)
    for schedule_uid in deleted_keys:
        do_schedule_delete(settings, schedule_uid)

    if created_key or updated_keys or deleted_keys:
        logger.info("Find server setting changes...")
        do_schedules_cronfile_update(settings, list(server_codes.keys()))
        fsutils.write(local_server_codes_file, json.dumps(server_codes, indent=4, ensure_ascii=False))
    else:
        logger.info("NO server setting change.")
    
def do_schedules_cronfile_update(settings, schedule_uids):
    schedules_root = settings["schedules"]
    config = settings["config"]
    django_crontab_agent_command = settings["django-crontab-agent-command"]
    lines = []
    for schedule_uid in schedule_uids:
        filepath = os.path.join(schedules_root, schedule_uid)
        schedule_settings = json.loads(fsutils.readfile(filepath, default="{}"))
        title = schedule_settings.get("title", "")
        schedule = schedule_settings.get("schedule", None)
        user = schedule_settings.get("user", None)
        cmd = settings["schedule-exec-command"].format(django_crontab_agent_command=django_crontab_agent_command, config=config, schedule=schedule_uid)
        if schedule and user and cmd:
            lines.append("# schedule uid={}".format(schedule_uid))
            lines.append("# {}".format(title))
            lines.append("{} {} {}".format(schedule, user, cmd))
            lines.append("")
    cronfile_text = "\n".join(lines)
    fsutils.write(settings["cronfile-for-schedules"], cronfile_text)

def do_schedule_update(settings, schedule):
    schedule_settings = getScheduleSettings(settings, schedule)
    schedule_settings_json = json.dumps(schedule_settings, indent=4, ensure_ascii=False)
    schedules_root = settings["schedules"]
    filepath = os.path.join(schedules_root, schedule)
    fsutils.write(filepath, schedule_settings_json)

def do_schedule_delete(settings, schedule):
    schedules_root = settings["schedules"]
    filepath = os.path.join(schedules_root, schedule)
    fsutils.rm(filepath)

def getServerSettings(settings):
    address = settings["server-address"]
    server = settings["server-name"]
    aclkey = settings["server-aclkey"]

    url = urljoin(address, "getServerSettings")
    params = {
        "server": server,
        "aclkey": aclkey,
    }
    logger.debug("getScheduleSettings, url={}, params={}".format(url, params))
    response = requests.get(url, params=params)
    logger.debug(response.content)
    response_data = json.loads(response.content)
    return response_data["result"]

def getScheduleSettings(settings, schedule):
    address = settings["server-address"]
    server = settings["server-name"]
    aclkey = settings["server-aclkey"]

    url = urljoin(address, "./getScheduleSettings")
    params = {
        "server": server,
        "aclkey": aclkey,
        "schedule": schedule,
    }
    logger.debug("getScheduleSettings, url={}, params={}".format(url, params))
    response = requests.get(url, params=params)
    logger.debug(response.content)
    response_data = json.loads(response.content)
    return response_data["result"]

def reportRunResult(settings, schedule, code, stdout, stderr):
    address = settings["server-address"]
    server = settings["server-name"]
    aclkey = settings["server-aclkey"]

    url = urljoin(address, "./reportRunResult")
    data = {
        "server": server,
        "aclkey": aclkey,
        "schedule": schedule,
        "code": code,
        "stdout": stdout,
        "stderr": stderr,
    }
    logger.debug("reportRunResult, url={}, data={}".format(url, data))
    response = requests.get(url, json=data)
    logger.debug(response.content)
    response_data = json.loads(response.content)
    return response_data["result"]
