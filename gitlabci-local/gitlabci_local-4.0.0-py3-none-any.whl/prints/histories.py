#!/usr/bin/env python3

# Standard libraries
from time import time

# Components
from ..prints.colors import Colors
from ..system.platform import Platform

# TimedHistory class
class TimedHistory:

    # Members
    __duration = 0
    __start_time = 0

    # Constructor
    def __init__(self):
        self.__duration = 0
        self.__start_time = time()

    # Refresh times
    def _refresh_times(self):

        # Evaluate duration
        duration = int(time() - self.__start_time)

        # Evaluate seconds
        seconds = '%.0f second%s' % (duration % 60, 's' if duration % 60 > 1 else '')

        # Evaluate minutes
        minutes = ''
        if duration >= 60:
            minutes = '%.0f minute%s ' % (duration / 60, 's' if duration / 60 > 1 else '')

        # Store total time
        self.__duration = minutes + seconds

    @property
    def duration(self):
        return self.__duration

# JobHistory class
class JobHistory(TimedHistory):

    # Members
    __details = ''
    __failure_allowed = False
    __name = None
    __result = None
    __stage = None

    # Constructor
    def __init__(self, name, stage):
        super().__init__()
        self.__details = ''
        self.__failure_allowed = False
        self.__name = name
        self.__result = None
        self.__stage = stage

    @property
    def failure_allowed(self):
        return self.__failure_allowed

    @failure_allowed.setter
    def failure_allowed(self, value):
        self.__failure_allowed = value

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, value):
        self.__details = value

    @property
    def name(self):
        return self.__name

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = value
        self._refresh_times()

    # Header
    def header(self, jobs_count, image, engine_type):

        # Header output
        if jobs_count > 1:
            print(' ')
        print(' %s===[ %s%s: %s%s %s(%s, %s) %s]===%s' % (
            Colors.GREEN,
            Colors.YELLOW,
            self.__stage,
            Colors.YELLOW,
            self.__name,
            Colors.CYAN,
            image,
            engine_type,
            Colors.GREEN,
            Colors.RESET,
        ))
        print(' ')
        Platform.flush()

    # Footer
    def footer(self):

        # Footer output
        print('  %s‣ %s: %s%s in %s%s%s%s' % (
            Colors.YELLOW,
            self.__name,
            Colors.GREEN if self.result else Colors.RED,
            'Success' if self.result else 'Failure',
            self.duration,
            Colors.CYAN,
            self.details,
            Colors.RESET,
        ))
        print(' ')
        Platform.flush()

    # Print
    def print(self):

        # Variables
        icon = ''
        summary = ''

        # Print result
        if self.result:
            icon = '%s✔' % (Colors.GREEN)
            summary = '%sSuccess in %s' % (Colors.GREEN, self.duration)
        elif self.failure_allowed:
            icon = '%s!' % (Colors.YELLOW)
            summary = '%sFailure in %s' % (Colors.YELLOW, self.duration)
        elif self.result is None:
            icon = '%s»' % (Colors.GREY)
            summary = '%sSkipped' % (Colors.GREY)
        else:
            icon = '%s✘' % (Colors.RED)
            summary = '%sFailure in %s' % (Colors.RED, self.duration)

        # Print result
        print('    %s %s%s: %s%s%s%s' % (
            icon,
            Colors.BOLD,
            self.name,
            summary,
            Colors.CYAN,
            self.details,
            Colors.RESET,
        ))

# StageHistory class
class StageHistory:

    # Members
    __jobs = []
    __name = None

    # Constructor
    def __init__(self, name):
        self.__jobs = []
        self.__name = name

    @property
    def name(self):
        return self.__name

    # Add
    def add(self, job_name):

        # Add job
        job = JobHistory(job_name, self.name)
        self.__jobs += [job]

        # Result
        return job

    # Print
    def print(self):

        # Stage header
        print('  %s• Stage %s:%s' % (
            Colors.YELLOW,
            self.name,
            Colors.RESET,
        ))

        # Iterate through jobs
        for job in self.__jobs:
            job.print()

# PipelineHistory class
class PipelineHistory(TimedHistory):

    # Members
    __jobs_count = 0
    __jobs_quiet = True
    __pipeline = None
    __result = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.__jobs_count = 0
        self.__jobs_quiet = True
        self.__pipeline = []
        self.__result = None

    @property
    def jobs_count(self):
        return self.__jobs_count

    @property
    def jobs_quiet(self):
        return self.__jobs_quiet

    @jobs_quiet.setter
    def jobs_quiet(self, value):
        self.__jobs_quiet = value

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = value
        self._refresh_times()

    # Add
    def add(self, stage_name, job_name):

        # Increment jobs count
        self.__jobs_count += 1

        # Find stage
        stage = self.get(stage_name)

        # Prepare stage
        if not stage:
            stage = StageHistory(stage_name)
            self.__pipeline += [stage]

        # Add job
        job = stage.add(job_name)

        # Result
        return job

    # Get
    def get(self, stage_name):

        # Find stage
        for stage in self.__pipeline:
            if stage.name == stage_name:
                return stage

        # Fallback
        return None

    # Print
    def print(self):

        # Header
        print(' ')
        print(' %s===[ %sPipeline: %s%s jobs %s]===%s' % (
            Colors.GREEN,
            Colors.YELLOW,
            Colors.BOLD,
            self.jobs_count,
            Colors.GREEN,
            Colors.RESET,
        ))
        print(' ')

        # Iterate through stages
        for stage in self.__pipeline:
            stage.print()
            print(' ')

        # Footer
        print('  %s‣ Pipeline: %s%s in %s total%s' % (
            Colors.YELLOW,
            Colors.BOLD if self.result else Colors.RED,
            'Success' if self.result else 'Failure',
            self.duration,
            Colors.RESET,
        ))
        print(' ')
