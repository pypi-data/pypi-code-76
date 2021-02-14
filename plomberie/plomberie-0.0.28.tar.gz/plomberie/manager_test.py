from typing import Optional, List, Callable
from unittest import TestCase

from timeout_decorator import timeout

from plomberie import Manager, Task
from plomberie.exceptions import CircularDependencyException


class LeaveHouseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        class LeaveHouseTask(Task):
            def __init__(self, append_to_run_sequence: Callable[['LeaveHouseTask'], None]):
                super().__init__()
                self.__append_to_run_sequence = append_to_run_sequence

            def run(self) -> None:
                self.__append_to_run_sequence(self)

        cls.__run_sequence: List[LeaveHouseTask] = []

        cls.__leave_house = LeaveHouseTask(cls.__run_sequence.append)
        cls.__put_on_shoes = LeaveHouseTask(cls.__run_sequence.append)
        cls.__put_on_pants = LeaveHouseTask(cls.__run_sequence.append)
        cls.__put_on_jacket = LeaveHouseTask(cls.__run_sequence.append)
        cls.__put_on_shirt = LeaveHouseTask(cls.__run_sequence.append)
        cls.__put_on_socks = LeaveHouseTask(cls.__run_sequence.append)
        cls.__put_on_underwear = LeaveHouseTask(cls.__run_sequence.append)
        cls.__take_shower = LeaveHouseTask(cls.__run_sequence.append)

        cls.__leave_house.depends_on(cls.__put_on_shoes, cls.__put_on_jacket)
        cls.__put_on_shoes.depends_on(cls.__put_on_pants, cls.__put_on_socks)
        cls.__put_on_pants.depends_on(cls.__put_on_underwear)
        cls.__put_on_jacket.depends_on(cls.__put_on_shirt)
        cls.__put_on_shirt.depends_on(cls.__take_shower)
        cls.__put_on_socks.depends_on(cls.__take_shower)
        cls.__put_on_underwear.depends_on(cls.__take_shower)

        manager = Manager()
        manager.launch(cls.__leave_house)

    def test_leave_house_last(self):
        self.assertEqual(self.__run_sequence[-1], self.__leave_house)

    def test_put_on_shoes_and_jacket_before_leaving(self):
        self.__assert_sequence(self.__put_on_shoes, self.__leave_house)
        self.__assert_sequence(self.__put_on_jacket, self.__leave_house)

    def test_take_a_shower_first(self):
        self.assertEqual(self.__run_sequence[0], self.__take_shower)

    def test_all_tasks_completed(self):
        self.assertEqual(8, len(self.__run_sequence))

    def __assert_sequence(self, first_test_task: Task, second_test_task: Task) -> None:
        index_of_first = self.__get_call_index(first_test_task)
        index_of_second = self.__get_call_index(second_test_task)
        self.assertLess(index_of_first, index_of_second)

    def __get_call_index(self, task: Task) -> Optional[int]:
        return next((i for i, t in enumerate(self.__run_sequence) if t == task), None)


class CircularDependencyTest(TestCase):
    @timeout(1)
    def test_circular_dependency(self):
        class TestTask(Task):
            def run(self) -> None:
                pass

        manager = Manager()
        task_a = TestTask()
        task_b = TestTask()
        task_c = TestTask()
        task_a.depends_on(task_b)
        task_b.depends_on(task_c)
        task_c.depends_on(task_a)
        self.assertRaises(CircularDependencyException, lambda: manager.launch(task_a))
