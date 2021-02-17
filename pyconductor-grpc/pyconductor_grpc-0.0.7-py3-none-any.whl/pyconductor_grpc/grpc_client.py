from multiprocessing import pool
import os
import socket
from threading import Thread
import time
import typing

import grpc

from pyconductor_grpc.conductor_grpc import (
    task_service_pb2_grpc,
    task_service_pb2,
    workflow_service_pb2_grpc,
    workflow_service_pb2,
)
from pyconductor_grpc.model import (
    startworkflowrequest_pb2,
    taskresult_pb2,
)


default_worker_id = socket.gethostname()


class ClientBase(object):
    def __init__(self, connection_uri: str = None, channel: grpc.Channel = None):
        if not channel:
            if not connection_uri:
                connection_uri = os.getenv("CONDUCTOR_SERVER_URL", "localhost:8090")
            self._channel = grpc.insecure_channel(connection_uri)
        else:
            self._channel = channel


class WorkflowService(ClientBase):
    def __init__(self, connection_uri: str = None, channel: grpc.Channel = None):
        super(WorkflowService, self).__init__(connection_uri, channel)
        self.stub = workflow_service_pb2_grpc.WorkflowServiceStub(self._channel)

    def start_workflow(
        self,
        name: str,
        version: int = 0,
        correlation_id: str = "",
        input: typing.Mapping[str, object] = None,
        # task_to_domain: typing.Mapping[str, str] = None,
        # workflow_def: WorkflowDefinition = None,
        # external_input_payload_storage_path: str = "",
        priority: int = 1,
    ) -> workflow_service_pb2.StartWorkflowResponse:
        if input is None:
            input = dict()
        return self.stub.StartWorkflow(
            startworkflowrequest_pb2.StartWorkflowRequest(
                name=name,
                version=version,
                correlation_id=correlation_id,
                input=input,
                priority=priority,
            )
        )

    def get_workflow_status(
        self,
        workflow_id: str,
        include_tasks=True,
    ) -> workflow_service_pb2.GetWorkflowStatusResponse:
        return self.stub.GetWorkflowStatus(
            workflow_service_pb2.GetWorkflowStatusRequest(
                workflow_id=workflow_id,
                include_tasks=include_tasks,
            )
        )


class TaskService(ClientBase):
    def __init__(self, connection_uri: str = None, channel: grpc.Channel = None):
        super(TaskService, self).__init__(connection_uri, channel)
        self.stub = task_service_pb2_grpc.TaskServiceStub(self._channel)

    def poll(
        self, task_type: str, worker_id: str = default_worker_id, domain: str = None
    ):
        return self.stub.Poll(
            task_service_pb2.PollRequest(
                task_type=task_type, worker_id=worker_id, domain=domain
            )
        )

    def batch_poll(
        self,
        task_type: str,
        count: int = None,
        timeout: int = None,
        worker_id: str = default_worker_id,
        domain: str = None,
    ):
        return self.stub.BatchPoll(
            task_service_pb2.BatchPollRequest(
                task_type=task_type,
                worker_id=worker_id,
                domain=domain,
                count=count,
                timeout=timeout,
            )
        )

    def ack_task(self, task_id: str, worker_id: str = default_worker_id):
        return self.stub.AckTask(
            task_service_pb2.AckTaskRequest(task_id=task_id, worker_id=worker_id)
        )

    def update_task(self, result):
        return self.stub.UpdateTask(task_service_pb2.UpdateTaskRequest(result=result))

    def execute(self, task, exec_function):
        task_result = taskresult_pb2.TaskResult()
        task_result.workflow_instance_id = task.workflow_instance_id
        task_result.task_id = task.task_id
        task_result.callback_after_seconds = 0
        task_result.worker_id = task.worker_id
        try:
            resp = exec_function(task)
            if type(resp) is not dict or not all(
                key in resp for key in ("output", "logs")
            ):
                raise Exception(
                    "Task execution function MUST return a response as a dict with output and logs fields"
                )

            task_result.status = 3  # COMPLETED
            task_result.output_data["output"].struct_value.update(resp["output"])
            task_result.output_message.value = bytes(resp["logs"], "utf-8")
            if "reasonForIncompletion" in resp:
                task["reasonForIncompletion"] = resp["reasonForIncompletion"]
        except Exception as err:
            print(
                f"Error executing task: {exec_function.__name__} with error: {str(err)}"
            )
            task_result.status = 1  # FAILED
            task_result.output_message.value = bytes(
                f"Error executing task: {exec_function.__name__} with error: {str(err)}",
                "utf-8",
            )
        finally:
            self.update_task(task_result)

    def poll_and_execute(
        self, task_type: str, exec_function, polling_interval: float, domain: str = None
    ):
        while True:
            time.sleep(polling_interval)
            polled = self.poll(task_type, domain=domain)
            if polled and polled.task and polled.task.task_id:
                self.ack_task(polled.task.task_id)
                self.execute(polled.task, exec_function)

    def startPool(
        self,
        task_type: str,
        exec_function,
        thread_count: int,
        polling_interval: float,
        wait: bool = False,
        domain: str = None,
    ):
        print(
            "Polling for task %s at a %f ms interval with %d threads for task execution, with worker id as %s"
            % (
                task_type,
                polling_interval * 1000,
                thread_count,
                default_worker_id,
            )
        )
        with pool.ThreadPool(thread_count) as tp:
            job_results = []
            while True:
                for job in job_results:
                    if job._number_left == 0:
                        job_results.remove(job)
                running_jobs = sum([job._number_left for job in job_results])
                poll_amount = thread_count - running_jobs
                print(f"looking for {poll_amount} jobs")
                polled = self.batch_poll(
                    task_type, poll_amount, timeout=1, domain=domain
                )
                tasks = []
                while 1:
                    try:
                        tasks.append((polled.next(), self, exec_function))
                    except StopIteration:
                        break
                    except Exception:
                        continue
                print(f" found {len(tasks)} jobs")
                if tasks:
                    job_results.append(tp.map_async(ack_and_execute, tasks))
                else:
                    time.sleep(float(polling_interval))

    def start(
        self,
        task_type: str,
        exec_function,
        thread_count: int,
        polling_interval: float,
        wait: bool = False,
        domain: str = None,
    ):
        print(
            "Polling for task %s at a %f ms interval with %d threads for task execution, with worker id as %s"
            % (
                task_type,
                polling_interval * 1000,
                thread_count,
                default_worker_id,
            )
        )
        for x in range(0, int(thread_count)):
            thread = Thread(
                target=self.poll_and_execute,
                args=(
                    task_type,
                    exec_function,
                    polling_interval,
                    domain,
                ),
            )
            thread.daemon = True
            thread.start()
        if wait:
            while 1:
                time.sleep(1)


def ack_and_execute(args):
    task, taskClient, exec_function = args
    taskClient.ack_task(task.task_id)
    taskClient.execute(task, exec_function)
