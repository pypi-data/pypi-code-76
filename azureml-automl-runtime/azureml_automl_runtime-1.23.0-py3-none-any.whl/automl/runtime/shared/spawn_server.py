# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Functionality to execute a function in a child process created using "spawn".

This file contains the server portion.
"""
import dill
import gc
import logging
import sys

from azureml.automl.core._logging import log_server
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.fake_traceback import FakeTraceback


logger = logging.getLogger("azureml.automl.runtime.shared.spawn_server")


def run_server(config_file_name, input_file_name, output_file_name, error_file_name):
    """Run the server."""
    # Reserve some memory (~4mb) for exception handling.
    mem = b"0" * 1024 * 1024 * 4
    ex = None
    try:
        # Deserialize the configuration object using dill.
        with open(config_file_name, "rb") as f:
            config = dill.load(f)

        # Initialize system path to match parent process configuration.
        sys.path = config["path"]

        # Deserialize the input file using dill.
        with open(input_file_name, "rb") as f:
            obj = dill.load(f)

        for logger_name in config["logger_names"]:
            log_server.install_handler(logger_name)

        with log_server.lock:
            # Set verbosity after loading function, since deserialization can cause dependencies to set the log level.
            log_server.set_verbosity(config["log_verbosity"])
            log_server.custom_dimensions.update(config["custom_dimensions"])

        # Deconstruct the input into function, arguments, keywords arguments.
        fn, args, kwargs = obj

        # Invoke the function and store the result in a (value, error) pair.
        # TODO: Currently this code assumes that the called function will already return such a pair. Need to fix.
        ret, ex = fn(*args, **kwargs)

    except BaseException as e:
        ret = None
        ex = e

    del mem
    gc.collect()

    if ex is not None:
        logging_utilities.log_traceback(ex, logger)

    error = ex, FakeTraceback.serialize_exception_tb(ex)
    with open(error_file_name, "wb") as f:
        dill.dump(error, f, protocol=dill.HIGHEST_PROTOCOL)

    # Write the result to the output file using dill.
    # HIGHEST_PROTOCOL is needed for models greater than 4Gb
    with open(output_file_name, "wb") as f:
        dill.dump(ret, f, protocol=dill.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    # Check command-line arguments.
    if len(sys.argv) != 5:
        print("Usage: spawn_server config_file input_file output_file error_file")
        exit(10)

    # Extract configuration, input, and output file names.
    config_file_name = sys.argv[1]
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]
    error_file_name = sys.argv[4]

    try:
        run_server(config_file_name, input_file_name, output_file_name, error_file_name)
    except Exception as e:
        sys.stderr.write("{}\n".format(e))
        logging_utilities.log_traceback(e, logger)
        exit(20)
