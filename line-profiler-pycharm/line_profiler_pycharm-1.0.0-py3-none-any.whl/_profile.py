import atexit
import json
import os
import pathlib
import sys

import line_profiler


class PyCharmLineProfiler(line_profiler.LineProfiler):
    """Singleton extension around the LineProfiler from line_profiler that writes profile data to a .pclprof file

    When the process exits, the profile results are written to a `.pclprof` file, which contains json data.
    This json file is recognized by the PyCharm Line Profiler plugin.
    The PyCharm Line Profiler plugin can visualize the json file with neat colormaps and other stuff
    directly into the code in the editors.

    PyCharmLineProfiler uses an environment variable called
        PC_LINE_PROFILER_STATS_FILENAME
    to determine where to save the profile file. This environment variable is set by the Line Profiler plugin
    so that plugin's Executor extension can automatically open the results of a profiling after running it.
    """
    _instance = None

    def __init__(self, *args, **kwargs):
        super(PyCharmLineProfiler, self).__init__(*args, **kwargs)
        # Stats file defaults to file in same directory as script with `.pclprof` appended
        self._stats_filename = os.environ.get("PC_LINE_PROFILER_STATS_FILENAME", pathlib.Path(sys.argv[0]).name)
        atexit.register(self._dump_stats_for_pycharm)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _dump_stats_for_pycharm(self):
        """Dumps profile stats that can be read by the PyCharm Line Profiler plugin

        The stats are written to a json file, with extension .pclprof
        This extension is recognized by the PyCharm Line Profiler plugin
        """
        stats = self.get_stats()

        stats_dict = {
            "profiledFunctions": [{
                "file": key[0],
                "lineNo": key[1],
                "functionName": key[2],
                "profiledLines": [{
                    "lineNo": element[0],
                    "hits": element[1],
                    "time": element[2]
                } for element in value]
            } for key, value in stats.timings.items()],
            "unit": stats.unit
        }

        with open(f"{self._stats_filename}.pclprof", 'w') as fp:
            json.dump(stats_dict, fp)


def profile(func):
    """Decorator to be used on functions that have to be profiled

    The decorator wraps the `PyCharmLineProfiler`.

    :param func: function to profile
    """
    return PyCharmLineProfiler.get_instance()(func)
