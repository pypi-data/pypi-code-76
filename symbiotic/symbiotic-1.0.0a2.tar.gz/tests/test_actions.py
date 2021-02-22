from unittest import TestCase

from symbiotic.actions import Action
from symbiotic.schedule import Schedule


class Test_Action_Unit(TestCase):

    def test_create_action_without_args(self):
        def mock_callback():
            pass

        action = Action(mock_callback)
        self.assertIsNotNone(action._callback)
        self.assertEqual((), action._callback.args)
        self.assertEqual({}, action._callback.keywords)

    def test_create_action_with_args(self):
        def mock_callback(**kwargs):
            return kwargs.pop('saywhat')

        action = Action(mock_callback, saywhat='what')
        response = action()

        self.assertEqual(action._callback.keywords, {'saywhat': 'what'})
        self.assertEqual('what', response)

    def test_create_action_with_schedule(self):
        def callback():
            pass
        action = Action(callback)
        schedule = Schedule().every_day().at('12:15')
        action.set_schedule(schedule)
