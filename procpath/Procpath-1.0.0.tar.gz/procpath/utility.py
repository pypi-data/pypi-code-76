import logging
import os
import platform
import resource
import subprocess


__all__ = 'evaluate', 'get_meta'

logger = logging.getLogger(__package__)


def evaluate(var_cmd_list) -> dict:
    """Evaluate given 2-tuple named list of shell commands."""

    script = []
    var_set = set()
    for var_name, command in var_cmd_list:
        var_set.add(var_name)
        script.append(f'{var_name}=$({command})')
        script.append(f'export {var_name}')

    script.append('env')
    env = subprocess.check_output('\n'.join(script), shell=True, encoding='utf-8')

    result = {}
    for line in env.splitlines():
        k, v = line.split('=', 1)
        if k in var_set:
            result[k] = v
            if not v:
                logger.warning('Variable %s evaluated empty', k)
            if len(result) == len(var_set):
                break

    return result


def get_meta() -> dict:
    """Get machine metadata."""

    return {
        'platform_node': platform.node(),
        'platform_platform': platform.platform(),
        'page_size': resource.getpagesize(),
        'clock_ticks': os.sysconf('SC_CLK_TCK'),
    }
