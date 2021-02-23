from unittest import TestCase


class TestExample(TestCase):
    def test_sum(self):
        from flask_templates.async_task import async_tasker

        while True:
            res = async_tasker.delay('flask_templates.async_task.example.sum', 1, 3)
            print(res.state)
            try:
                print(res.get(timeout=10))

            except Exception as e:
                import traceback
                traceback.print_exc()

