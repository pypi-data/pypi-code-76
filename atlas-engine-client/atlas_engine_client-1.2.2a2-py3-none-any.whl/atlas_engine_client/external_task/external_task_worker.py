import asyncio
import inspect
import logging
import traceback

from ..core import BaseClient, LoopHelper
from .functional_error import FunctionalError


logger = logging.getLogger(__name__)


class ExternalTaskWorker(BaseClient):

    ADDITIONAL_LOCK_DURATION = (100 * 1000) - 100
    EXTEND_LOCK_TIMEOUT = (100 * 1000)
    
    def __init__(self, url, session, identity, loop_helper, handler, external_task, options={}):
        super(ExternalTaskWorker, self).__init__(url, session, identity)
        self._loop_helper = loop_helper
        self._handler = handler
        self._external_task = external_task
        self._payload = self._external_task.get('payload', {})
        self._options = options

    def __with_external_task_param(self):

        def is_handler_a_func(func):
            spec = inspect.getfullargspec(func)
            is_func = inspect.isroutine(func)

            result = (len(spec.args) == 2 and is_func)

            return result

        def is_handler_callable(caller):
            spec = inspect.getfullargspec(caller)
            is_func = inspect.isroutine(caller)

            result = (len(spec.args) == 3 and not is_func)

            return result

        return is_handler_a_func(self._handler) or is_handler_callable(self._handler)

    async def start(self):

        async def extend_lock_task_wrapper():
            worker_id = self._external_task['workerId']
            external_task_id = self._external_task['id']

            additional_duration = self._options.get("additional_lock_duration", ExternalTaskWorker.ADDITIONAL_LOCK_DURATION)

            await self.extend_lock(worker_id, external_task_id, additional_duration)

        extend_lock_timeout = self._options.get("extend_lock_timeout", ExternalTaskWorker.EXTEND_LOCK_TIMEOUT)

        options = {'delay': extend_lock_timeout}
        extend_lock = self._loop_helper.register_background_task(extend_lock_task_wrapper, **options)
        
        external_task_id = self._external_task['id']
        logger.info(f"starting external task '{external_task_id}'")

        try:
            result = None
            
            if asyncio.iscoroutinefunction(self._handler):
                if self.__with_external_task_param():
                    result = await self._handler(self._payload, self._external_task)
                else:
                    result = await self._handler(self._payload)
            else:
                if self.__with_external_task_param():
                    result = self._handler(self._payload, self._external_task)
                else:
                    result = self._handler(self._payload)

            await self.__finish_task_successfully(result)
        except FunctionalError as fe:
            logger.warning(f"Finish external task with functional error (code: {fe.get_code()}, message: {fe.get_message()})")
            await self.__finish_task_with_functional_errors(fe.get_code(), fe.get_message())

        except Exception as e:
            formatted_lines = traceback.format_exc().splitlines()
            logger.error(f"Finish external task with technial error ({str(e)} -> {formatted_lines})")
            await self.__finish_task_with_technical_errors(str(e), str(formatted_lines))
        finally:
            self._loop_helper.unregister_background_task(extend_lock, "extend_lock background task")
            logger.info(f"finish external task '{external_task_id}'")

    async def extend_lock(self, worker_id, external_task_id, additional_duration):
        path = f"/atlas_engine/api/v1/external_tasks/{external_task_id}/extend_lock"

        request = {
            "workerId": worker_id,
            "additionalDuration": additional_duration
        }

        await self.do_post(path, request)

    async def __finish_task_successfully(self, result):
        logger.info(f"finish task {self._external_task['id']} successfully.")
        path = f"/atlas_engine/api/v1/external_tasks/{self._external_task['id']}/finish"

        payload = {
            "workerId": self._external_task['workerId'],
            "result": result
        }

        result = await self.do_put(path, payload)
        logger.debug(f"finished task {self._external_task['id']} successfully.")

    async def __finish_task_with_functional_errors(self, error_code, error_message):
        logger.warn(f"finished external task_with functional errors '{self._external_task}', '{error_code}', '{error_message}'.")
        path = f"/atlas_engine/api/v1/external_tasks/{self._external_task['id']}/handle_bpmn_error"

        payload = {
            "workerId": self._external_task['workerId'],
            "bpmnError": {
                "errorCode": error_code,
                "errorMessage": error_message
            }
        }

        await self.do_put(path, payload)

    async def __finish_task_with_technical_errors(self, error_message, error_details):
        logger.warn(f"finished task with technical errors '{self._external_task}', '{error_message}', '{error_details}'.")
        path = f"/atlas_engine/api/v1/external_tasks/{self._external_task['id']}/handle_service_error"

        payload = {
            "workerId": self._external_task['workerId'],
            "error": {
                "errorMessage": error_message,
                "errorDetails": error_details
            }
        }

        await self.do_put(path, payload)
