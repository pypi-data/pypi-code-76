import unittest
import logging
import pandas as pd

from s3_log_query.S3LogQuery import LogQuery


class TestLogQuery(unittest.TestCase):
    def setUp(self):
        self.log_query = LogQuery(log_paths={'server1': 'server1/server1.log', 'db server': 'db_server/db_server.log',
                                             'server2': 'server2/server2.log', 'server3': 'server3/server3/log'},
                                  s3_bucket='mikethoun-logs')


class TestQuery(TestLogQuery):
    def test_query_server1(self):
        data = [['02/28/2020 5:20:56.25', 'warn', 'Rejecting request: No such database.', 'db server'],
                ['02/28/2020 5:20:56.45', 'warn', 'Database “my_db7” did not exist', 'server1'],
                ['02/28/2020 5:20:57.25', 'warn',
                 'Rejecting request: User does not have sufficient quota to create database.', 'db server'],
                ['02/28/2020 5:20:57.35', 'error',
                 'Could not create database “my_db7”. Database server rejected request.', 'server1'],
                ['02/28/2020 5:20:57.45', 'fatal', 'Unable to write to database “my_db7”. Exiting.', 'server1']]

        test = pd.DataFrame(data, columns=['timestamp', 'severity', 'message', 'server'])
        test.set_index('timestamp', inplace=True)

        result = self.log_query.query(start='02/28/2020 5:20:55', entries=100, keys=['server1', 'db server'],
                                      min_severity=logging.WARN, output='dataframe')

        pd.testing.assert_frame_equal(test, result)


if __name__ == '__main__':
    unittest.main()
