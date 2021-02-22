from datetime import datetime

from fastapi import Request, Response

from fastapi.routing import APIRoute
from typing import Callable

from magicapi.Models.Call import make_call_from_request_and_response
from magicapi.Models.task_executor import save_tasks

from magicapi.Services.Sentry import HAS_SENTRY_DSN, capture_exception

from magicapi.Errors import IgnoreException


class MagicCallLogger(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = None
            error = None
            time_received = datetime.utcnow()
            try:
                response: Response = await original_route_handler(request)
            except IgnoreException as e:
                raise e
            except Exception as e:
                if HAS_SENTRY_DSN:
                    capture_exception(e)
                if "aws.context" in request.scope:
                    context = request.scope["aws.context"]
                    if hasattr(context, "serverless_sdk"):
                        context.serverless_sdk.capture_exception(e)
                print("Error in call route", e.__dict__)
                error = e
            time_done = datetime.utcnow()
            delta = time_done - time_received
            secs_took = delta.seconds + delta.microseconds / 1_000_000
            times = {
                "time_received": time_received,
                "time_done": time_done,
                "secs_took": secs_took,
            }
            await make_call_from_request_and_response(request, response, error, times)
            if error:
                try:
                    save_tasks()
                except Exception as save_task_error:
                    print("[ERROR] save task error", save_task_error)
                raise error
            return response

        return custom_route_handler
