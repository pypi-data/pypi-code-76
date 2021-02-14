import unittest
from datetime import datetime

from codenotes import parse_args
from codenotes.cli.tasks import AddTask, SearchTask


class TestAddTask(unittest.TestCase):
    # ! format_task_text function is indirectly tested
    def test_add_bad_input_task(self):
        """ Test bad task input, when is only typed ; """
        args = parse_args(['add', 'task', ';'])
        add_task = AddTask(args)

        self.assertTrue(isinstance(add_task.task, list))
        self.assertListEqual(add_task.task, [])

    def test_add_task_and_category(self):
        args = parse_args(['add', 'task', 'CLI', 'task', '--category','CLI', 'Category'])
        add_task = AddTask(args)

        self.assertEqual(add_task.category_id, 2)
        self.assertEqual(add_task.category_name, 'CLI Category')
        self.assertEqual(add_task.task, 'CLI task')
        
        args = parse_args([
            'add', 'task', 'Task', 'in','same', 'category', '--category','CLI', 'Category'
            ])
        add_task = AddTask(args)

        self.assertEqual(add_task.category_id, 2)
        self.assertEqual(add_task.category_name, 'CLI Category')
        self.assertEqual(add_task.task, 'Task in same category')

    def test_add_many_tasks(self):
        """ Test the storage of two tasks """
        args = parse_args(['add', 'task', 'New task #2;New task #3'])
        add_task = AddTask(args)

        self.assertTrue(isinstance(add_task.task, list))
        self.assertListEqual(add_task.task, ['New task #2', 'New task #3'])

    def test_add_one_task(self):
        """ Test the storage of one task """
        args = parse_args(['add', 'task', 'New task #1'])
        add_task = AddTask(args)

        self.assertTrue(isinstance(add_task.task, str))
        self.assertEqual(add_task.task, 'New task #1')


class TestSearchTask(unittest.TestCase):

    def setUp(self) -> None:
        self.date = datetime.now().date().strftime('%Y-%m-%d')
        self.default_category_name = 'TODO Tasks'

    def test_search_month_task(self):
        # Stores a fourth task
        args = parse_args(['add', 'task', 'Different', 'task'])
        AddTask.set_args(args)

        expected_tasks = [
            ('New task #1', 0, self.date, self.default_category_name),
            ('New task #2', 0, self.date, self.default_category_name),
            ('New task #3', 0, self.date, self.default_category_name),
            ('Different task', 0, self.date, self.default_category_name),
            ('CLI task', 0, self.date, 'CLI Category'),
            ('Task in same category', 0, self.date, 'CLI Category')
        ]

        args = parse_args(['search', 'task', '--month'])
        query = SearchTask(args).sql_query()

        self.assertCountEqual(query, expected_tasks)

    def test_search_text_date(self):
        """ Test that search only one task by keywords and date in common """

        expected_tasks=[
            ('Different task', 0, self.date, self.default_category_name)
        ]
        args = parse_args(['search', 'task', 'Different', '--today'])
        query = SearchTask(args).sql_query()

        self.assertCountEqual(query, expected_tasks)

    def test_search_text_task(self):
        """ Test that search all tasks that match to some keywords  """
        expected_tasks = [
            ('New task #1', 0, self.date, self.default_category_name),
            ('New task #2', 0, self.date, self.default_category_name),
            ('New task #3', 0, self.date, self.default_category_name)
        ]
        args = parse_args(['search', 'task', 'New', 'task'])
        query = SearchTask(args).sql_query()

        self.assertCountEqual(query, expected_tasks)

    def test_search_today_task(self):
        """ Test that search for the four tasks added """
        expected_tasks = [
            ('New task #1', 0, self.date, self.default_category_name),
            ('New task #2', 0, self.date, self.default_category_name),
            ('New task #3', 0, self.date, self.default_category_name),
            ('Different task', 0, self.date, self.default_category_name),
            ('CLI task', 0, self.date, 'CLI Category'),
            ('Task in same category', 0, self.date, 'CLI Category')
        ]

        args = parse_args(['search', 'task', '--today'])
        query = SearchTask(args).sql_query()

        self.assertCountEqual(query, expected_tasks)

    def test_search_yesterday_task(self):
        expected_tasks = []

        args = parse_args(['search', 'task', '--yesterday'])
        query = SearchTask(args).sql_query()

        self.assertCountEqual(query, expected_tasks)

    def tearDown(self) -> None:
        del self.date
        del self.default_category_name


if __name__ == '__main__':
    unittest.main()
