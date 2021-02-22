"""Utility functions for RPAListener."""
import re
from typing import List


def stage_is_transactional(task) -> bool:
    return task.tags.match("repeat")


def get_error_handler_from_tags(tags: List) -> str:
    """ Looks for explicit error handler given in test tag prefixed `error_handler=`"""
    try:
        explicit_error_handler = next(filter(lambda tag: tag.startswith("error_handler="), tags))
        return explicit_error_handler.split("=")[1]
    except StopIteration:
        return None


def test_timed_out(result):
    if result.timeout:
        return result.timeout.timed_out()
    else:
        return None
