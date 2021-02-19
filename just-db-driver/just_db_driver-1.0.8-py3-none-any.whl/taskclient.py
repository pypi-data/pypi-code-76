import json
import requests

from just.justerror import JustError
from just.realtime_task_param import RealtimeTaskParam
from just.offline_task_param import OfflineTaskParam
from just.justclient import JustClient


class TaskClient:
    """
    Task客户端
    date: 2020-10-15 11:00
    """
    TASK_URI_PREFIC = '/just-task-client/api/v1'

    def __init__(self, driver_url, public_key, secret_key,
                 project_name="default"):
        """
        初始化函数
        :param driver_url: JUST域名
        :param public_key: 公钥
        :param secret_key: 秘钥
        :param project_name: 项目名，为null的话会创建一个default的项目名
        """
        self.driver_url =\
            driver_url if driver_url[-1] != '/' else driver_url[:-1]
        self.public_key = public_key
        self.secret_key = secret_key

        self._token_header = {"username": None}
        self._check_and_get_token()
        # Project ID 设置
        self.project_id = self.get_or_create_project(project_name)

    def _check_and_get_token(self):
        key_dict = {
            "publicKey": self.public_key,
            "secretKey": self.secret_key
        }
        token = self._post("/api/sdk/token-check", key_dict)
        self._token_header['username'] = token

    def get_or_create_project(self, project_name):
        """
        1.获取项目列表【项目列表接口】
        2.如果项目不存在，创建一个【项目添加接口】，返回ID
        3.否则直接返回ID
        :param project_name 项目名
        :return 项目ID
        """
        assert isinstance(project_name, str), "project_name应该被设置为string值"
        project_id = None
        res = self._task_get("/projects?projectName=" + project_name)
        if (res is None or len(res) == 0):
            new_project_setting = {
                "projectName": project_name
            }
            new_res = self._task_post("/projects", new_project_setting)
            project_id = new_res[0]["projectId"]
        else:
            project_id = res[0]["projectId"]
            # pass
        return project_id

    def submit_realtime_task(self, realtime_param):
        """
        提交实时任务

        1.【任务添加接口】，获得taskBasicId
        2.【实时任务编辑接口】
        3.【任务启动接口】
        """
        assert isinstance(realtime_param, RealtimeTaskParam),\
            "请输入RealtimeTaskParam对象作为参数"
        # 1.
        task_id = self._add_task(realtime_param.task_name, "realtime")
        # 2.
        self._task_post("/tasks/" + str(task_id) + "/realtime",
                        realtime_param.task_flow_param)
        # 3.
        self._task_post("/tasks/" + str(task_id) + "/start", None)

        return task_id

    def submit_offline_task(self, offline_param):
        """
        提交离线任务
        1.【任务添加接口】，获得taskBasicId
        2.【离线任务编辑接口】编辑任务必选项
        3.【任务flow保存接口】提交任务
        4.【任务启动接口】
        """
        assert isinstance(offline_param, OfflineTaskParam),\
            "请输入OfflineTaskParam对象作为参数"
        self._check_db(offline_param.db_name)
        # 1.
        task_id = self._add_task(offline_param.task_name, "offline")
        assert task_id > 0, "任务添加失败"
        # 2.
        self._task_post("/tasks/" + str(task_id) +
                        "/offline", offline_param.task_edit_param)
        # 3.
        task_flow_param = offline_param.task_flow_param
        task_flow_param["taskBasicId"] = task_id
        self._task_post("/tasks/" + str(task_id) + "/flow", task_flow_param)
        # 4.
        self._task_post("/tasks/" + str(task_id) + "/start", None)
        return task_id

    def get_task_status(self, task_id):
        """根据任务ID获取状态，自动区分实时和离线"""
        assert isinstance(task_id, int), "Task ID 需要为整数"
        try:
            return self._get_task_remote(task_id, "/offline")
        except Exception:
            return self._get_task_remote(task_id, "/realtime")

    def kill_task(self, task_id):
        self._task_post("/tasks/" + str(task_id) + "/stop", None)
        return True

    def get_task_log(self, task_id):
        """
        根据任务ID获取任务日志
        离线任务的日志只有执行完了才能获取
        离线的：
        1.先要调用【执行记录列表接口】获得执行列表，获取第一个项
        2.再调用【离线任务执行记录job列表接口】获得job列表,取top 1
        3.再调用【job日志接口】获取日志
        实时的没有第二步
        :param task_id 任务ID
        :return 全部日志文本
        """
        task_status = self.get_task_status(task_id)
        # 1.
        task_execute_list_uri = "/tasks/" + str(task_id) +\
            "/executions?taskType=" + task_status["task_type"].lower()
        task_execute_list_dict = self._task_get(task_execute_list_uri)
        assert len(task_execute_list_dict) > 0, "获取执行列表失败"

        task_list = task_execute_list_dict["pageList"]
        assert task_list is not None and len(task_list) > 0,\
            "不存在任务执行记录，请检查任务是否已经执行"
        latest_task = task_list[0]
        exec_id = latest_task["execId"]

        if task_status["task_type"] == "OFFLINE":
            # 2.
            job_list_uri = "/jobs/offline?taskBasicId=" +\
                str(task_id) + "&execId=" + str(exec_id)
            job_list_dict = self._task_get(job_list_uri)
            assert job_list_dict is not None and len(job_list_dict) > 0,\
                "不存在任务JOB，请检查是否执行过"
            job_id = job_list_dict[0]["jobId"]
            # 3.
            job_log_uri = "/jobs/offline/log?jobId=" + str(job_id) +\
                "&execId=" + str(exec_id)
            job_log_dict = self._task_get(job_log_uri)
            assert job_log_dict is not None, "获取日志异常"
            return job_log_dict["log"]
        elif task_status["task_type"] == "REALTIME":
            # 3.
            job_log_uri = "/jobs/realtime/log?execId=" + str(exec_id)
            job_log_dict = self._task_get(job_log_uri)
            assert job_log_dict is not None, "获取日志异常"
            return job_log_dict["log"]

        raise JustError("获取日志失败")

    def _get_task_remote(self, task_id, online_offline):
        res_dict = self._task_get("/tasks/" + str(task_id) + online_offline)
        assert len(res_dict) > 0, "任务不存在"  # 返回空dict
        return {
            "task_name": res_dict["taskName"],
            "task_type": res_dict["taskType"].upper(),
            "task_status": res_dict["taskStatus"].upper()
        }

    def _check_db(self, db_name):
        """检查指定db是否创建"""
        try:
            df_db = JustClient(self.public_key,
                               self.secret_key, self.driver_url).list_db()
            assert [db_name] in df_db.values, "数据库不合法"
        except Exception:
            raise Exception()

    def _add_task(self, task_name, task_type):
        add_task_settings = {
            "projectId": self.project_id,
            "taskName": task_name,
            "taskType": task_type
        }
        res = self._task_post("/tasks", add_task_settings)
        return res["taskBasicId"]

    def _task_get(self, uri):
        return self._get(self.TASK_URI_PREFIC + uri)

    def _task_post(self, uri, data):
        return self._post(self.TASK_URI_PREFIC + uri, data)

    def _sdk_post(self, uri, data):
        return self._post(self.driver_url + uri, data)

    def _post(self, uri, data):
        """执行POST request，同时检测异常状态，返回response data"""
        headers = {}
        headers.update(self._token_header)
        headers.update({"Content-type": "application/json"})
        url = self.driver_url + uri
        try:
            response = requests.post(url, json=data, headers=headers)
            return self._process_http_response(response)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def _get(self, uri):
        """执行GET request，同时检测异常状态，返回response data"""
        header = self._token_header
        url = self.driver_url + uri
        try:
            response = requests.get(url, headers=header)
            return self._process_http_response(response)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def _process_http_response(self, response):
        """检测HTTP response的结果，如果有异常报错，没有则返回data"""
        response.encoding = 'utf-8'
        result_string = response.text
        result_dict = json.loads(result_string)
        result_code = result_dict['resultCode']
        if result_code != 200:
            result_msg = result_dict['resultMsg']
            raise JustError(result_msg)
        return result_dict['data']
