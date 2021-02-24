# Fenix Library
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://gitlab.com/rebornos-team/fenix/libraries

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2. 

# IMPORTS
from __future__ import annotations
from abc import ABC
import collections
from dataclasses import dataclass
from enum import Enum
import functools
import os
import pathlib
import signal
import subprocess
from subprocess import Popen
import textwrap
import threading
from typing import Any, Deque, Dict, List, Optional, Tuple, Union, IO, Callable
import typing
import logging
from concurrent.futures import ThreadPoolExecutor
import itertools
from queue import Queue
from concurrent.futures import Future

# PRIVATE CLASSES

class LoggingLevel(Enum):
    """
    Indicates the logging severity   

    """
    CRITICAL = 50
    EXCEPTION = 40
    ERROR = 40    
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

# PUBLIC CLASSES

class LoggingHandler:
    """
    A class to handle logging in any particular module. 

    Attributes
    ----------
    logging_functions: List[Callable[[int, str, Any], Any]]
            A list of functions that are to be called with (logging_level: int, message: str, *args, **kwargs) in order to do the logging
            This may contain the Python standard logging.Logger.log(...) function, along with any functions that can write logs to the user interface (UI)
    process_output_thread_pool_executor: ThreadPoolExecutor
        A thread pool with one worker for reading stdout pipe of the process
    process_error_thread_pool_executor: ThreadPoolExecutor
        A thread pool with one worker for reading stderr pipe of the process
    process_coordination_thread_pool_executor: ThreadPoolExecutor
        A thread pool with one worker to coordinate and schedule output and error logs in the order they arrive, not the order they finish
    log_thread_pool_executor: ThreadPoolExecutor
        A thread pool with one worker for calling the logging functions
    process_futures: List[Future]
        A list of future objects corresponding to either output or error being read from the process pipes.
    """

    # CONSTRUCTOR

    def __init__(
        self,
        logging_functions: List[Callable[[int, str, Any], Any]],
        process_thread_name_prefix: str = "",
        log_thread_name_prefix: str = ""
    ) -> None:
        """
        Initializes a new LoggingHandler instance

        Parameters
        ----------
        logging_functions: List[Callable[[int, str, Any], Any]]
            A list of functions that are to be called with (logging_level: int, message: str, *args, **kwargs) in order to do the logging
            This may contain the Python standard logging.Logger.log(...) function, along with any functions that can write logs to the user interface (UI)

        Returns
        -------
        Nothing
        """

        # Initialize attributes from the give parameters
        self.logging_functions: List[Callable[[int, str, Any], Any]] = logging_functions

        # Initialize other parameters
        self.process_output_thread_pool_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 1, thread_name_prefix= process_thread_name_prefix + "_out_")
        self.process_error_thread_pool_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 1, thread_name_prefix= process_thread_name_prefix + "_err_")
        self.process_coordination_thread_pool_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 1, thread_name_prefix= process_thread_name_prefix)
        self.log_thread_pool_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 1, thread_name_prefix= log_thread_name_prefix)
        self.process_futures: List[Future] = []

    # DESTRUCTOR

    def __del__(self) -> None:
        """
        Shuts down all the thread pool executors

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.process_error_thread_pool_executor.shutdown()
        self.process_output_thread_pool_executor.shutdown()
        self.process_coordination_thread_pool_executor.shutdown()
        self.log_thread_pool_executor.shutdown()

    # PRIVATE METHODS

    def _log_message(
        self,
        logging_level: int = LoggingLevel.DEBUG.value,
        message: str = "",
        *args,
        **kwargs
    ) -> None:
        """
        Used by the library functions to call the logging functions specified by the user

        This function is not meant to be used outside the library. 
        Use the respective `write` or `run_and_log` methods of individual `LogMessage` and `Command` instances instead.

        Parameters
        ----------
        logging_level: int
            The logging severity indicated as numerical values of logging levels as specified in the LoggingLevel class
            and in https://docs.python.org/3/library/logging.html
        message: str
            The log message
        args: Tuple[Any]
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods

        Returns
        -------
        Nothing
        """

        # Combine all logging methods into one function
        def __consolidated_logging_function(
            logging_level: int,
            message: str,
            *args,
            **kwargs
        ) -> None:
           for logging_function in self.logging_functions:
                logging_function(
                    logging_level,
                    message,
                    *args,
                    **kwargs
                )

        _ = self.log_thread_pool_executor.submit(
            __consolidated_logging_function,
            logging_level,
            message,
            *args,
            **kwargs
        )  

    def _log_process(
        self,
        process: subprocess.Popen,
        is_silent: bool
    ) -> Future:
        """
        Handles the logging of both stdout and stderr of a process

        Parameters
        ----------
        process: subprocess.Popen
            The process that needs to be logged
        is_silent: bool
            Indicates whether to skip logging

        Returns
        -------
        Nothing
        """

        def __process_output() -> str:
            total_output: str = ""
            if process.stdout is not None:
                for output_line in iter(process.stdout):
                    output_line = output_line.strip()
                    if not output_line.startswith("S>"):
                        total_output = total_output + output_line
                    log_message: LogMessage = LogMessage.Debug(message= output_line, is_silent= is_silent)
                    future = self.log_thread_pool_executor.submit(
                        self._log_message,
                        log_message.logging_level.value,
                        log_message.message,
                        *log_message.args,
                        **log_message.kwargs
                    )
                    self.process_futures.append(future)
            return total_output

        def __process_error() -> str:
            total_output: str = ""
            if process.stderr is not None:
                for error_line in iter(process.stderr):
                    error_line = error_line.strip()
                    if "critical" in error_line.lower() or "fatal" in error_line.lower():  # If either of the words "critical" or "fatal" is found in stderr
                        log_message: LogMessage = LogMessage.Critical(message= error_line, is_silent= is_silent)
                    elif "error" in error_line.lower() or "exception" in error_line.lower(): # If either of the words "error" or "exception" is found in stderr
                        log_message: LogMessage = LogMessage.Error(message= error_line, is_silent= is_silent)
                    elif "warning" in error_line.lower() or "caution" in error_line.lower(): # If either of the words "warning" or "caution" is found in stderr
                        log_message: LogMessage = LogMessage.Warning(message= error_line, is_silent= is_silent)  
                    elif error_line.isspace() or len(error_line) == 0: 
                        continue
                    else:
                        log_message: LogMessage = LogMessage.Error(message= error_line, is_silent= is_silent)
                    total_output = total_output + error_line  
                    future = self.log_thread_pool_executor.submit(
                        self._log_message,
                        log_message.logging_level.value,
                        log_message.message,
                        *log_message.args,
                        **log_message.kwargs
                    )
                    self.process_futures.append(future)
            return total_output

        def __coordinate() -> str:
            total_output: str = ""
            assert(total_output is not None)
            for future in self.process_futures:
                total_output = total_output + str(future.result())
            return total_output

        _ = self.process_output_thread_pool_executor.submit(__process_output)
        _ = self.process_error_thread_pool_executor.submit(__process_error)
        output_future = self.process_coordination_thread_pool_executor.submit(__coordinate)

        return output_future

class LogMessage:
    """
    Represents a log message
    
    Stores the logging level and other optional arguments to be passed to the standard Python logging library, 
    or to other custom logging functions that follow the same function signature

    Usage Examples:
        - `log_message = LogMessage.DEBUG("Some message")
        - `log_message = LogMessage(LogMessage.DEBUG, "Some message")

    Static Attributes
    ----------------
    CRITICAL: LoggingLevel
        LoggingLevel.CRITICAL
    EXCEPTION: LoggingLevel
        LoggingLevel.EXCEPTION
    ERROR: LoggingLevel
        LoggingLevel.ERROR
    WARNING: LoggingLevel
        LoggingLevel.WARNING
    INFO: LoggingLevel
        LoggingLevel.INFO
    DEBUG: LoggingLevel
        LoggingLevel.DEBUG
    NOTSET: LoggingLevel
        LoggingLevel.NOTSET

    Attributes
    ----------
    logging_level: LoggingLevel
        The logging level as en enumeration. Can be one of 
            - LogMessage.CRITICAL
            - LogMessage.EXCEPTION
            - LogMessage.ERROR
            - LogMessage.WARNING
            - LogMessage.INFO
            - LogMessage.DEBUG
            - LogMessage.NOTSET
    message: str
        The log message
    is_silent: bool
        Indicates whether logging is to be skipped
    args: Tuple[Any]
        Any un-named arguments to the Python standard logging methods
    kwargs: Dict[str, Any]
        Any named arguments to the Python standard logging methods
    
    """

    # STATIC ATTRIBUTES

    CRITICAL = LoggingLevel.CRITICAL
    EXCEPTION = LoggingLevel.EXCEPTION
    ERROR = LoggingLevel.ERROR
    WARNING = LoggingLevel.WARNING
    INFO = LoggingLevel.INFO
    DEBUG = LoggingLevel.DEBUG
    NOTSET = LoggingLevel.NOTSET

    # CONSTRUCTOR

    def __init__(
        self,
        logging_level: LoggingLevel = LoggingLevel.INFO,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    )-> None:
        """
        Creates a new LogMessage object

        Parameters
        ----------
        logging_level: LoggingLevel
            The logging level as en enumeration. Can be one of 
                - LogMessage.CRITICAL
                - LogMessage.EXCEPTION
                - LogMessage.ERROR
                - LogMessage.WARNING
                - LogMessage.INFO
                - LogMessage.DEBUG
                - LogMessage.NOTSET
        message: str
            The log message
        is_silent: bool
            Indicates whether logging is to be skipped
        args: Tuple[Any]
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        # Assign LogMessage attributes based on the given parameters
        self.logging_level: LoggingLevel = logging_level
        self.message: str = message
        self.is_silent: bool = is_silent
        self.args: Tuple[Any, ...] = args
        self.kwargs: Dict[str, Any] = kwargs    

    # CLASS METHODS TO CREATE SPECIAL LOG OBJECTS
    # Usage example: log_message = LogMessage.Debug("Test message")

    @classmethod
    def Critical(
        cls,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    ) -> LogMessage:
        """
        Returns a LogMessage object representing a critical log message

        Usage example: log_message = LogMessage.Critical("Test message")

        Parameters
        ----------
        message: str
            Stored the log message
        is_silent: bool
            Whether logging is to be skipped
        args: Tuple
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        return cls(
            logging_level= LogMessage.CRITICAL,
            message= message,
            is_silent= is_silent,
            *args,
            **kwargs
        )

    @classmethod
    def Exception(
        cls,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    ) -> LogMessage:
        """
        Returns a LogMessage object representing an exception log message

        Usage example: log_message = LogMessage.Exception("Test message")

        Parameters
        ----------
        message: str
            Stored the log message
        is_silent: bool
            Whether logging is to be skipped
        args: Tuple
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        return cls(
            logging_level= LogMessage.EXCEPTION,
            message= message,
            is_silent= is_silent,
            *args,
            **kwargs
        )

    @classmethod
    def Error(
        cls,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    ) -> LogMessage:
        """
        Returns a LogMessage object representing an error log message

        Usage example: log_message = LogMessage.Error("Test message")

        Parameters
        ----------
        message: str
            Stored the log message
        is_silent: bool
            Whether logging is to be skipped
        args: Tuple
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        return cls(
            logging_level= LogMessage.ERROR,
            message= message,
            is_silent= is_silent,
            *args,
            **kwargs
        )

    @classmethod
    def Warning(
        cls,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    ) -> LogMessage:
        """
        Returns a LogMessage object representing a warning log message

        Usage example: log_message = LogMessage.Warning("Test message")

        Parameters
        ----------
        message: str
            Stored the log message
        is_silent: bool
            Whether logging is to be skipped
        args: Tuple
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        return cls(
            logging_level= LogMessage.WARNING,
            message= message,
            is_silent= is_silent,
            *args,
            **kwargs
        )

    @classmethod
    def Info(
        cls,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    ) -> LogMessage:
        """
        Returns a LogMessage object representing an informational log message

        Usage example: log_message = LogMessage.Info("Test message")

        Parameters
        ----------
        message: str
            Stored the log message
        is_silent: bool
            Whether logging is to be skipped
        args: Tuple
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        return cls(
            logging_level= LogMessage.INFO,
            message= message,
            is_silent= is_silent,
            *args,
            **kwargs
        )

    @classmethod
    def Debug(
        cls,
        message: str = "",
        is_silent: bool = False,
        *args,
        **kwargs
    ) -> LogMessage:
        """
        Returns a LogMessage object representing a debug log message

        Usage example: log_message = LogMessage.Debug("Test message")

        Parameters
        ----------
        message: str
            Stored the log message
        is_silent: bool
            Whether logging is to be skipped
        args: Tuple
            Any un-named arguments to the Python standard logging methods
        kwargs: Dict[str, Any]
            Any named arguments to the Python standard logging methods
        """

        return cls(
            logging_level= LogMessage.DEBUG,
            message= message,
            is_silent= is_silent,
            *args,
            **kwargs
        )

    # REGULAR METHODS
    def write(
        self,
        logging_handler: LoggingHandler = None
    ) -> None:
        """
        Writes to the Python logger

        Parameters
        ----------
        logging_handler: Optional[LoggingHandler]
            The LoggingHandler object which stores the logging functions, logging threads, logger information, etc.
        """

        if not self.is_silent and (logging_handler is not None): 
            logging_handler._log_message(
                self.logging_level.value,
                self.message,
                *self.args,
                **self.kwargs
            )

class AbstractRunnable(ABC):
    """
    An abstract class that represents anything that can be run through Python or through a shell.

    Attributes
    ----------
    is_silent: bool
        Whether logging should be skipped
    pre_run_function: Optional[functools.partial]
        The function to be called before the execution
    post_run_function: Optional[functools.partial]
        The function to be called after the execution
    do_send_output_to_post_run_function: bool
        Whether to receive the output of the command as the first argument for the `post_run_function` method
    do_abort: bool
        An abort request has been received
    is_running: bool
        Whether the execution has started
    has_completed: bool
        Whether the execution has completed
    output: Optional[Any]
        The output
    """

    # CONSTRUCTOR

    def __init__(
        self,
        *, # The arguments following this must all have a name. For example, function(a= 1, text= "hello") 
        is_silent: bool = False,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False
    ) -> None:
        """
        Initializes the current instance

        Parameters
        ----------
        is_silent: bool, default False
            Whether logging should be skipped
        pre_run_function: Optional[functools.partial], default None
            The function to be called before the execution
        post_run_function: Optional[functools.partial], default None
            The function to be called after the execution
        do_send_output_to_post_run_function: bool, default False
            Whether to receive the output after execution as the first argument for `post_run_function`

        Returns
        -------
        Nothing
        """

        # Initialize attributes from arguments
        self.is_silent: bool = is_silent
        self.pre_run_function: Optional[functools.partial] = pre_run_function
        self.post_run_function: Optional[functools.partial] = post_run_function
        self.do_send_output_to_post_run_function: bool = do_send_output_to_post_run_function

        # Initialize other attributes
        self.do_abort: bool = False
        self.is_running: bool = False
        self.has_completed: bool = False
        self.output: Optional[Any] = None

    # REGULAR METHODS

    def call_pre_run_function(self) -> Optional[Any]:
        """
        Executes the `post_run_function` method and handles cases where it is absent

        Parameters
        ----------
        None

        Returns
        -------
        output: Optional[Any]
            The object(s) returned from the method `pre_run_function`
        """

        if self.pre_run_function is not None: # If a pre run function is specified
            return self.pre_run_function() # Call the function handle 
        else: # If a pre run function is not specified
            return None # Do nothing

    def call_post_run_function(self) -> Optional[Any]:
        """
        Executes the `post_run_function` method and handles cases where it is absent

        Parameters
        ----------
        None

        Returns
        -------
        output: Optional[Any]
            The object(s) returned from the method `post_run_function`
        """

        if self.post_run_function is not None: # If a post run function is specified
            if self.do_send_output_to_post_run_function:
                modified_function_handle: functools.partial = functools.partial( # Modify the function format to add the command's output output as the first argument
                    self.post_run_function.func,
                    self.output,
                    *self.post_run_function.args,
                    **self.post_run_function.keywords
                )
                return modified_function_handle() # Call the modified function handle
            else:
                return self.post_run_function()         
        else: # If a post run function is not specified
            return None # Do nothing

class Function(AbstractRunnable, functools.partial):
    """
    Represents a function along with its arguments
    A wrapper for functools.partial

    Properties
    ----------
    handle: Callable
        Stores the function handle. Wrapper for functools.partial.func
    arguments: Tuple[Any]
        The arguments to be passed to the function. Wrapper for functools.partial.func.args
    is_silent: bool
        Whether logging should be skipped
    pre_run_function: Optional[functools.partial]
        The function to be called before the execution
    post_run_function: Optional[functools.partial]
        The function to be called after the execution
    do_send_output_to_post_run_function: bool
        Whether to receive the output of the command as the first argument for the `post_run_function` method
    keyword_arguments: Dict[str, Any]
        The named arguments to be passed to the function. Wrapper for functools.partial.func.keywords
    
    """

    # CONSTRUCTOR

    def __init__(
        self,
        handle: Callable,
        *arguments,
        is_silent: bool = False,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False,
        **keyword_arguments
    ) -> None:
        """
        Initializes the current instance

        Parameters
        ----------
        handle: Callable
            The function handle as a callable
        arguments
            The arguments to be passed to the function, separated by commas
        is_silent: bool
            Whether logging should be skipped
        pre_run_function: Optional[functools.partial]
            The function to be called before the execution
        post_run_function: Optional[functools.partial]
            The function to be called after the execution
        do_send_output_to_post_run_function: bool
            Whether to receive the output of the command as the first argument for the `post_run_function` method
        keyword_arguments
            The named arguments to be passed to the function, separated by commas        
        """

        # Initialize attributes from arguments
        self.handle: Callable = handle
        self.arguments: Tuple = arguments
        self.keyword_arguments: Dict[str, Any] = keyword_arguments    
            
        # Call the parent class constructor
        AbstractRunnable.__init__(
            self,
            is_silent= is_silent,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= do_send_output_to_post_run_function
        )

    # CLASS METHODS
    # TO CREATE SPECIAL FUNCTION OBJECTS

    @classmethod
    def Silent(
        cls,
        handle: Callable,
        *arguments,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False,
        **keyword_arguments
    ) -> Function:
        """
        Creates a silent Function object that skips logging and returns it

        Parameters
        ----------
        handle: Callable
            The function handle as a callable
        arguments
            The arguments to be passed to the function, separated by commas
        pre_run_function: Optional[functools.partial]
            The function to be called before the execution
        post_run_function: Optional[functools.partial]
            The function to be called after the execution
        keyword_arguments
            The named arguments to be passed to the function, separated by commas    

        Returns
        -------
        A Function instance that skips logging
        """

        function: Function = cls(
            handle= handle,
            *arguments,
            is_silent= True,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= do_send_output_to_post_run_function,
            **keyword_arguments
        ) # Create a general function object from the arguments
        return function

    # REGULAR METHODS

    def run(self) -> Optional[Any]:
        """
        Run the function

        Returns
        -------
        output: Optional[Any]
            The output of the function
        """

        self.call_pre_run_function()
        output: Optional[Any] = self.__call__()
        self.call_post_run_function()

        return output

    def run_and_log(
        self,
        logging_handler: LoggingHandler = None
    ) -> Optional[Any]:
        """
        Run the function and logs the output

        Parameters
        ----------
        logging_handler: Optional[LoggingHandler]
            The LoggingHandler object which stores the logging functions, logging threads, logger information, etc.

        Returns
        -------
        output: Optional[Any]
            The output of the function
        """

        # Log details about the function being run
        LogMessage.Debug(message= "PYTHON> Calling: " + str(self.handle), is_silent= self.is_silent).write(logging_handler= logging_handler)

        self.call_pre_run_function()
        self.output = str(self.__call__()) # Call the function and capture the output
        self.call_post_run_function()

        # Log the output
        LogMessage.Debug(message= "P> Returned: " + self.output, is_silent= self.is_silent).write(logging_handler= logging_handler)

        return self.output   

    # OVERLOADED MAGIC METHODS
    def __call__(self, /, *more_arguments, **more_keyword_arguments) -> Optional[Any]:
        """
        Calls the function handle

        Parameters
        ----------
        *more_arguments
            Any number of arguments separated by commas
        **more_keyword_arguments
            Any number of named arguments separated by commas

        Returns
        -------
        output: Optional[Any]
            The return value of the function
        """

        callable_function: functools.partial = functools.partial(
            self.handle,
            *self.arguments,
            **self.keyword_arguments
        )

        self.is_running = True
        self.has_completed = False

        output: Optional[Any] = callable_function(*more_arguments, **more_keyword_arguments)

        self.is_running = False
        self.has_completed = True

        return output

class Command(AbstractRunnable):
    """
    Represents a command that can be executed on the host system through Python.
    Overloads the "<", ">", ">=", "<<", ">>", "|" and "&" operators to interface the unwieldy Python pipes into beautiful shell-like syntax. Examples for usage of operator overloading: 
    - `command = Command(["cat"]) < pathlib.Path("file.txt")`
    - `command = Command(["grep", "bread"]) << "I eat peanut butter with bread"`
    - `command = Command(["echo", "Hello"]) > pathlib.Path("file.txt")`
    - `command = Command(["echo", "Hello"]) >= pathlib.Path("file.txt")`
    - `command = Command(["echo", "Hello"]) >> pathlib.Path("non_empty_file.txt")`
    - `command = Command(["echo", "Hello my green umbrella"]) | Command(["grep", "umbrella"])`
    - `command = Command(["echo", "Hello my green umbrella"]) |= Command(["grep", "umbrella"])`
    - `command = Command["ping", "www.google.com"] & None`
    - `command = pathlib.Path("file.txt") > Command(["cat"])`
    - `command = "I eat peanut butter with bread" >> Command(["grep", "bread"])`
    - `command = pathlib.Path("file.txt") < Command(["echo", "Hello"])`
    - `command = pathlib.Path("file.txt") <= Command(["echo", "Hello"])`
    - `command = pathlib.Path("non_empty_file.txt") << Command(["echo", "Hello"])`
    
    Static Attributes
    ----------------
    SHELL_TRAP_STRING
        Bash trap command to display inputs and outputs. Multiple nested quotes have been escaped.
    UNIVERSAL_NEWLINES: bool
        TRUE, use strings instead of bytes for stdin, stdout, and stderr. 
        FALSE, use bytes instead of strings for stdin, stdout, and stderr. Call <bytes>.decode() to convert to string 
    BUFFER_SIZE: int
        From the python documentation: https://docs.python.org/3/library/subprocess.html
        0, unbuffered (read and write are one system call and can return short)
        1, line buffered (only usable if universal_newlines=True i.e., in a text mode)
        any other positive value means use a buffer of approximately that size
        negative bufsize (the default) means the system default of io.DEFAULT_BUFFER_SIZE will be used.

    Attributes
    ----------
    command_strings: List[str]
        A list of strings containing the command to be executed and its arguments
    command_string: str
        A string containing the command to be executed in a shell
    timeout: Optional[float]
        The time for which the command can run before aborting
    working_directory: Optional[str]
        The working directory to run the command in
    environment: Optional[os._Environ]
        The environment that should be set, for executing the command
    on_shell: bool
        Whether the command should run in a shell
    shell_command_string: Optional[str]
        A single string containing the command to be executed (used when shell = True)
    stdin_subprocess: Optional[Union[int, IO]]
        One of [None, subprocess.PIPE, <file descriptor>]
    stdout_subprocess: Optional[Union[int, IO]]
        One of [None, subprocess.PIPE, <file descriptor>]
    stderr_subprocess: Optional[Union[int, IO]]
        One of [None, subprocess.PIPE, subprocess.STDOUT, <file descriptor>]
    stdin_external_source: Optional[Union[str, pathlib.Path]
        The source of the input stream can be a string or a filepath
    stdout_external_destination: Optional[pathlib.Path]
        The destination of the stdout can be a filepath
    rightside_operator: Optional[str]
        One of ["<", ">", ">=", "<<", ">>", "|", "&", None]
    command_pointer: Optional[Command]
        The current command in the pipe chain
    next_pipe_command: Optional[Command]
        The next command in the pipe chain
    processes: List[subprocess.Popen]
        The processes associated with the current Command
    temp_filepath: Optional[str]
        Temporary file path for modifying the script with a trap command
        Only used with Command.Script(...) and Command.ScriptShell(...)

    TODO
    ----
    Overload `&` or __and__ for running the command in the background

    """

    # STATIC ATTRIBUTES

    # _trap_string_with_date = "trap \'printf \"[%s %s %s] %s\\n\" $(date \'\"\'\"\'+%F, %T %Z\'\"\'\"\') \"$BASH_COMMAND\"\' DEBUG" # bash trap command to display inputs and outputs with time stamps. Multiple nested quotes have been escaped.
    SHELL_TRAP_STRING = "trap \'printf \"%s\\n\" \"" + "S>" + " $BASH_COMMAND\"\' DEBUG"
    UNIVERSAL_NEWLINES: bool = True
    BUFFER_SIZE: int = 1
    TYPE_ERROR: TypeError = TypeError("This method or syntax is not suitable when using the Shell constructor or when on_shell is set to true. All pipes and redirections can be made directly in the command string.")

    # CONSTRUCTOR

    def __init__(
        self,
        command_strings: List[str] = [],
        *, # The arguments following this must all have a name. For example, function(a= 1, text= "hello")
        timeout: Optional[float] = None,
        working_directory: Optional[str] = None,
        environment: Optional[os._Environ] = None,
        is_silent: bool = False,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False,
        temp_filepath: Optional[str] = None
    ) -> None:
        """
        Initialize a 'Command' object to run through Python
        
        Parameters
        ----------
        command_strings: List[str], default []
            A list of strings containing the command to be executed and its arguments
        timeout: Optional[float], default None
            The time for which the command can run before aborting
        working_directory: Optional[str]
            The working directory to run the command in
        environment: Optional[os._Environ], default None
            The environment that should be set, for executing the command
        is_silent: bool, default False
            Whether logging should be skipped
        pre_run_function: Optional[functools.partial], default None
            The function to be called before the execution
        post_run_function: Optional[functools.partial], default None
            The function to be called after the execution
        do_send_output_to_post_run_function: bool, default False
            Whether to receive the output after execution as the first argument for `post_run_function`
        temp_filepath: Optional[str]
            Temporary file path for modifying a script with a trap command
            Only used with Command.Script(...) and Command.ScriptShell(...)

        Returns
        -------
        Nothing
        """

        # Assign arguments to attributes
        self.command_strings: List[str] = command_strings
        self.timeout: Optional[float] = timeout
        self.working_directory: Optional[str] = working_directory
        self.environment: Optional[os._Environ] = environment
       
        # Initialize other attributes
        self.command_string: str = ""
        self.on_shell: bool = False

        self.stdin_subprocess: Optional[Union[int, IO]] = subprocess.PIPE
        self.stdout_subprocess: Optional[Union[int, IO]] = subprocess.PIPE
        self.stderr_subprocess: Optional[Union[int, IO]] = subprocess.PIPE        
        self.stdin_external_source: Optional[Union[str, pathlib.Path]] = None
        self.stdout_external_destination: pathlib.Path = pathlib.Path("")
        self.rightside_operator: Optional[str] = None
        self.next_pipe_command: Optional[Command] = None
        self.command_pointer: Optional[Command] = self
        self.processes: List[subprocess.Popen] = []

        self.temp_filepath: Optional[str] = temp_filepath

        # Call the parent class constructor
        super().__init__(
            is_silent= is_silent,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= do_send_output_to_post_run_function
        )

    # CLASS METHODS
    # TO CREATE SPECIAL COMMAND OBJECTS

    @classmethod
    def Shell(
        cls,
        command_string: str = "",
        *, # The arguments following this must all have a name. For example, function(a= 1, text= "hello")
        timeout: Optional[float] = None,
        working_directory: Optional[str] = None,
        environment: Optional[os._Environ] = None,
        is_silent: bool = False,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False
    ) -> Command:
        """
        Initialize a 'Command' object to run *in a shell* and return that Command object
        
        Parameters
        ----------
        command_string: str, default ""
            The string containing the command to be executed in a shell
        timeout: Optional[float], default None
            The time for which the command can run before aborting
        working_directory: Optional[str]
            The working directory to run the command in
        environment: Optional[os._Environ], default None
            The environment that should be set, for executing the command
        is_silent: bool, default False
            Whether logging should be skipped
        pre_run_function: Optional[functools.partial], default None
            The function to be called before the execution
        post_run_function: Optional[functools.partial], default None
            The function to be called after the execution
        do_send_output_to_post_run_function: bool, default False
            Whether to receive the output after execution as the first argument for `post_run_function`

        Returns
        -------
        Command
            A command instance to run in a shell
        """

        shell_command: Command = cls(
            command_strings= [],
            timeout= timeout,
            working_directory= working_directory,
            environment= environment,
            is_silent= is_silent,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= do_send_output_to_post_run_function
        )

        shell_command.command_string = command_string
        shell_command.on_shell = True

        return shell_command

    @classmethod
    def Script(
        cls,
        script_filepath: str,
        script_arguments: List[str] = [],
        execution_prefix: str = "sh",
        *, # The arguments following this must all have a name. For example, function(a= 1, text= "hello")
        timeout: Optional[float] = None,
        working_directory: Optional[str] = None,
        environment: Optional[os._Environ] = None,
        is_silent: bool = False,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False
    ) -> Command:
        """
        Initialize a 'Command' object to run a script with internal logging, and return the Command object
        
        Parameters
        ----------
        script_filepath: str
            A string containing the relative filepath to the script to be executed
        script_arguments: List[str], default []
            The arguments to the script to be executed
        execution_prefix: str, default "sh"
            The prefix to be added to execute the command
        timeout: Optional[float], default None
            The time for which the command can run before aborting
        working_directory: Optional[str]
            The working directory to run the command in
        environment: Optional[os._Environ], default None
            The environment that should be set, for executing the command
        is_silent: bool, default False
            Whether logging should be skipped
        pre_run_function: Optional[functools.partial], default None
            The function to be called before the execution
        post_run_function: Optional[functools.partial], default None
            The function to be called after the execution
        do_send_output_to_post_run_function: bool, default False
            Whether to receive the output after execution as the first argument for `post_run_function`

        Returns
        -------
        Command
            A command instance to run a script and log its internal commands
        """              

        # Create a temporary copy of the script to prefix a trap command
        temp_filepath: str = script_filepath + "_temp"
        with open(temp_filepath, "w") as script_file_new:
            with open(script_filepath, "r") as script_file_old:
                script_file_new.write(cls.SHELL_TRAP_STRING + "\n\n") # create a temporary script with a trap command to display both inputs and outputs, with time stamps              
                script_file_new.write(script_file_old.read()) # copy all lines from the script to a temporary script

        # Call the Command class constructor
        return cls(
            command_strings= [execution_prefix, temp_filepath] + script_arguments,
            timeout= timeout,
            working_directory= working_directory,
            environment= environment,
            is_silent= is_silent,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= do_send_output_to_post_run_function,
            temp_filepath= temp_filepath
        )   

    @classmethod
    def ScriptShell(
        cls,
        script_filepath: str,
        script_arguments_string: str = "",
        execution_prefix: str = "sh",
        *, # The arguments following this must all have a name. For example, function(a= 1, text= "hello")
        timeout: Optional[float] = None,
        working_directory: Optional[str] = None,
        environment: Optional[os._Environ] = None,
        is_silent: bool = False,
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None,
        do_send_output_to_post_run_function: bool = False
    ) -> Command:
        """
        Initialize a 'Command' object to run a script with internal logging inside a shell, and return the Command object
        
        Parameters
        ----------
        script_filepath: str
            A string containing the relative filepath to the script to be executed
        script_arguments_string: str, default ""
            The arguments to the script to be executed
        execution_prefix: str, default "sh"
            The prefix to be added to execute the command
        timeout: Optional[float], default None
            The time for which the command can run before aborting
        working_directory: Optional[str]
            The working directory to run the command in
        environment: Optional[os._Environ], default None
            The environment that should be set, for executing the command
        is_silent: bool, default False
            Whether logging should be skipped
        pre_run_function: Optional[functools.partial], default None
            The function to be called before the execution
        post_run_function: Optional[functools.partial], default None
            The function to be called after the execution
        do_send_output_to_post_run_function: bool, default False
            Whether to receive the output after execution as the first argument for `post_run_function`

        Returns
        -------
        Nothing
        """      

        script_launch_command = cls.Script(
            script_filepath= script_filepath,
            script_arguments= [],
            execution_prefix= execution_prefix,
            timeout= timeout,
            working_directory= working_directory,
            environment= environment,
            is_silent= is_silent,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= do_send_output_to_post_run_function
        ) 

        if script_launch_command.temp_filepath is not None:
            script_launch_command.command_string = " ".join([execution_prefix, script_launch_command.temp_filepath, script_arguments_string])
            script_launch_command.on_shell = True

        return script_launch_command

    # DESTRUCTOR
    def __del__(self) -> None:
        """
        Destructor of the class. 
        When the current instance is being destroyed, deletes temporary files created for scripts

        Parameters
        ----------
        None

        Returns
        -------
        Nothing        
        """

        if self.temp_filepath is not None:
            os.remove(self.temp_filepath) # remove the temporary script

    # CLASS METHODS
    # TO CREATE SPECIAL SCRIPTLAUNCHCOMMAND OBJECTS

    # EXECUTION METHODS

    def start(self) -> subprocess.Popen:
        """
        Start running the command and pass the control back (do not wait until command completion)

        Parameters
        ----------
        None

        Returns
        -------
        process_handle: subprocess.Popen
            The Popen object generated from the last subprocess in the pipe chain
        """

        process: Optional[subprocess.Popen] = None

        if self.on_shell is True:
            process = self._shell_command_worker()
            self.processes.append(process)
        else:
            for command_part in self:
                if command_part.rightside_operator is None:
                    process = Command._command_part_worker(command_part)
                elif command_part.rightside_operator == "|":
                    process = Command._command_part_worker(command_part)
                    command_part.next_pipe_command.stdin_subprocess = process.stdout
                elif command_part.rightside_operator == "|=":
                    command_part.stderr_subprocess = subprocess.STDOUT
                    process = Command._command_part_worker(command_part)
                    command_part.next_pipe_command.stdin_subprocess = process.stdout
                elif command_part.rightside_operator == ">>":
                    command_part.stdout_subprocess = open(command_part.stdout_external_destination, "ab")
                    process = Command._command_part_worker(command_part)
                elif command_part.rightside_operator == "<<":
                    process = Command._command_part_worker(command_part)
                    process.stdin.write(
                        textwrap.dedent(
                            typing.cast(
                                str,
                                command_part.stdin_external_source
                            )
                        ).encode()
                    )
                elif command_part.rightside_operator == ">=":
                    command_part.stdout_subprocess = open(command_part.stdout_external_destination, "wb")
                    command_part.stderr_subprocess = subprocess.STDOUT
                    process = Command._command_part_worker(command_part)
                elif command_part.rightside_operator == ">":
                    command_part.stdout_subprocess = open(command_part.stdout_external_destination, "wb")
                    process = Command._command_part_worker(command_part)
                elif command_part.rightside_operator == "<":
                    command_part.stdin_subprocess = open(
                        typing.cast(pathlib.Path, command_part.stdin_external_source),
                        "rb"
                    )
                    process = Command._command_part_worker(command_part)
                else: 
                    raise NotImplementedError("The operator " + command_part.rightside_operator + "is not supported yet.")          

                self.processes.append(process) # store the process of the command_part              

        if process is not None:
            self.is_running = True
            self.has_completed = False
            return process
        else:
            print("command_strings: ", self.command_strings)
            print("command_string: ", self.command_string)
            raise Exception("A process could not be created...")

    def run_and_wait(self) -> str:
        """
        Start running the command and wait until completion

        Parameters
        ----------
        None

        Returns
        -------
        output: str
            The output of the command
        """

        self.call_pre_run_function()        
        process = self.start()
        self.is_running = True
        self.has_completed = False
        process.wait()
        self.is_running = False
        self.has_completed = True
        self.output, error = process.communicate()
        if (not error.isspace()) and len(error) != 0:
            self.output = self.output + error
        self.call_post_run_function()

        return str(self.output)

    def run_log_and_wait(self, logging_handler: Optional[LoggingHandler] = None) -> str:
        """
        Start running the command, log it live, and wait until completion

        Parameters
        ----------
        logging_handler: Optional[LoggingHandler]
            The LoggingHandler object which stores the logging functions, logging threads, logger information, etc.

        Returns
        -------
        output: str
            The output of the command
        """

        self.call_pre_run_function()

        # Log details about the command being run
        if self.on_shell:
            LogMessage.Debug(message= "SHELL> " + self.command_string, is_silent= self.is_silent).write(logging_handler= logging_handler)
        else:
            LogMessage.Debug(message= "OS> " + " ".join(self.command_strings), is_silent= self.is_silent).write(logging_handler= logging_handler)

        # Start the execution
        process: subprocess.Popen = self.start()   
        self.is_running = True
        self.has_completed = False       

        output_future = logging_handler._log_process(process, self.is_silent)
        process.wait()
        self.output = output_future.result()

        leftover_output: str = process.communicate()[0]
        leftover_error: str = process.communicate()[1]
        if leftover_output is not None:
            leftover_output = leftover_output.strip()
            LogMessage.Debug(message= leftover_output).write(logging_handler= logging_handler)
            self.output = self.output + leftover_output
        if (leftover_error is not None) and (not leftover_error.isspace()) and (len(leftover_error) != 0):
            leftover_error = leftover_error.strip()
            LogMessage.Error(message= leftover_error).write(logging_handler= logging_handler)
            self.output = self.output + leftover_error
            
        self.is_running = False
        self.has_completed = True        
        self.call_post_run_function()

        return str(self.output)

    # CLEANUP METHODS
    def abort(
        self,
        logging_handler: LoggingHandler
    ) -> None:
        """
        Send a signal to abort the command

        Parameters
        ----------
        logging_handler: LoggingHandler
            The LoggingHandler object which stores the logging functions, logging threads, logger information, etc.

        Returns
        -------
        Nothing
        """

        if self.on_shell:
            LogMessage.Critical(message= "Aborting the currently running command `" + self.command_string + "`", is_silent= self.is_silent).write(logging_handler= logging_handler)
        else:
            LogMessage.Critical(message= "Aborting the currently running command `" + " ".join(self.command_strings) + "`", is_silent= self.is_silent).write(logging_handler=logging_handler)

        self.do_abort = True

        self._end_processes()
        self.processes.clear()
        self.has_completed = False
        self.is_running = False

    # OPERATOR OVERLOADS

    # OPERATOR OVERLOADS: INPUT REDIRECTION
    # Usage example: `command = Command(["cat"]) < pathlib.Path("file.txt")`
    def __lt__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the source for stdin.
        Overloads the < operator.
        Usage example: `command = Command(["cat"]) < pathlib.Path("file.txt")`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.input_redirect_from_file(filepath)

    # Usage example: `command = Command(["grep", "bread"]) << "I eat peanut butter with bread"`
    def __lshift__(self, string_input: str) -> Command:
        """
        Store the input string for sending to stdin through Popen.stdin.write
        Overloads the `<<` operator
        Usage example: `command = Command(["grep", "bread"]) << "I eat peanut butter with bread"`

        Parameters
        ----------
        string_input : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.input_redirect_from_string(string_input)


    # OPERATOR OVERLOADS: OUTPUT REDIRECTION
    # Usage example: `command = Command(["echo", "Hello"]) > pathlib.Path("file.txt")`
    def __gt__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the destination for stdout.
        Overloads the > operator.
        Usage example: `command = Command(["echo", "Hello"]) > pathlib.Path("file.txt")`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.output_redirect_to_file(filepath)

    # Usage example: `command = Command(["echo", "Hello"]) >= pathlib.Path("file.txt")`
    def __ge__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the destination for stdout and stderr.
        Overloads the >= operator.
        Usage example: `command = Command(["echo", "Hello"]) >= pathlib.Path("file.txt")`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.output_and_error_redirect_to_file(filepath)

    # Usage example: `command = Command(["echo", "Hello"]) >> pathlib.Path("non_empty_file.txt")`
    def __rshift__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the append destination for stdout
        Overloads the `>>` operator
        Usage example: `command = Command(["echo", "Hello"]) >> pathlib.Path("non_empty_file.txt")`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        self.append_output_to_file(filepath)
        return self


    # OPERATOR OVERLOADS: MISC
    # Usage example: `command = Command(["echo", "Hello my green umbrella"]) | Command(["grep", "umbrella"])`
    def __or__(self, other_command: Command) -> Command:
        """
        Store the next command to pipe the output to
        Overloads the `|` operator
        Usage example: `command = Command(["echo", "Hello my green umbrella"]) | Command(["grep", "umbrella"])`

        Parameters
        ----------
        other_command : Command
            The command to pipe to

        Returns
        -------
        Command
            The modified instance
        """

        return self.pipe_to(other_command)

    # Usage example: `command = Command(["echo", "Hello my green umbrella"]) |= Command(["grep", "umbrella"])`
    def __ior__(self, other_command: Command) -> Command:
        """
        Store the next command to pipe the output to
        Overloads the `|=` operator
        Usage example: `command = Command(["echo", "Hello my green umbrella"]) |= Command(["grep", "umbrella"])`

        Parameters
        ----------
        other_command : Command
            The command to pipe to

        Returns
        -------
        Command
            The modified instance
        """

        return self.pipe_all_to(other_command)

    # Usage example: `command = Command["ping", "www.google.com"] & None`
    def __and__(self, other: None) -> Command:
        """
        Marks the command to run in the background
        Overloads the `&` operator
        Usage example: `command = Command["ping", "www.google.com"] & None`

        Parameters
        ----------
        _: None
            A None operand

        Returns
        -------
        Command
            The modified instance
        """               
        
        return self.in_background()


    # OPERATOR OVERLOADS: REFLECTED INPUT REDIRECTION
    # Usage example: `command = pathlib.Path("file.txt") > Command(["cat"])`
    def __rgt__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the source for stdin.
        Overloads the < operator.
        Usage example: `command = pathlib.Path("file.txt") > Command(["cat"])`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.input_redirect_from_file(filepath)

    # Usage example: `command = "I eat peanut butter with bread" >> Command(["grep", "bread"])`
    def __rrshift__(self, string_input: str) -> Command:
        """
        Store the input string for sending to stdin through Popen.stdin.write
        Overloads the `<<` operator
        Usage example: `command = "I eat peanut butter with bread" >> Command(["grep", "bread"])`

        Parameters
        ----------
        string_input : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.input_redirect_from_string(string_input)


    # OPERATOR OVERLOADS: REFLECTED OUTPUT REDIRECTION
    # Usage example: `command = pathlib.Path("file.txt") < Command(["echo", "Hello"])`
    def __rlt__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the destination for stdout.
        Overloads the > operator.
        Usage example: `command = pathlib.Path("file.txt") < Command(["echo", "Hello"])`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.output_redirect_to_file(filepath)

    # Usage example: `command = pathlib.Path("file.txt") <= Command(["echo", "Hello"])`
    def __rle__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the destination for stdout and stderr.
        Overloads the >= operator.
        Usage example: `command = pathlib.Path("file.txt") <= Command(["echo", "Hello"])`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.output_and_error_redirect_to_file(filepath)

    # Usage example: `command = pathlib.Path("non_empty_file.txt") << Command(["echo", "Hello"])`
    def __rlshift__(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the append destination for stdout
        Overloads the `>>` operator
        Usage example: `command = pathlib.Path("non_empty_file.txt") << Command(["echo", "Hello"])`

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        return self.append_output_to_file(filepath)

    # COMMAND BUILDING METHODS

    # COMMAND BUILDING METHODS: INPUT REDIRECTION
    def input_redirect_from_file(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the source for stdin

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the input file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = "<"
        self.stdin_external_source = filepath
        return self

    def input_redirect_from_string(self, string_input: str) -> Command:
        """
        Store the input string for sending to stdin through Popen.stdin.write        

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = "<<"
        self.stdin_external_source = string_input
        return self

    # COMMAND BUILDING METHODS: OUTPUT REDIRECTION
    def output_redirect_to_file(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the destination for stdout        

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = ">"
        self.stdout_external_destination = filepath
        return self

    def output_and_error_redirect_to_file(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the destination for stdout        

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = ">="
        self.stdout_external_destination = filepath
        return self

    def append_output_to_file(self, filepath: pathlib.Path) -> Command:
        """
        Store the details of a file as the append destination for stdout        

        Parameters
        ----------
        filepath : pathlib.Path
            Relative/absolute filepath of the output file as a pathlib.Path object

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = ">>"
        self.stdout_external_destination = filepath
        return self

    # COMMAND BUILDING METHODS: MISCELLANEOUS
    def pipe_to(self, other_command: Command) -> Command:
        """
        Store the next command to pipe the output to        

        Parameters
        ----------
        other_command : Command
            The command to pipe to

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = "|"
        self.next_pipe_command = other_command
        return self

    def pipe_all_to(self, other_command: Command) -> Command:
        """
        Store the next command to pipe the stdout and stderr to
        
        Parameters
        ----------
        other_command : Command
            The command to pipe to

        Returns
        -------
        Command
            The modified instance
        """

        if self.on_shell:
            raise Command.TYPE_ERROR

        self.rightside_operator = "|="
        self.next_pipe_command = other_command
        return self

    def in_background(self) -> Command:
        """
        Mark the command as to be run in the background        

        Returns
        -------
        Command
            The modified instance
        """  

        if self.on_shell:
            raise Command.TYPE_ERROR             

        self.rightside_operator = "&"
        raise NotImplementedError("The `&` operator to run commands in the background has not been implemented yet.")
        # return self

    # ITERATOR METHODS

    def __iter__(self) -> Command:
        """
        Implemented to make this class iterable

        Returns
        -------
        Command
            The current instance
        """

        return self

    def __next__(self) -> Command:
        """
        Implemented to make this class iterable.
        Returns the next command in the pipe chain

        Returns
        -------
        Command
            The next command in the pipe chain
        """

        if self.command_pointer is None:
            raise StopIteration()
        else:
            command: Command = self.command_pointer
            self.command_pointer = self.command_pointer.next_pipe_command
            return command

    # PRIVATE METHODS  
    def _shell_command_worker(self) -> subprocess.Popen:
        """
        Executes the command string *in a shell* through subprocess.Popen

        Parameters
        ----------
        None

        Returns
        -------
        subprocess.Popen
            The started process handle
        """

        return subprocess.Popen(
            args= self.command_string,
            shell= True,
            stdin= subprocess.PIPE,
            stdout= subprocess.PIPE,
            stderr= subprocess.PIPE,
            cwd= self.working_directory,
            env= self.environment,
            universal_newlines= Command.UNIVERSAL_NEWLINES,
            bufsize= Command.BUFFER_SIZE                      
        )

    @staticmethod
    def _command_part_worker(command_part: Command) -> subprocess.Popen:
        """
        For a given command part within a chain of `pipes`, runs the particular part using subprocess.Popen

        Parameters
        ----------
        command_part: Command
            The command part to be run

        Returns
        -------
        subprocess.Popen
            The process that was started
        """

        return subprocess.Popen(
            args= command_part.command_strings,
            shell= False,
            stdin= command_part.stdin_subprocess,
            stdout= command_part.stdout_subprocess,
            stderr= command_part.stderr_subprocess,
            cwd= command_part.working_directory,
            env= command_part.environment,
            universal_newlines= Command.UNIVERSAL_NEWLINES,
            bufsize= Command.BUFFER_SIZE                     
        )
 
    def _end_processes(self) ->None:
        """
        Ends the all the processes associated with the command

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """
    
        for process in self.processes:
            try:
                if self.on_shell: # If the command is marked to run with shell= True on subprocess.Popen
                    os.killpg(
                        os.getpgid(process.pid),
                        signal.SIGKILL
                    )
                    process.wait()
                else: # If the command is marked to run with shell= False on subprocess.Popen
                    process.kill()
            except Exception as _:
                pass
     
class BatchJob(AbstractRunnable):
    """
    Create queue of tasks that can be run in sequence on a separate non-blocking thread, while logging all the output live.

    Every command that is run and its output are usually displayed on the GUI and also written to the log file in `log` directory. For scripts, both the script path and its internal commands (one level deep) are logged in addition to the output. The logging process is **live** : for every monitored _job_, there is a _boss_ thread (separate from the main thread) that runs tasks in sequence. The _worker_ spawns a subprocess (through Python's `subprocess.Popen`) for running a command or a script and also starts polling the subprocess for live `stdout` and `stderr` output until the task finishes. This means that for a long running task that fails, you would know what the last output was, before it exited.

    Attributes
    ----------
    thread_name: str
        Name for prefixing the threads
    logging_handler: Optional[LoggingHandler]
        The LoggingHandler object which stores the logging functions, logging threads, logger information, etc.
    pre_run_function: functools.partial
        A function to be called before the monitored job starts. Its name and arguments are wrapped together by calling functools.partial
    post_run_function: functools.partial
        A function to be called after the monitored job finishes. Its name and arguments are wrapped together by calling functools.partial
    tasks: Deque[Union[BatchJob, Command, Function, LogMessage]]
        The queue of tasks to be run in a sequence
    thread_name: str
        The name of the thread
    boss_thread: threading.Thread
        The boss thread
    current_process: Optional[subprocess.Popen]
        The currently running process
    current_task: Optional[Union[BatchJob, Command, LogMessage, Function]]
        The currently running process
    
    TODO
    ----
     - Implement timeout for commands and scripts

    """

    # CONSTRUCTOR

    def __init__(
        self,
        thread_name: str = "BatchJob",
        logging_handler: Optional[LoggingHandler] = None,
        *, # The arguments following this must all have a name. For example, function(a= 1, text= "hello")
        pre_run_function: Optional[functools.partial] = None,
        post_run_function: Optional[functools.partial] = None
    ) -> None:
        """
        Initialize a 'BatchJob' instance
        
        Parameters
        ----------
        thread_name: str, default "BatchJob"
            Name for prefixing the threads
        logging_handler: Optional[LoggingHandler]
            The LoggingHandler object which stores the logging functions, logging threads, logger information, etc.
        pre_run_function: Optional[functools.partial], default None
            A function to be called before the monitored job starts. Its name and arguments are wrapped together by calling functools.partial
        post_run_function: Optional[functools.partial], default None
            A function to be called after the monitored job finishes. Its name and arguments are wrapped together by calling functools.partial
        """
        
        # Assign attributes from arguments
        self.logging_handler: Optional[LoggingHandler] = logging_handler

        # Initialize threading attributes
        self.thread_name: str = thread_name    
        self.boss_thread: threading.Thread = threading.Thread(
            target= self._boss,
            name= self.thread_name + "_Boss"
        )

        # Initialize other attributes
        self.tasks: Deque[Union[BatchJob, Command, Function, LogMessage]] = collections.deque([])
        self.current_process: Optional[subprocess.Popen] = None
        self.current_task: Optional[Union[BatchJob, Command, Function, LogMessage]] = None

        # Call the parent class constructor
        super().__init__(
            is_silent= False,
            pre_run_function= pre_run_function,
            post_run_function= post_run_function,
            do_send_output_to_post_run_function= False
        )
       
    # REGULAR METHODS

    def queue(self, task: Union[BatchJob, Command, Function, LogMessage]) -> None:
        """
        Add the provided task to a queue to be executed and logged.

        Parameters
        ----------
        task : Union[BatchJob, Command, Function, LogMessage]
            The task to be queued
        
        Returns
        -------
        Nothing
        """

        self.tasks.append(task)
    
    def start(self) -> None:
        """
        Start running the added commands (from the task queue) in order,
        by running self._boss() on a separate thread

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """

        self.do_abort = False

        # Start a boss thread to run the method _boss()
        self.boss_thread.start()
   
    # OVERLOADED OPERATORS

    # Usage examples: 
    # `batch_job += Command(["echo", "Hello"])`
    # `batch_job += Function(print, "Hello")`
    # `batch_job += LogMessage.Info("Hello")`
    # `batch_job += batch_job2`
    def __iadd__(self: BatchJob, other: Union[BatchJob, Command, Function, LogMessage]) -> BatchJob:
        """
        Overloads the += operator to add tasks or other monitored jobs to the queue
        Usage examples: 
        `batch_job += Command(["echo", "Hello"])`
        `batch_job += Function(print, "Hello")`
        `batch_job += LogMessage.Info("Hello")`
        `batch_job += batch_job2`

        Parameters
        ----------
        other : Union[BatchJob, Command, Function, LogMessage]
            The second operand

        Returns
        -------
        BatchJob
            The modified BatchJob instance with the new task in queue
        """

        self.queue(other)
        return self

    # CLEANUP METHODS

    def clear_tasks(self) -> None:
        """
        Clears the queue of added commands and scripts

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """

        self.tasks.clear()

    def abort(self) -> None:
        """
        Send a signal to abort the monitored job

        Parameters
        ----------
        Nothing

        Returns
        -------
        Nothing
        """

        LogMessage.Critical(
            message= "An abort request has been received. Terminating the currently running process and exiting...",
            is_silent= False
        ).write(logging_handler= self.logging_handler)
        self.do_abort = True
        self.clear_tasks()
        self._end_process()
        self.has_completed = False
        self.is_running = False

    # PRIVATE METHODS

    def _boss(self) -> None:
        """
        Start running the added commands (from the tasks queue) in order.

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """

        self.call_pre_run_function() # Call the global pre_run_function that executes before the job starts (before any task).
        self.is_running = True
        self.has_completed = False

        for self.current_task in self.tasks: # For every task in the list in order 
            if self.do_abort: # If an abort request has been sent
                self.has_completed = True
                return # Do nothing and exit            
            _ = self._task_worker(self.current_task) # Start the task
        
        self.is_running = False
        self.has_completed = True
        self.call_post_run_function() # Call the global post_run_function that executes after the whole job (including all the tasks) is completed
    
    def _task_worker(self, task: Union[BatchJob, Command, LogMessage, Function]) -> Optional[Any]:
        """
        Runs the task and logs the output live if permitted. Also returns the collected output

        Parameters
        ----------
        task:Union[BatchJob, Command, LogMessage, Function]
            The task to be run

        Returns
        -------
        output: Optional[Any]
            The collected output
        """

        if isinstance(task, BatchJob): # Another batch job
            task.start() # Start the batch job
            task.boss_thread.join() # Wait for the batch job to finish
            return None # Exit this function
        elif isinstance(task, LogMessage): # Log Message
            task.write(self.logging_handler)
            return task.message
        elif isinstance(task, Function): # Function
            return task.run_and_log(logging_handler= self.logging_handler)
        elif isinstance(task, Command): # Command            
            return task.run_log_and_wait(logging_handler= self.logging_handler)

    def _end_process(self) ->None:
        """
        Ends the currently running process from the task queue

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """
    
        if isinstance(self.current_task, Command): # If the current task is a command
            try:
                if self.current_task.on_shell: # If the current task is marked to run with shell= True on subprocess.Popen
                    os.killpg(
                        os.getpgid(self.current_process.pid),
                        signal.SIGKILL
                    )
                    self.current_process.wait()
                else: # If the current task is marked to run with shell= False on subprocess.Popen
                    self.current_process.kill()
            except Exception as _:
                pass
            self.current_task.has_completed = False
            self.current_task.is_running = False        
        else: # If the current task is not a command
            return # Do nothing
