import logging
import os
import time
from logstash_async.handler import AsynchronousLogstashHandler
from egune.interfaces import ActorMessage, ActorResponse, Interface, UserMessage
from typing import Callable, Dict, Any, List


logger = logging.getLogger('')


def init_logger(config):
    global logger
    logger = logging.getLogger(config["name"])
    logger.setLevel(logging.INFO)
    if config["host"] == "HOST":
        config["host"] = os.environ["HOST"]
    logger.addHandler(AsynchronousLogstashHandler(
        config["host"],
        config["port"],
        None
    ))
    logger.info(f"Started {config['name']}", extra={
        "log_event": "system started"
    })


def user_message_log(func: Callable[[UserMessage], UserMessage]):
    def wrapper(data: Dict[str, Any]) -> Dict[str, Any]:
        s = time.time()
        try:
            result = func(UserMessage.from_dict(data)).to_dict()
            logger.info("Processed", extra={
                "log_event": "processed",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": result,
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed", extra={
                "log_event": "process failed",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": e,
                "time": time.time() - s
            })
            return data
    return wrapper


def cd_user_message_log(func: Callable[[UserMessage], List[Interface]]):
    def wrapper(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        s = time.time()
        try:
            result = [c.to_dict() for c in func(UserMessage.from_dict(data))]
            logger.info("Processed User message", extra={
                "log_event": "user message",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": result,
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed User message", extra={
                "log_event": "user message failed",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": e,
                "time": time.time() - s
            })
            return []
    return wrapper


def cd_actor_response_log(func: Callable[[ActorResponse], List[Interface]]):
    def wrapper(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        s = time.time()
        try:
            result = [c.to_dict() for c in func(ActorResponse.from_dict(data))]
            logger.info("Processed User message", extra={
                "log_event": "user message",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": result,
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed User message", extra={
                "log_event": "user message failed",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": e,
                "time": time.time() - s
            })
            return []
    return wrapper


def egune_response_log(func: Callable[[ActorMessage], ActorMessage]):
    def wrapper(data: Dict[str, Any]) -> Dict[str, Any]:
        s = time.time()
        try:
            result = func(ActorMessage.from_dict(data)).to_dict()
            logger.info("Processed User message", extra={
                "log_event": "user message",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": result,
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed User message", extra={
                "log_event": "user message failed",
                "user_id": data["user_id"],
                "process_input": data,
                "process_output": e,
                "time": time.time() - s
            })
            return data
    return wrapper
