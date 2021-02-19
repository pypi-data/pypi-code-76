import json
import tempfile
import logging
import requests
from .settings import DAPENG_INSTANCE
LOGGER = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)


class JobNotExists(Exception):
    pass


class DapengAPI(object):

    DAPENG_TASK_STATUS = {
        0: "",
        1: "Waiting",
        2: "Building",
        3: "Running",
        4: "Finished",
        5: "Stopped"
    }

    DAPENG_HOST = "10.192.225.198"
    DAPENG_JOB_URL = "http://%s/api/request/" % DAPENG_HOST
    DAPENG_TASK_URL = "http://%s/api/testcase/" % DAPENG_HOST
    DAPENG_STATE_EXCHANGE = "dapeng.dapeng.state"
    DAPENG_LOG_EXCHANGE = "dapeng_log_exchange"

    @staticmethod
    def setup_instance(server_type):
        if not server_type:
            server_type = 'prod1'
        instance = DAPENG_INSTANCE.get(server_type)
        dapeng_host = instance.get("ip")
        DapengAPI.DAPENG_HOST = dapeng_host
        DapengAPI.DAPENG_STATE_EXCHANGE = instance.get("state_exchange")
        DapengAPI.DAPENG_JOB_URL = "http://%s/api/request/" % dapeng_host
        DapengAPI.DAPENG_TASK_URL = "http://%s/api/testcase/" % dapeng_host

    @staticmethod
    def get_job(job_id, needall=False):
        """Get job/request info"""

        params = {
            "id": job_id,
            "needall": str(needall).lower()
        }
        info = None
        resp = requests.get(DapengAPI.DAPENG_JOB_URL, params=params)
        if resp.status_code == 404:
            raise JobNotExists("Job: %s is not exists!" % job_id)

        if resp.status_code == 200:
            info = resp.json()

        return info

    @staticmethod
    def get_testcase(case_id, args=None):
        """Get testcase info"""

        info = None
        params = {"id": case_id}
        if args:
            params.update(args)
        resp = requests.get(DapengAPI.DAPENG_TASK_URL, params)
        if resp.status_code == 404:
            raise JobNotExists("Testcase: %s is not exists!" % case_id)

        if resp.status_code == 200:
            info = resp.json()

        if not info:
            raise JobNotExists("Testcase [%s] does not exists" % case_id)
        return info

    @staticmethod
    def stop_job(job_id):
        """Stop job/request"""

        LOGGER.info('=> Test job is stopping: %s', job_id)
        post_value = {"id": job_id, "action": 'stop'}
        response = requests.post(DapengAPI.DAPENG_JOB_URL, data=post_value)
        response.raise_for_status()

    @staticmethod
    def rerun_testcase(job_id, case_id):
        params = {
            "id": job_id,
            "action": "rerun",
            "subtasks": case_id
        }
        response = requests.post(DapengAPI.DAPENG_JOB_URL, data=params)
        if response.status_code == 404:
            raise JobNotExists("Job: %s is not exists!" % job_id)
        response.raise_for_status()
        print (response.content)
        LOGGER.info("Successfully rerun testcase: %s.", case_id)

    @staticmethod
    def submit_job(job_config):
        """Submit a new job on Dapeng"""

        assert isinstance(job_config, dict)
        is_run_type = False

        if "header" in job_config:
            is_run_type = True
            url = "http://%s/newRequest/" % DapengAPI.DAPENG_HOST
            with tempfile.TemporaryFile() as outfile:
                outfile.write(json.dumps(job_config).encode())
                outfile.seek(0)
                kwargs = {
                    "files": {"requestconfigfile": outfile},
                    "data": None,
                    "timeout": 120
                }
                response = requests.post(url, **kwargs)
        else:
            url = "http://%s/api/new_job/" % DapengAPI.DAPENG_HOST
            parameters = {
                "jsondata": json.dumps(job_config),
            }
            response = requests.post(url, parameters)

        response.raise_for_status()
        if is_run_type:
            ret = response.json()
            if ret['status'] in (True, 'true'):
                LOGGER.info("Submit: %s!", ret['message'])
                job_url = "http://%s/request/%s/testcases/" % (DapengAPI.DAPENG_HOST, ret['id'])
                LOGGER.info("Job can be found at: http://%s/request/%s/testcases/",
                            DapengAPI.DAPENG_HOST, ret['id'])
                return ret["id"], job_url
            else:
                LOGGER.error("Submit: %s!", ret['message'])
                exit(1)
        else:
            LOGGER.info("Submit success!")


