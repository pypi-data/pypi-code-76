import os
import simple_utils

def test_json_to_csv():
    csv_data = simple_utils.file.json_to_csv([
        {
            'hello': 'world',
            'abc':'def'
        },
        {
            'hello': 'simple',
            'abc':'ghi'
        }
    ]).replace('\r', '')

    assert csv_data == 'hello,abc\nworld,def\nsimple,ghi\n'


def test_read_file():
    assert simple_utils.file.read_file('assets/message.txt') == 'Hello World'

