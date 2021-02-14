import asyncio
from typing import Dict, Set, Type

from plomberie import Task
from plomberie.exceptions import CircularDependencyException
from plomberie.progress_bar.abstract_progress_bar import AbstractProgressBar
from plomberie.progress_bar.disabled_progress_bar import DisabledProgressBar
from plomberie.progress_bar.lazy_loaded_progress_bar import LazyLoadedProgressBar


class Manager:
    def __init__(self, enable_progress_bar: bool = True):
        self.__progress_bar: Type[AbstractProgressBar] = LazyLoadedProgressBar if enable_progress_bar \
            else DisabledProgressBar

    def launch(self, root_task: Task) -> None:
        dependency_map = self.__get_dependency_map(root_task)
        while dependency_map:
            ready_to_run = set(task for task, dependencies in dependency_map.items() if not dependencies)
            for task in ready_to_run:
                task.set_progress_bar(self.__progress_bar)
                task.run()
                task.post_run()
            dependency_map = {
                task: dependencies - ready_to_run
                for task, dependencies in dependency_map.items() if dependencies
            }

    def __get_dependency_map(self, task: Task) -> Dict[Task, Set[Task]]:
        dependency_map: Dict[Task, Set[Task]] = {}
        tasks = {task}
        while tasks:
            task = tasks.pop()
            dependencies = set(task.dependencies)
            dependency_map[task] = dependencies
            self.__detect_circular_dependency(dependency_map)
            tasks.update(dependencies)
        return dependency_map

    # TODO: is there a more efficient way to detect circular dependencies?
    @staticmethod
    def __detect_circular_dependency(dependency_map: Dict[Task, Set[Task]]) -> None:
        for task, dependencies in dependency_map.items():
            dependency_stack = set(dependencies)
            while dependency_stack:
                dependency = dependency_stack.pop()
                if task == dependency:
                    raise CircularDependencyException()
                dependency_stack.update(dependency.dependencies)
