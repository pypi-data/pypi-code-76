import unittest
from tamarin.command import Command
from tamarin.multiprocessing import Todo


class LightTurnOn(Command):
    def execute(self):
        print('light turn on')
        return 'light turn on'


class WakeUp(Command):
    def execute(self):
        print('wake up')
        return 'wake_up'


class MultiProcessingTest(unittest.TestCase):
    first_command = LightTurnOn(None)
    second_command = WakeUp(None)

    def setUp(self) -> None:
        pass

    def test_todo(self):
        commands = [self.first_command, self.second_command]
        todo = Todo(commands=commands)
        response = todo.process()
