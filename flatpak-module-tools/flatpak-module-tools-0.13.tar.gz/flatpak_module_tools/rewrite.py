#!/usr/bin/python

import click
from enum import Enum
import sys
import shutil
from datetime import datetime, timezone
import time

class TaskState(Enum):
    PENDING =1
    RUNNING = 2
    SUCCEEDED = 3
    FAILED = 4
    SKIPPED = 5

class Task:
    def __init__(self, name):
        self.name = name
        self.timestamps = {}
        self.state = TaskState.PENDING

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.timestamps[state] = datetime.now(tz=timezone.utc)

class TaskProgress:
    def __init__(self):
        self.lines_written = 0
        self.tasks = set()

    def add_task(self, task):
        self.tasks.add(task)

    def erase(self):
        for i in range(0, self.lines_written):
            sys.stdout.write("\x1b[1A\x1b[2K") # move up cursor and delete whole line
        self.lines_written = 0

    def render_task_list_short(self, header, tasks, fg=None):
        sys.stdout.write(click.style(header, bold=True) + '\n')
        self.lines_written += 1
        column = 1
        n_total = 0
        for task in tasks:
            if n_total == 0:
                prefix = '  '
            else:
                prefix = ' '

            if n_total == len(tasks) - 1:
                suffix = ''
            else:
                suffix = ','

            if column + len(prefix) + len(task.name) + len(suffix) > self.width:
                sys.stdout.write('\n ')
                column = 1
                self.lines_written += 1

            column += len(prefix + task.name + suffix)
            sys.stdout.write(prefix + click.style(task.name, fg=fg) + suffix)
        sys.stdout.write('\n')
        self.lines_written += 1

    def render_task_list_long(self, header, tasks, include_duration=False, fg=None):
        sys.stdout.write(click.style(header, bold=True) + '\n')
        self.lines_written += 1
        for task in tasks:
            unstyled_line = '  ' + task.name + ' [Log: /etc/passwd]'
            line = '  ' + click.style(task.name, fg=fg) + ' [Log: \x1b]8;;file:/etc/passwd\x1b\\/etc/passwd\x1b]8;;\x1b\\]'
            if include_duration:
                duration = (self.now - task.timestamps[task.state]).total_seconds()
                duration_minutes = int(duration // 60)
                duration_string = f"[{duration_minutes:02d}:{duration - duration_minutes * 60:04.1f}]"
                sys.stdout.write(line + (self.width - (len(unstyled_line) + len(duration_string))) * " " + duration_string + "\n")
            else:
                sys.stdout.write(line + '\n')
            self.lines_written += 1

    def render(self):
        self.width, _ = shutil.get_terminal_size((80, 20))
        self.now = datetime.now(tz=timezone.utc)

        self.erase()

        def filter_tasks(state):
            return list(sorted((t for t in self.tasks if t.state == state), key=lambda t: t.name))

        pending_tasks = filter_tasks(TaskState.PENDING)
        running_tasks = filter_tasks(TaskState.RUNNING)
        succeeded_tasks = filter_tasks(TaskState.SUCCEEDED)
        failed_tasks = filter_tasks(TaskState.FAILED)
        skipped_tasks = filter_tasks(TaskState.SKIPPED)

        if pending_tasks:
            self.render_task_list_short('Pending:', pending_tasks)
        if running_tasks:
            self.render_task_list_long('Running:', running_tasks, include_duration=True)
        if succeeded_tasks:
            self.render_task_list_short('Succeeded:', succeeded_tasks, fg='green')
        if failed_tasks:
            self.render_task_list_long('Failed:', failed_tasks, fg='red')
        if skipped_tasks:
            self.render_task_list_short('Skipped:', skipped_tasks)

foo_task = Task('Foo')
bar_task = Task('Bar')
baz_task = Task('Baz')
progress = TaskProgress()
progress.add_task(foo_task)
progress.add_task(bar_task)
progress.add_task(baz_task)

click.secho("Compiling module...", bold=True)
progress.render()
time.sleep(0.75)
foo_task.state = TaskState.RUNNING
progress.render()
time.sleep(1.5)
bar_task.state = TaskState.RUNNING
progress.render()
time.sleep(1.5)
foo_task.state = TaskState.SUCCEEDED
progress.render()
time.sleep(1.5)
bar_task.state = TaskState.FAILED
baz_task.state = TaskState.SKIPPED
progress.render()
