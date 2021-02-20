""" Complex ftest language function """

#pylint: disable=unused-variable
#pylint: disable=unused-argument

import inspect
import os
import subprocess
import time

from result import Ok, Err

from .vio import adc_pack
from .logger import logger
from .lang import unwrap, Procedure


def register(env, config, name=None):
    """Export a functions to be used by ftest."""
    def decorator(function):
        def run(*args):
            """Run"""
            return function(config, *args)

        run.__doc__ = function.__doc__
        function_name = name if name is not None else function.__name__
        env.update({function_name: run})
        return run


    return decorator


def register_functions(global_env, config, monitor, supervisor):
    """Register."""
    @register(global_env, config)
    def launch(config, *args):
        dir_name = args[0].split("-")[0]
        exe = "/".join([config["root"], dir_name, "bin", args[0] + ".out"])

        if not os.path.isfile(exe):
            logger.error(f"Executable file not found {exe}")
            return Err("Failed")

        logger.debug(f"launch {args[0]}")
        if args[0] not in monitor.launch_table.keys():
            monitor.launch_table[args[0]] = subprocess.Popen(
                exe + f">> {args[0]}.log", shell=True, preexec_fn=os.setsid
            )
            #print_console(
            #    "%s[LAUNCH] Component Initializing... %s" % (fg(243), attr(0)),
            #    False,
            #    config,
            #)
            time.sleep(1)
        else:
            pass
            #print_console(
            #    "%s[LAUNCH] Component already running...Skipping %s"
            #    % (fg(243), attr(0)),
            #    False,
            #    config,
            #)

        return Ok()


    @register(global_env, config)
    def send_adc(config, *args):
        sock = global_env["supervisor"].middle
        sock.sendto(adc_pack(args[0], args[1]), ("127.0.0.1", 9999))
        #print("%ssend_adc %s %s %s" % (fg(243), args[0], args[1], attr(0)))
        return Ok()

    @register(global_env, config)
    def builtin_cmd(config, *args):
        dev, cmd, *args = args
        args = tuple([unwrap(arg) for arg in args])

        return supervisor.fcpcom.cmd(dev, cmd, args)


    @register(global_env, config)
    def builtin_set(config, *args):
        dev, cmd, value = args
        return supervisor.fcpcom.set(dev, cmd, unwrap(value))

    @register(global_env, config)
    def builtin_get(config, *args):
        dev, cmd = args
        return supervisor.fcpcom.get(dev, cmd)


    @register(global_env, config, name="help")
    def _help(config, *args):
        """Get the help string for a function."""
        function = args[0]

        if isinstance(function, Procedure):
            print(function.doc())
        elif callable(function):
            print(inspect.getdoc(args[0]))

    @register(global_env, config)
    def get_signal(config, *args):
        return Ok(global_env["supervisor"].get_signal(args[0]))

    @register(global_env, config)
    def doc(config, *args):
        print(args)



    @register(global_env, config, name='~=')
    def approx(config, *args):
        """Check for equality with a error margin."""
        err = 1e-3
        if len(args) == 2:
            v1, v2 = args
        if len(args) == 3:
            v1, v2, err = args

        v1 = unwrap(v1)
        v2 = unwrap(v2)
        err = unwrap(err)
        return Ok((abs(v1-v2))/(abs(v2)+err) < err)

