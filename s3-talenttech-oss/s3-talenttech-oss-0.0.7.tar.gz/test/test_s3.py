import random
import string

from s3.client import Client

client = Client()

LOCAL_FILE = "test/data/file.txt"


def random_string(string_length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class test_context(object):

    def __init__(self, cl):
        self.client = cl
        self.root_dir = random_string()

    def __enter__(self):
        return self.root_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.delete_dir(self.root_dir)


def test_dir_wrap():
    path = '{}/{}'.format(random_string(), random_string())
    wrapped_1 = client.dir_to_s3(path)
    wrapped_2 = client.dir_to_s3(path + '/')
    wrapped_3 = client.dir_to_s3('/' + path)
    assert wrapped_1 == path + '/'
    assert wrapped_2 == path + '/'
    assert wrapped_3 == path + '/'


def test_delete():
    root_dir = '{}'.format(random_string())
    client.create_dir(root_dir)
    assert client.path_exists(root_dir) == True
    client.delete_dir(root_dir)
    assert client.path_exists(root_dir) == False


def test_list_file():
    n = 15
    with test_context(client) as root_dir:
        for i in range(n):
            file_name = '{}.txt'.format(random_string())
            file_path = '{}/{}'.format(root_dir, file_name)
            client.create_file(file_path)

        file_list = client.get_file_list(root_dir)

        assert len(file_list) == n

    # after exit
    file_list = client.get_file_list(root_dir)
    assert len(file_list) == 0


def test_create_empty_file():
    with test_context(client) as root_dir:
        file_name = '{}.txt'.format(random_string())
        file_path = '{}/{}'.format(root_dir, file_name)
        client.create_file(file_path)
        s3_file_data = client.read_file(file_path)
        assert len(s3_file_data) == 0


def test_create_file():
    with test_context(client) as root_dir:
        file_name = '{}.txt'.format(random_string())
        file_path = '{}/{}'.format(root_dir, file_name)
        test_f = open(LOCAL_FILE, "r")
        test_data = test_f.read()
        client.create_file(file_path, test_data)
        s3_file_data = client.read_file(file_path)
        assert test_data == s3_file_data


def test_upload_file():
    with test_context(client) as root_dir:
        file_name = '{}.txt'.format(random_string())
        file_path = '{}/{}'.format(root_dir, file_name)

        test_f = open(LOCAL_FILE, "r")
        test_data = test_f.read()

        client.upload_file(LOCAL_FILE, file_path)

        s3_file_data = client.read_file(file_path)

        assert test_data == s3_file_data


def test_bulk_read():
    with test_context(client) as root_dir:
        file_name = '{}.txt'.format(random_string())
        file_path = '{}/{}'.format(root_dir, file_name)
        client.create_file(file_path, 'qwe')

        file_name = '{}.txt'.format(random_string())
        file_path = '{}/{}'.format(root_dir, file_name)
        client.create_file(file_path, 'rty')

        data = client.bulk_read(root_dir)

        assert 'qwe' in data
        assert 'rty' in data
