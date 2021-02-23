import functools
from contextlib import contextmanager
import threading
import os
import json
import sqlite3

try:
    FileNotFoundError
except:
    FileNotFoundError = IOError


def _open_file_info(fname):
    with open(fname, 'rt') as f:
        return json.load(f)


def save_record(resource_id):
    conn = SqliteTabel()
    for id, remote in resource_id.items():
        conn.select_sql_query(['category_id'], 'resource_category', ['resource_id=?'])
        local_category_id = conn.execute_sql_query((id,))
        if set(local_category_id) ^ set(remote):
            delete_record = set(local_category_id) - set(remote)
            if delete_record:
                conn.delete_sql_query('resource_category', ['resource_id=?', 'category_id=?'])
                conn.execute_query(id, delete_record)
            insert_record = set(remote) - set(local_category_id)
            if insert_record:
                conn.insert_sql_query('resource_category', "(?, ?)")
                conn.execute_query(id, insert_record)
    conn.connection.close()


def get_sample_datasets_dir():
    orange_data_table = os.path.dirname(__file__)
    dataset_dir = os.path.join(orange_data_table, '..', 'datasets')
    return os.path.realpath(dataset_dir)


def _create_path(target):
    try:
        os.makedirs(target)
    except OSError:
        pass


def _keyed_lock(lock_constructor=threading.Lock):
    lock = threading.Lock()
    locks = {}

    def get_lock(key):
        with lock:
            if key not in locks:
                locks[key] = lock_constructor()
            return locks[key]

    return get_lock


def get_id():
    from .remote import Server
    return Server().open('userinfo')['userId']


_get_lock = _keyed_lock(threading.RLock)


def _split_path(head):
    out = []
    while True:
        head, tail = os.path.split(head)
        out.insert(0, tail)
        if not head:
            break
    return out


class LocalFiles:
    """Manage local files."""

    def __init__(self, path, serverfiles=None):
        super().__init__()
        self.serverfiles_dir = path  # 文件下载路径
        """A folder downloaded files are stored in."""
        _create_path(self.serverfiles_dir)
        self.serverfiles = serverfiles
        """A ServerFiles instance."""

    @contextmanager
    def _lock_file(self, *args):
        path = self.localpath(*args)
        path = os.path.normpath(os.path.realpath(path))
        lock = _get_lock(path)
        lock.acquire(True)
        try:
            yield
        finally:
            lock.release()

    def _locked(f):
        @functools.wraps(f)
        def func(self, *path, **kwargs):
            with self._lock_file(*path):
                return f(self, *path, **kwargs)

        func.unwrapped = f
        return func

    def localpath(self, *args):
        """ Return the local location for a file. """
        return os.path.join(os.path.expanduser(self.serverfiles_dir), *args)

    def add_record(self, remote_category_id, info_id):
        save_record(remote_category_id)
        user_id = get_id()  # 用户的id
        conn = SqliteTabel()
        conn.insert_sql_query('resource_download', "(?, ?)")
        conn.execute_sql_query((user_id, info_id))
        conn.connection.close()


    @_locked
    def download(self, *path, **kwargs):
        """
        :param info_download: dict{}
        :param kwargs:
        :param path: tuple()
        :return:
        """
        callback = kwargs.get("callback", None)
        type = 'DATA' if path[1].endswith('.bw') else 'CASE'
        self.serverfiles.data_type = {'type': type}
        info = self.serverfiles.info(*path)
        target = self.localpath(*(path[1], ))
        self.serverfiles.download(path[0], target=target, callback=callback)
        if type == 'DATA':
            remote_category_id = {}
            remote_category_id[info['id']] = [(i['id'],) for i in info['categories']]
            self.add_record(remote_category_id, info['id'])

    @_locked
    def localpath_download(self, *path, **kwargs):
        """
        Return local path for the given domain and file. If file does not exist,
        download it. Additional arguments are passed to the :obj:`download` function.
        """
        pathname = self.localpath(path[1])
        if not os.path.exists(pathname):
            self.download.unwrapped(self, *path, **kwargs)
        return pathname

    def allinfo(self, suffix=None):
        """Return all local info files in a dictionary, where keys are paths."""
        user_id = get_id()
        conn = SqliteTabel()
        conn.select_sql_query(['resource_id'], 'resource_download', ['user_id=?'])
        local_data = conn.execute_sql_query((user_id,))
        conn.connection.close()
        data = [(i + (i[0]+suffix, )) for i in local_data]
        return data


class SqliteTabel(object):
    sqlite_path = None

    def __init__(self):
        # path = os.path.join(get_sample_datasets_dir(), 'user_name')
        path = os.path.join(get_sample_datasets_dir(), '..', 'user')

        self.connection = sqlite3.connect(path)
        self.query = None

    def select_sql_query(self, fields, table_name=None, filters=(),
                         group_by=None, order_by=None,
                         offset=None, limit=None):

        sql = ['SELECT', ', '.join(fields) if len(fields) > 1 else fields[0],
               "FROM", table_name]
        if filters:
            sql.extend(["WHERE", " AND ".join(filters)])
        if group_by is not None:
            sql.extend(["GROUP BY", ", ".join(group_by)])
        if order_by is not None:
            sql.extend(["ORDER BY", ",".join(order_by)])
        if offset is not None:
            sql.extend(["OFFSET", str(offset)])
        if limit is not None:
            sql.extend(["LIMIT", str(limit)])

        self.query = " ".join(sql)

    def delete_sql_query(self, table_name=None, filter=()):
        sql = ['DELETE', "FROM", table_name]
        sql.extend(["WHERE", " AND ".join(filter) if len(filter) > 1 else filter[0]])
        self.query = " ".join(sql)

    def insert_sql_query(self, table_name, key):
        sql = ['INSERT INTO', table_name, 'VALUES' + key]
        self.query = " ".join(sql)

    def execute_query(self, resource_id, params):
        try:
            cur = self.connection.cursor()
            for param in params:
                cur.execute(self.query, (resource_id, list(param)[0]))
        except Exception as e:
            print('Error', e)
        finally:
            self.connection.commit()

    def execute_sql_query(self, params):
        try:
            cur = self.connection.cursor()
            cur.execute(self.query, params)
            return cur.fetchall()
        except sqlite3.Error as ex:
            print('Error', ex)
        finally:
            self.connection.commit()
