import asyncio
import configparser
import contextlib
import datetime
import functools
import io
import json
import math
import multiprocessing
import os
import re
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
import zipfile
from unittest import mock

import jsonpyth

from . import cli, playbook, plotting, procfile, procrec, procret, proctree, utility
from .cmd import CommandError, explore, play, plot, query, record, watch


try:
    import apsw
except ImportError:
    apsw = None


class TestUtility(unittest.TestCase):

    def test_evaluate(self):
        actual = utility.evaluate([
            ('A', 'date -I'),
            ('B', 'echo 42')
        ])
        self.assertEqual({'A': datetime.date.today().isoformat(), 'B': '42'}, actual)

    def test_get_meta(self):
        self.assertEqual(
            {'platform_node', 'platform_platform', 'page_size', 'clock_ticks'},
            utility.get_meta().keys(),
        )

    def test_get_line_distance(self):
        self.assertEqual(10, plotting.get_line_distance((0, 0), (10, 0), (10, 0)))
        self.assertEqual(10, plotting.get_line_distance((0, 0), (10, 0), (10, 10)))

        actual = plotting.get_line_distance((90, 51), (34, 15), (-11, -51))
        self.assertAlmostEqual(25.9886, actual, delta=0.00001)

    def test_decimate(self):
        self.assertEqual([(1, 1)], plotting.decimate([(1, 1)], 0))
        self.assertEqual([(1, 1), (1, 1)], plotting.decimate([(1, 1), (1, 1)], 0))
        self.assertEqual([(1, 1), (1, 1)], plotting.decimate([(1, 1), (1, 1), (1, 1)], 0))

        actual = plotting.decimate([(1, 1), (2, 1.1), (3, 1)], 0.05)
        self.assertEqual([(1, 1), (2, 1.1), (3, 1)], actual)
        actual = plotting.decimate([(1, 1), (2, 1.1), (3, 1)], 0.15)
        self.assertEqual([(1, 1), (3, 1)], actual)

        points = [(x / 10, math.log2(x)) for x in range(1, 100)]
        actual = plotting.decimate(points, 0.3)
        expected = [
            (0.1, 0.0),
            (0.7, 2.807354922057604),
            (2.1, 4.392317422778761),
            (5.0, 5.643856189774724),
            (9.9, 6.6293566200796095),
        ]
        self.assertEqual(expected, actual)

    def test_moving_average(self):
        r = range(10)
        self.assertEqual(list(r), list(plotting.moving_average(r, n=1)))

        expected = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]
        self.assertEqual(expected, list(plotting.moving_average(r, n=2)))

        expected = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        self.assertEqual(expected, list(plotting.moving_average(r, n=5)))

        expected = [4.5]
        self.assertEqual(expected, list(plotting.moving_average(r, n=10)))

    def test_plot(self):
        pid_series = {
            309: [(0, 0), (10, 10), (15, 5)],
            2610: [(0, 0), (10, 10), (25, 10)],
        }
        with tempfile.NamedTemporaryFile() as f:
            plotting.plot(pid_series, f.name, 'Visions', style=None)
            svg_bytes = f.read()

        self.assertIn(b'<svg', svg_bytes)
        self.assertIn(b'Visions', svg_bytes)
        self.assertIn(b'309', svg_bytes)
        self.assertIn(b'2610', svg_bytes)
        self.assertGreater(len(svg_bytes), 18000)

        with tempfile.NamedTemporaryFile() as f:
            plotting.plot(pid_series, f.name, 'Visions', style='LightGreenStyle')
            svg_green_bytes = f.read()

        self.assertIn(b'<svg', svg_bytes)
        self.assertIn(b'Visions', svg_bytes)
        self.assertIn(b'309', svg_bytes)
        self.assertIn(b'2610', svg_bytes)
        self.assertGreater(len(svg_bytes), 18000)
        self.assertNotEqual(svg_bytes, svg_green_bytes)


class ChromiumTree(proctree.Forest):

    proc_map: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        node_list = get_chromium_node_list()
        proc_list = [{k: v for k, v in p.items() if k != 'children'} for p in node_list]
        self.proc_map = {proc['stat']['pid']: proc for proc in proc_list}
        self.proc_map[1] = {'stat': {'ppid': 0, 'pid': 1}}

    def _read_process_dict(self, p, pass_n, **kwargs):
        return self._dictcls({
            k: self._dictcls(v) if isinstance(v, dict) else v
            for k, v in self.proc_map[p].items()
            if k == ['stat', 'cmdline'][pass_n]
        })

    def get_pid_list(self):
        return list(self.proc_map.keys()) + [os.getpid()]


class TestProctreeForest(unittest.TestCase):

    testee = None

    def setUp(self):
        self.testee = ChromiumTree(procfile.registry)

    def test_get_pid_list(self):
        actual = proctree.Forest.get_pid_list()
        self.assertTrue(all(isinstance(v, int) for v in actual))
        self.assertEqual(actual, sorted(actual))

    def test_get_nodemap(self):
        expected = {p['stat']['pid']: p for p in get_chromium_node_list()}
        expected[1] = {'stat': {'ppid': 0, 'pid': 1}, 'children': [get_chromium_node_list()[0]]}
        actual = self.testee._get_nodemap()
        self.assertEqual(expected, actual)

    def test_get_roots(self):
        expected = [{'stat': {'ppid': 0, 'pid': 1}, 'children': [get_chromium_node_list()[0]]}]
        actual = self.testee.get_roots()
        self.assertEqual(expected, actual)

    def test_get_roots_branch_pids(self):
        node_list = get_chromium_node_list()
        pid_18482 = self.testee.proc_map[18482].copy()
        pid_18482['children'] = [node_list[4]]  # PID 18484 with children
        pid_18467 = self.testee.proc_map[18467].copy()
        pid_18467['children'] = [pid_18482, node_list[3]]  # the second item is PID 18508
        expected = [{'stat': {'ppid': 0, 'pid': 1}, 'children': [pid_18467]}]
        actual = self.testee.get_roots([18484, 18531, 18508])
        self.assertEqual(expected, actual)

    def test_get_roots_branch_pids_noop(self):
        self.assertEqual(self.testee.get_roots(), self.testee.get_roots([1, 2, 3]))

    def test_get_roots_branch_pids_non_existent(self):
        self.assertEqual([], self.testee.get_roots([666]))

    def test_get_roots_branch_pids_hidden_parent(self):
        # For instance, Termux shell knows its PPID but it's not in /proc
        self.testee.proc_map = {
            18571: self.testee.proc_map[18571],
            18503: self.testee.proc_map[18503],
            18517: self.testee.proc_map[18517],
        }
        expected = [
            self.testee.proc_map[18571],
            {
                **self.testee.proc_map[18503],
                'children': [self.testee.proc_map[18517]],
            },
        ]
        actual = self.testee.get_roots()
        self.assertEqual(expected, actual)

    def test_read_process_dict(self):
        testee = proctree.Forest(procfile.registry)
        actual = testee._read_process_dict(os.getpid(), pass_n=0)
        self.assertEqual({'stat'}, actual.keys())
        self.assertIn('rss', actual['stat'])

        actual = testee._read_process_dict(os.getpid(), pass_n=1)
        self.assertEqual({'cmdline', 'io', 'status'}, actual.keys())
        self.assertIn('rchar', actual['io'])
        self.assertIn('vmswap', actual['status'])

        testee = proctree.Forest(
            {k: v for k, v in procfile.registry.items() if k in ('stat', 'cmdline')}
        )
        actual = testee._read_process_dict(os.getpid(), pass_n=0)
        actual.update(testee._read_process_dict(os.getpid(), pass_n=1))
        self.assertEqual(['stat', 'cmdline'], list(actual.keys()))

    def test_read_process_dict_permission_error(self):
        testee = proctree.Forest(
            {k: v for k, v in procfile.registry.items() if k in ('stat', 'io')}
        )

        with self.assertLogs('procpath', 'WARNING') as ctx:
            actual = testee._read_process_dict(1, pass_n=1)
        self.assertEqual(1, len(ctx.records))
        msg = ctx.records[0].message
        self.assertTrue(msg.startswith('Storing empty values for pid 1, procfile io because of'))
        self.assertIn('Permission denied', msg)

        self.assertEqual({'io': procfile.read_io.empty}, actual)  # @UndefinedVariable

    def test_read_process_dict_file_not_found_error(self):
        testee = proctree.Forest({k: v for k, v in procfile.registry.items() if k in ('stat',)})

        with self.assertLogs('procpath', 'DEBUG') as ctx:
            actual = testee._read_process_dict(2 ** 15 + 1, pass_n=0, raise_on_missing_file=False)
        self.assertEqual(1, len(ctx.records))
        msg = ctx.records[0].message
        self.assertTrue(msg.startswith('Storing empty values for pid 32769, procfile stat'))
        self.assertIn("No such file or directory: '/proc/32769/stat'", msg)

        self.assertEqual({'stat': procfile.read_stat.empty}, actual)  # @UndefinedVariable

    def test_get_roots_do_not_skip_self(self):
        testee = proctree.Forest({'stat': procfile.registry['stat']}, skip_self=False)
        proc_map = {
            1: {'stat': {'ppid': 0}},
            os.getpid(): {'stat': {'ppid': 1}}
        }
        testee._read_process_dict = lambda p, pass_n, **kwargs: {} if pass_n else proc_map[p]
        testee.get_pid_list = lambda: list(proc_map.keys())

        expected = [{'stat': {'ppid': 0}, 'children': [{'stat': {'ppid': 1}}]}]
        self.assertEqual(expected, testee.get_roots())

    def test_required_stat(self):
        with self.assertRaises(RuntimeError) as ctx:
            proctree.Forest({'io': procfile.registry['io']})
        self.assertEqual('stat file reader is required', str(ctx.exception))


class TestProctree(unittest.TestCase):

    def test_flatten(self):
        actual = proctree.flatten(get_chromium_node_list(), ['stat'])

        # trim for brevity
        for d in actual:
            for k in list(d.keys()):
                if k not in ('stat_pid', 'stat_rss', 'stat_state'):
                    d.pop(k)

        expected = [
            {'stat_pid': 18467, 'stat_rss': 53306, 'stat_state': 'S'},
            {'stat_pid': 18482, 'stat_rss': 13765, 'stat_state': 'S'},
            {'stat_pid': 18484, 'stat_rss': 3651, 'stat_state': 'S'},
            {'stat_pid': 18529, 'stat_rss': 19849, 'stat_state': 'S'},
            {'stat_pid': 18531, 'stat_rss': 26117, 'stat_state': 'S'},
            {'stat_pid': 18555, 'stat_rss': 63235, 'stat_state': 'S'},
            {'stat_pid': 18569, 'stat_rss': 18979, 'stat_state': 'S'},
            {'stat_pid': 18571, 'stat_rss': 8825, 'stat_state': 'S'},
            {'stat_pid': 18593, 'stat_rss': 22280, 'stat_state': 'S'},
            {'stat_pid': 18757, 'stat_rss': 12882, 'stat_state': 'S'},
            {'stat_pid': 18769, 'stat_rss': 54376, 'stat_state': 'S'},
            {'stat_pid': 18770, 'stat_rss': 31106, 'stat_state': 'S'},
            {'stat_pid': 18942, 'stat_rss': 27106, 'stat_state': 'S'},
            {'stat_pid': 18503, 'stat_rss': 27219, 'stat_state': 'S'},
            {'stat_pid': 18517, 'stat_rss': 4368, 'stat_state': 'S'},
            {'stat_pid': 18508, 'stat_rss': 20059, 'stat_state': 'S'},
        ]
        self.assertEqual(expected, actual)

    def test_flatten_single_value_procfile(self):
        actual = proctree.flatten(get_chromium_node_list(), ['cmdline'])

        renderer = {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...'}
        expected = [
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote'},
            renderer, renderer, renderer, renderer,
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...'},
            renderer, renderer, renderer, renderer, renderer,
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=gpu-process ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=broker'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...'},
        ]
        self.assertEqual(expected, actual)

    def test_flatten_list_value(self):
        actual = proctree.flatten([{
            'stat': {
                'pid': 18467,
                'ppid': 1,
            },
            'status': {
                'name': 'MainThread',
                'umask': 18,
                'state': 'S',
                'tgid': 24167,
                'ngid': 0,
                'pid': 24167,
                'ppid': 3887,
                'tracerpid': 0,
                'uid': [1000, 1000, 1000, 1000],
                'gid': [1000, 1000, 1000, 1000],
                'fdsize': 256,
                'groups': [4, 24, 27, 29, 30, 46, 113, 130, 131, 132, 136, 1000],
            },
        }], ['status'])
        expected = [{
            'status_name': 'MainThread',
            'status_umask': 18,
            'status_state': 'S',
            'status_tgid': 24167,
            'status_ngid': 0,
            'status_pid': 24167,
            'status_ppid': 3887,
            'status_tracerpid': 0,
            'status_uid': '[1000,1000,1000,1000]',
            'status_gid': '[1000,1000,1000,1000]',
            'status_fdsize': 256,
            'status_groups': '[4,24,27,29,30,46,113,130,131,132,136,1000]'
        }]
        self.assertEqual(expected, actual)

    def test_attr_dict(self):
        ad = proctree.AttrDict({'a': 'b'})
        self.assertEqual('b', ad.a)

    def test_process_exists(self):
        self.assertTrue(proctree.process_exists(os.getppid()))

        p = subprocess.run('true & echo $!', stdout=subprocess.PIPE, shell=True)
        time.sleep(0.01)
        self.assertFalse(proctree.process_exists(int(p.stdout)))


class TestProcrecSqliteStorage(unittest.TestCase):

    testeee = None

    def setUp(self):
        self.testee = procrec.SqliteStorage(':memory:', ['stat', 'cmdline'], {})

    def test_create_schema_all(self):
        testee = procrec.SqliteStorage(
            ':memory:', ['stat', 'cmdline', 'io', 'status'], utility.get_meta()
        )
        testee.create_schema()

        cursor = testee._conn.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite%'
        ''')
        self.assertEqual([('record',), ('meta',)], cursor.fetchall())

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'record'
        ''')
        expected = '''
            CREATE TABLE record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        REAL NOT NULL,
                cmdline TEXT,
                io_rchar INTEGER,
                io_wchar INTEGER,
                io_syscr INTEGER,
                io_syscw INTEGER,
                io_read_bytes INTEGER,
                io_write_bytes INTEGER,
                io_cancelled_write_bytes INTEGER,
                stat_pid INTEGER,
                stat_comm TEXT,
                stat_state TEXT,
                stat_ppid INTEGER,
                stat_pgrp INTEGER,
                stat_session INTEGER,
                stat_tty_nr INTEGER,
                stat_tpgid INTEGER,
                stat_flags INTEGER,
                stat_minflt INTEGER,
                stat_cminflt INTEGER,
                stat_majflt INTEGER,
                stat_cmajflt INTEGER,
                stat_utime INTEGER,
                stat_stime INTEGER,
                stat_cutime INTEGER,
                stat_cstime INTEGER,
                stat_priority INTEGER,
                stat_nice INTEGER,
                stat_num_threads INTEGER,
                stat_itrealvalue INTEGER,
                stat_starttime INTEGER,
                stat_vsize INTEGER,
                stat_rss INTEGER,
                status_name TEXT,
                status_umask INTEGER,
                status_state TEXT,
                status_tgid INTEGER,
                status_ngid INTEGER,
                status_pid INTEGER,
                status_ppid INTEGER,
                status_tracerpid INTEGER,
                status_uid TEXT,
                status_gid TEXT,
                status_fdsize INTEGER,
                status_groups TEXT,
                status_nstgid TEXT,
                status_nspid TEXT,
                status_nspgid TEXT,
                status_nssid TEXT,
                status_vmpeak INTEGER,
                status_vmsize INTEGER,
                status_vmlck INTEGER,
                status_vmpin INTEGER,
                status_vmhwm INTEGER,
                status_vmrss INTEGER,
                status_rssanon INTEGER,
                status_rssfile INTEGER,
                status_rssshmem INTEGER,
                status_vmdata INTEGER,
                status_vmstk INTEGER,
                status_vmexe INTEGER,
                status_vmlib INTEGER,
                status_vmpte INTEGER,
                status_vmpmd INTEGER,
                status_vmswap INTEGER,
                status_hugetlbpages INTEGER,
                status_coredumping INTEGER,
                status_threads INTEGER,
                status_sigq TEXT,
                status_sigpnd INTEGER,
                status_shdpnd INTEGER,
                status_sigblk INTEGER,
                status_sigign INTEGER,
                status_sigcgt INTEGER,
                status_capinh INTEGER,
                status_capprm INTEGER,
                status_capeff INTEGER,
                status_capbnd INTEGER,
                status_capamb INTEGER,
                status_nonewprivs INTEGER,
                status_seccomp INTEGER,
                status_speculation_store_bypass TEXT,
                status_cpus_allowed INTEGER,
                status_cpus_allowed_list TEXT,
                status_mems_allowed TEXT,
                status_mems_allowed_list TEXT,
                status_voluntary_ctxt_switches INTEGER,
                status_nonvoluntary_ctxt_switches INTEGER
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'meta'
        ''')
        expected = '''
            CREATE TABLE meta (
                key   TEXT PRIMARY KEY NOT NULL,
                value TEXT NOT NULL
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

        cursor = testee._conn.execute('SELECT * FROM meta')
        actual = dict(list(cursor))
        actual['page_size'] = int(actual['page_size'])
        actual['clock_ticks'] = int(actual['clock_ticks'])
        self.assertEqual(utility.get_meta(), actual)

    def test_create_schema_one(self):
        testee = procrec.SqliteStorage(':memory:', ['cmdline'], {})
        testee.create_schema()

        cursor = testee._conn.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite%'
        ''')
        self.assertEqual([('record',), ('meta',)], cursor.fetchall())

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'record'
        ''')
        expected = '''
            CREATE TABLE record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        REAL NOT NULL,
                cmdline   TEXT
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

    def test_record(self):
        ts = 1594483603.109486
        data = proctree.flatten(get_chromium_node_list(), self.testee._procfile_list)
        with self.testee:
            self.testee.record(ts, data)

            self.testee._conn.row_factory = sqlite3.Row
            cursor = self.testee._conn.execute('SELECT * FROM record')
            expected = [dict(d, record_id=i + 1, ts=ts) for i, d in enumerate(data)]
            self.assertEqual(expected, list(map(dict, cursor)))

        with self.assertRaises(sqlite3.ProgrammingError) as ctx:
            self.testee._conn.execute('SELECT * FROM record')
        self.assertEqual('Cannot operate on a closed database.', str(ctx.exception))

    def test_record_unsigned_bigint(self):
        ts = 1594483603.109486
        data = proctree.flatten(get_chromium_node_list(), self.testee._procfile_list)

        data[0]['stat_vsize'] = 2 ** 63  # observed for status_vmlib in the wild
        with self.testee:
            self.testee.record(ts, data)

            self.testee._conn.row_factory = sqlite3.Row
            cursor = self.testee._conn.execute('SELECT * FROM record')
            expected = [dict(d, record_id=i + 1, ts=ts) for i, d in enumerate(data)]
            self.assertEqual(expected, list(map(dict, cursor)))

    def test_record_empty(self):
        ts = 1594483603.109486
        with self.testee:
            self.testee.record(ts, [])
            cursor = self.testee._conn.execute('SELECT * FROM record')
            self.assertEqual([], cursor.fetchall())


class TestProcret(unittest.TestCase):

    database_file = None

    @classmethod
    def setUpClass(cls):
        cls.database_file = tempfile.NamedTemporaryFile()
        cls.database_file.__enter__()

        storage = procrec.SqliteStorage(
            cls.database_file.name, ['stat', 'cmdline'], utility.get_meta()
        )
        data = proctree.flatten(get_chromium_node_list(), storage._procfile_list)
        with storage:
            for i, ts in enumerate(range(1567504800, 1567504800 + 7200, 60)):
                data = [
                    dict(d, stat_utime=d['stat_utime'] + i / 4) if d['stat_pid'] == 18467 else d
                    for d in data
                ]
                storage.record(ts, data)

    @classmethod
    def tearDownClass(cls):
        cls.database_file.close()

    def test_rss(self):
        rows = procret.query(self.database_file.name, procret.registry['rss'])
        self.assertEqual(1920, len(rows))
        self.assertEqual({'ts': 1567504800.0, 'pid': 18467, 'value': 208.2265625}, rows[0])

    def test_rss_filter_ts(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            after=datetime.datetime(2019, 9, 3, 10, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 11, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(976, len(rows))
        self.assertEqual({'ts': 1567506600.0, 'pid': 18467, 'value': 208.2265625}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            after=datetime.datetime(2019, 9, 3, 12, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 13, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual([], rows)

    def test_rss_filter_pid(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            pid_list=[18508, 18555, 18757],
        )
        self.assertEqual(360, len(rows))
        self.assertEqual({'pid': 18508, 'ts': 1567504800.0, 'value': 78.35546875}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['rss'],
            pid_list=[666],
        )
        self.assertEqual([], rows)

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_cpu(self):
        rows = procret.query(self.database_file.name, procret.registry['cpu'])
        self.assertEqual(1904, len(rows))
        self.assertEqual(
            [
                {'pid': 18467, 'ts': 1567504860.0, 'value': 0.004166666666666667},
                {'pid': 18467, 'ts': 1567504920.0, 'value': 0.008333333333333333},
                {'pid': 18467, 'ts': 1567504980.0, 'value': 0.0125},
                {'pid': 18467, 'ts': 1567505040.0, 'value': 0.016666666666666666},
                {'pid': 18467, 'ts': 1567505100.0, 'value': 0.020833333333333332},
                {'pid': 18467, 'ts': 1567505160.0, 'value': 0.025},
                {'pid': 18467, 'ts': 1567505220.0, 'value': 0.029166666666666667},
                {'pid': 18467, 'ts': 1567505280.0, 'value': 0.03333333333333333},
                {'pid': 18467, 'ts': 1567505340.0, 'value': 0.0375},
                {'pid': 18467, 'ts': 1567505400.0, 'value': 0.041666666666666664},
                {'pid': 18467, 'ts': 1567505460.0, 'value': 0.04583333333333333},
                {'pid': 18467, 'ts': 1567505520.0, 'value': 0.05},
                {'pid': 18467, 'ts': 1567505580.0, 'value': 0.05416666666666667},
                {'pid': 18467, 'ts': 1567505640.0, 'value': 0.058333333333333334},
                {'pid': 18467, 'ts': 1567505700.0, 'value': 0.0625},
                {'pid': 18467, 'ts': 1567505760.0, 'value': 0.06666666666666667},
                {'pid': 18467, 'ts': 1567505820.0, 'value': 0.07083333333333333},
                {'pid': 18467, 'ts': 1567505880.0, 'value': 0.075},
                {'pid': 18467, 'ts': 1567505940.0, 'value': 0.07916666666666666},
                {'pid': 18467, 'ts': 1567506000.0, 'value': 0.08333333333333333},
                {'pid': 18467, 'ts': 1567506060.0, 'value': 0.0875},
                {'pid': 18467, 'ts': 1567506120.0, 'value': 0.09166666666666666},
                {'pid': 18467, 'ts': 1567506180.0, 'value': 0.09583333333333334},
                {'pid': 18467, 'ts': 1567506240.0, 'value': 0.1},
            ],
            rows[:24],
        )

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_cpu_filter_ts(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            after=datetime.datetime(2019, 9, 3, 10, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 11, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(976, len(rows))
        self.assertEqual({'pid': 18467, 'ts': 1567506600.0, 'value': 0.125}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            after=datetime.datetime(2019, 9, 3, 12, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 13, 30, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual([], rows)

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_cpu_filter_pid(self):
        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            pid_list=[18508, 18555, 18757],
        )
        self.assertEqual({'pid': 18508, 'ts': 1567504860.0, 'value': 0.0}, rows[0])

        rows = procret.query(
            self.database_file.name,
            procret.registry['cpu'],
            pid_list=[666],
        )
        self.assertEqual([], rows)

    def test_create_query(self):
        query = procret.create_query('260 / 10', title='Custom query')
        rows = procret.query(
            self.database_file.name,
            query,
            after=datetime.datetime(2019, 9, 3, 10, 30, tzinfo=datetime.timezone.utc),
            before=datetime.datetime(2019, 9, 3, 11, 30, tzinfo=datetime.timezone.utc),
            pid_list=[18508, 18555, 18757],
        )
        self.assertEqual(183, len(rows))
        self.assertEqual({'ts': 1567506600.0, 'pid': 18508, 'value': 26}, rows[0])
        self.assertEqual({'ts': 1567510200.0, 'pid': 18757, 'value': 26}, rows[-1])


class TestCli(unittest.TestCase):

    def test_build_parser_record(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'record',
            '-f', 'stat,cmdline',
            '-e', 'N=\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'',
            '-i', '10',
            '-r', '100',
            '-v', '25',
            '-d', 'db.sqlite',
            '$..children[?(@.stat.pid == $N)]',
        ]))
        expected = {
            'command': 'record',
            'procfile_list': ['stat', 'cmdline'],
            'environment': [['N', '\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'']],
            'interval': 10.0,
            'recnum': 100,
            'reevalnum': 25,
            'pid_list': None,
            'database_file': 'db.sqlite',
            'query': '$..children[?(@.stat.pid == $N)]',
            'logging_level': 'INFO',
            'stop_without_result': False,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'record',
            '-e', 'N=\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'',
            '-p', '1,$N',
            '-d', 'db.sqlite',
            '--stop-without-result',
        ]))
        expected = {
            'command': 'record',
            'procfile_list': ['stat', 'cmdline'],
            'environment': [['N', '\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'']],
            'interval': 10.0,
            'recnum': None,
            'reevalnum': None,
            'pid_list': '1,$N',
            'database_file': 'db.sqlite',
            'query': None,
            'logging_level': 'INFO',
            'stop_without_result': True,
        }
        self.assertEqual(expected, actual)

    def test_build_parser_query(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f', 'stat',
            '-d', ',',
            '$..children[?(@.stat.pid == 666)]..pid',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': ',',
            'indent': None,
            'query': '$..children[?(@.stat.pid == 666)]..pid',
            'output_file': sys.stdout,
            'sql_query': None,
            'logging_level': 'INFO',
            'environment': None,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f', 'stat',
            '-i', '2',
            '$..children[?(@.stat.pid == 666)]..pid',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': None,
            'indent': 2,
            'query': '$..children[?(@.stat.pid == 666)]..pid',
            'output_file': sys.stdout,
            'sql_query': None,
            'logging_level': 'INFO',
            'environment': None,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            '--logging-level', 'ERROR',
            'query',
            '-f', 'stat',
            '-i', '2',
            '$..children[?(@.stat.pid == 666)]',
            'SELECT SUM(stat_rss) / 1024.0 * 4 FROM record',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': None,
            'indent': 2,
            'query': '$..children[?(@.stat.pid == 666)]',
            'output_file': sys.stdout,
            'sql_query': 'SELECT SUM(stat_rss) / 1024.0 * 4 FROM record',
            'logging_level': 'ERROR',
            'environment': None,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f', 'stat',
            '-i', '2',
            '-e', 'I=echo 123',
            '-e', 'D=date',
            '',
            'SELECT SUM(stat_rss) / 1024.0 * 4 FROM record',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': None,
            'indent': 2,
            'query': '',
            'output_file': sys.stdout,
            'sql_query': 'SELECT SUM(stat_rss) / 1024.0 * 4 FROM record',
            'logging_level': 'INFO',
            'environment': [['I', 'echo 123'], ['D', 'date']],
        }
        self.assertEqual(expected, actual)

    def test_build_parser_plot(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args(['plot', '-d', 'db.sqite']))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'plot.svg',
            'query_name_list': None,
            'after': None,
            'before': None,
            'pid_list': None,
            'epsilon': None,
            'moving_average_window': None,
            'logarithmic': False,
            'style': None,
            'formatter': None,
            'title': None,
            'custom_query_file_list': None,
            'custom_value_expr_list': None,
            'logging_level': 'INFO',
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args(['plot', '-d', 'db.sqite', '-q', 'cpu']))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'plot.svg',
            'query_name_list': ['cpu'],
            'after': None,
            'before': None,
            'pid_list': None,
            'epsilon': None,
            'moving_average_window': None,
            'logarithmic': False,
            'style': None,
            'formatter': None,
            'title': None,
            'custom_query_file_list': None,
            'custom_value_expr_list': None,
            'logging_level': 'INFO',
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            '--logging-level', 'WARNING',
            'plot',
            '-d', 'db.sqite',
            '-f', 'rss.svg',
            '--query-name', 'rss',
            '--query-name', 'cpu',
            '--log',
            '-p', '1,2,3',
            '--epsilon', '26.1089',
            '-w', '10',
            '--style', 'LightGreenStyle',
            '--formatter', 'integer',
            '--title', 'Visions',
        ]))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'rss.svg',
            'query_name_list': ['rss', 'cpu'],
            'after': None,
            'before': None,
            'pid_list': [1, 2, 3],
            'epsilon': 26.1089,
            'moving_average_window': 10,
            'logarithmic': True,
            'style': 'LightGreenStyle',
            'formatter': 'integer',
            'title': 'Visions',
            'custom_query_file_list': None,
            'custom_value_expr_list': None,
            'logging_level': 'WARNING',
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'plot',
            '-d', 'db.sqite',
            '--title', 'Custom',
            '--after', '2000-01-01T00:00:00',
            '--before', '2020-01-01T00:00:00',
            '--custom-query-file', 'query1.sql',
            '--custom-query-file', 'query2.sql',
        ]))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'plot.svg',
            'query_name_list': None,
            'after': datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'before': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'pid_list': None,
            'epsilon': None,
            'moving_average_window': None,
            'logarithmic': False,
            'style': None,
            'formatter': None,
            'title': 'Custom',
            'custom_query_file_list': ['query1.sql', 'query2.sql'],
            'custom_value_expr_list': None,
            'logging_level': 'INFO',
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'plot',
            '-d', 'db.sqite',
            '--title', 'Custom',
            '--after', '2000-01-01T00:00:00',
            '--before', '2020-01-01T00:00:00',
            '--custom-value-expr', 'stat_majflt / 1000.0',
            '--custom-value-expr', 'stat_minflt / 1000.0',
        ]))
        expected = {
            'command': 'plot',
            'database_file': 'db.sqite',
            'plot_file': 'plot.svg',
            'query_name_list': None,
            'after': datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'before': datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'pid_list': None,
            'epsilon': None,
            'moving_average_window': None,
            'logarithmic': False,
            'style': None,
            'formatter': None,
            'title': 'Custom',
            'custom_query_file_list': None,
            'custom_value_expr_list': ['stat_majflt / 1000.0', 'stat_minflt / 1000.0'],
            'logging_level': 'INFO',
        }
        self.assertEqual(expected, actual)

    def test_build_parser_watch(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args(['watch', '-c', 'echo 1', '-i', '10']))
        expected = {
            'command': 'watch',
            'environment': None,
            'query_list': None,
            'command_list': ['echo 1'],
            'interval': 10.0,
            'repeat': None,
            'procfile_list': ['stat', 'cmdline'],
            'stop_signal': 'SIGINT',
            'logging_level': 'INFO',
            'no_restart': False,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'watch',
            '-e', 'D=date +%s',
            '-c', 'echo 1',
            '-c', 'echo $D',
            '--interval', '30',
            '-r', '1',
            '-s', 'SIGTERM',
        ]))
        expected = {
            'command': 'watch',
            'environment': [['D', 'date +%s']],
            'query_list': None,
            'command_list': ['echo 1', 'echo $D'],
            'interval': 30.0,
            'repeat': 1,
            'procfile_list': ['stat', 'cmdline'],
            'stop_signal': 'SIGTERM',
            'logging_level': 'INFO',
            'no_restart': False,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            '--logging-level', 'ERROR',
            'watch',
            '--procfile-list', 'stat,status',
            '--interval', '30',
            '--environment', 'C=docker inspect -f "{{.State.Pid}}" stack_postgres_1',
            '--environment', 'S=systemctl show --property MainPID nginx.service | cut -d "=" -f 2',
            '--environment', 'D=date +%s',
            '--query', 'L1=$..children[?(@.stat.pid == $C)]..pid',
            '--query', 'L2=$..children[?(@.stat.pid == $S)]..pid',
            '--command', "pidstat -dru -hl -p $L1 10 30 >> 'record-$D.pidstat",
            '--command', 'smemstat -o smemstat-$D.json -p $L2',
            '--no-restart',
        ]))
        expected = {
            'command': 'watch',
            'environment': [
                ['C', 'docker inspect -f "{{.State.Pid}}" stack_postgres_1'],
                ['S', 'systemctl show --property MainPID nginx.service | cut -d "=" -f 2'],
                ['D', 'date +%s'],
            ],
            'query_list': [
                ['L1', '$..children[?(@.stat.pid == $C)]..pid'],
                ['L2', '$..children[?(@.stat.pid == $S)]..pid']
            ],
            'command_list': [
                "pidstat -dru -hl -p $L1 10 30 >> 'record-$D.pidstat",
                'smemstat -o smemstat-$D.json -p $L2'
            ],
            'interval': 30.0,
            'procfile_list': ['stat', 'status'],
            'repeat': None,
            'stop_signal': 'SIGINT',
            'logging_level': 'ERROR',
            'no_restart': True,
        }
        self.assertEqual(expected, actual)

    def test_build_parser_play(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args(['play', '-f', 'jigsaw.procfile', '*']))
        expected = {
            'logging_level': 'INFO',
            'command': 'play',
            'target': ['*'],
            'playbook_file': 'jigsaw.procfile',
            'list_sections': False,
            'dry_run': False,
            'option_override_list': None,
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'play', '-f', 'jigsaw.procfile', '-n', 'river:watch', 'river:plot'
        ]))
        expected = {
            'logging_level': 'INFO',
            'command': 'play',
            'target': ['river:watch', 'river:plot'],
            'playbook_file': 'jigsaw.procfile',
            'list_sections': False,
            'dry_run': True,
            'option_override_list': None,
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'play', '-f', 'jigsaw.procfile', '-l', 'river:watch', 'river:plot'
        ]))
        expected = {
            'logging_level': 'INFO',
            'command': 'play',
            'target': ['river:watch', 'river:plot'],
            'playbook_file': 'jigsaw.procfile',
            'list_sections': True,
            'dry_run': False,
            'option_override_list': None,
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            '--logging-level', 'ERROR',
            'play',
            '-f', 'jigsaw.procfile',
            '-l',
            '--option', 'epsilon=0.1',
            '--option', 'database_file=desert_island_disk.sqlite',
            '*:plot'
        ]))
        expected = {
            'logging_level': 'ERROR',
            'command': 'play',
            'target': ['*:plot'],
            'playbook_file': 'jigsaw.procfile',
            'list_sections': True,
            'dry_run': False,
            'option_override_list': [
                ['epsilon', '0.1'],
                ['database_file', 'desert_island_disk.sqlite'],
            ],
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

    def test_build_parser_explore(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args(['explore']))
        expected = {
            'logging_level': 'INFO',
            'command': 'explore',
            'reinstall': False,
            'build_url': 'https://github.com/lana-k/sqliteviz/releases/latest/download/dist.zip',
            'bind': '',
            'port': 8000,
            'open_in_browser': True
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args(['explore', '-p', '8080', '--bind', '127.0.0.1']))
        expected = {
            'logging_level': 'INFO',
            'command': 'explore',
            'reinstall': False,
            'build_url': 'https://github.com/lana-k/sqliteviz/releases/latest/download/dist.zip',
            'bind': '127.0.0.1',
            'port': 8080,
            'open_in_browser': True
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            '--logging-level', 'ERROR',
            'explore',
            '--reinstall',
            '--build-url', 'https://github.com/lana-k/sqliteviz/releases/download/0.6.0/dist.zip'
        ]))
        expected = {
            'logging_level': 'ERROR',
            'command': 'explore',
            'reinstall': True,
            'build_url': 'https://github.com/lana-k/sqliteviz/releases/download/0.6.0/dist.zip',
            'bind': '',
            'port': 8000,
            'open_in_browser': True
        }
        self.assertEqual(expected, actual)

    def test_cli(self):
        subprocess.check_output(
            [sys.executable, '-m', 'procpath', 'query', '$..children[?(@.stat.pid == -1)]..pid'],
            env=os.environ,
        )

    def test_cli_help(self):
        subprocess.check_output(
            [sys.executable, '-m', 'procpath', 'plot', '--help'],
            env=os.environ,
        )

    def test_cli_missing_command(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            subprocess.check_output(
                [sys.executable, '-m', 'procpath'], stderr=subprocess.PIPE, env=os.environ
            )
        self.assertTrue(
            ctx.exception.stderr.endswith(
                b'error: the following arguments are required: command\n'
            )
        )

    def test_cli_command_error(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            subprocess.check_output(
                [sys.executable, '-m', 'procpath', 'query', '!@#$'],
                stderr=subprocess.PIPE,
                env=os.environ,
            )
        self.assertEqual(1, ctx.exception.returncode)
        self.assertIn(b'JSONPath syntax error', ctx.exception.stderr)

    def test_cli_logging_level(self):
        output = subprocess.check_output(
            [
                sys.executable, '-m', 'procpath', 'watch',
                '-i', '0.1',
                '-r', '1',
                '-c', 'echo Carousel',
                '-c', 'sleep 0.05 && echo "A Glutton for Punishment" 1>&2',
            ],
            stderr=subprocess.STDOUT,
            env=os.environ,
            encoding='utf-8',
        )
        lines = output.splitlines()
        self.assertEqual(2, len(lines))
        self.assertIn('INFO    procpath №1: Carousel', lines[0])
        self.assertIn('WARNING procpath №2: A Glutton for Punishment', lines[1])

        output = subprocess.check_output(
            [
                sys.executable, '-m', 'procpath', '--logging-level', 'WARNING', 'watch',
                '-i', '0',
                '-r', '1',
                '-c', 'echo Carousel',
                '-c', 'echo "A Glutton for Punishment" 1>&2',
            ],
            stderr=subprocess.STDOUT,
            env=os.environ,
            encoding='utf-8',
        )
        lines = output.splitlines()
        self.assertEqual(1, len(lines))
        self.assertIn('WARNING procpath №2: A Glutton for Punishment', lines[0])

    def test_cli_clean_sigint_stop(self):
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        self.addCleanup(loop.close)

        async def test():
            with tempfile.NamedTemporaryFile() as f:
                process = await asyncio.create_subprocess_exec(
                    *[sys.executable, '-m', 'procpath', 'record', '-p', '1', '-d', f.name],
                    env=os.environ,
                )
                process.send_signal(signal.SIGINT)
                stdout_data, stderr_data = await process.communicate()

            self.assertIsNotNone(process.returncode)
            self.assertNotEqual(0, process.returncode)
            self.assertIsNone(stdout_data)
            self.assertIsNone(stderr_data)

        loop.run_until_complete(test())


class TestProcfile(unittest.TestCase):

    maxDiff = None

    def test_read_stat(self):
        content = (
            b'32222 (python3.7) R 29884 337 337 0 -1 4194304 3765 0 1 0 19 3 0 '
            b'0 20 0 2 0 89851404 150605824 5255 18446744073709551615 4194304 '
            b'8590100 140727866261328 0 0 0 4 553652224 2 0 0 0 17 2 0 0 1 0 0 '
            b'10689968 11363916 15265792 140727866270452 140727866270792 '
            b'140727866270792 140727866273727 0\n'
        )
        expected = {
            'pid': 32222,
            'comm': 'python3.7',
            'state': 'R',
            'ppid': 29884,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194304,
            'minflt': 3765,
            'cminflt': 0,
            'majflt': 1,
            'cmajflt': 0,
            'utime': 19,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 2,
            'itrealvalue': 0,
            'starttime': 89851404,
            'vsize': 150605824,
            'rss': 5255
        }
        actual = procfile.read_stat(content)
        self.assertEqual(expected, actual)

    def test_read_cmdline(self):
        content = b'python3.7\x00-Wa\x00-u\x00'
        expected = 'python3.7 -Wa -u'
        actual = procfile.read_cmdline(content)
        self.assertEqual(expected, actual)

    def test_read_io(self):
        content = (
            b'rchar: 2274068\nwchar: 15681\nsyscr: 377\nsyscw: 10\nread_bytes: '
            b'0\nwrite_bytes: 20480\ncancelled_write_bytes: 0\n'
        )
        expected = {
            'rchar': 2274068,
            'wchar': 15681,
            'syscr': 377,
            'syscw': 10,
            'read_bytes': 0,
            'write_bytes': 20480,
            'cancelled_write_bytes': 0
        }
        actual = procfile.read_io(content)
        self.assertEqual(expected, actual)

    def test_read_status_4_13(self):
        content = (
            b'Name:\tMainThread\n'
            b'Umask:\t0022\n'
            b'State:\tS (sleeping)\n'
            b'Tgid:\t24167\n'
            b'Ngid:\t0\n'
            b'Pid:\t24167\n'
            b'PPid:\t3887\n'
            b'TracerPid:\t0\n'
            b'Uid:\t1000    1000    1000    1000\n'
            b'Gid:\t1000    1000    1000    1000\n'
            b'FDSize:\t256\n'
            b'Groups:\t4 24 27 29 30 46 113 130 131 132 136 1000\n'
            b'NStgid:\t24167\n'
            b'NSpid:\t24167\n'
            b'NSpgid:\t2287\n'
            b'NSsid:\t2287\n'
            b'VmPeak:\t  19488708 kB\n'
            b'VmSize:\t  3523068 kB\n'
            b'VmLck:\t         0 kB\n'
            b'VmPin:\t         0 kB\n'
            b'VmHWM:\t    608460 kB\n'
            b'VmRSS:\t    520744 kB\n'
            b'RssAnon:\t          370924 kB\n'
            b'RssFile:\t           73148 kB\n'
            b'RssShmem:\t          76672 kB\n'
            b'VmData:\t   578248 kB\n'
            b'VmStk:\t       132 kB\n'
            b'VmExe:\t      1972 kB\n'
            b'VmLib:\t    232128 kB\n'
            b'VmPTE:\t      2604 kB\n'
            b'VmPMD:\t       280 kB\n'
            b'VmSwap:\t        0 kB\n'
            b'HugetlbPages:\t          0 kB\n'
            b'Threads:\t57\n'
            b'SigQ:\t1/31038\n'
            b'SigPnd:\t0000000000000000\n'
            b'ShdPnd:\t0000000000000000\n'
            b'SigBlk:\t0000000000000000\n'
            b'SigIgn:\t0000000021001000\n'
            b'SigCgt:\t0000000f800044ff\n'
            b'CapInh:\t0000000000000000\n'
            b'CapPrm:\t0000000000000000\n'
            b'CapEff:\t0000000000000000\n'
            b'CapBnd:\t0000003fffffffff\n'
            b'CapAmb:\t0000000000000000\n'
            b'NoNewPrivs:\t0\n'
            b'Seccomp:\t0\n'
            b'Speculation_Store_Bypass:\tthread vulnerable\n'
            b'Cpus_allowed:\tff\n'
            b'Cpus_allowed_list:\t0-7\n'
            b'Mems_allowed:\t00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000001\n'
            b'Mems_allowed_list:\t0\n'
            b'voluntary_ctxt_switches:\t1443497\n'
            b'nonvoluntary_ctxt_switches:\t724507\n'
        )
        expected = {
            'name': 'MainThread',
            'umask': 18,
            'state': 'S',
            'tgid': 24167,
            'ngid': 0,
            'pid': 24167,
            'ppid': 3887,
            'tracerpid': 0,
            'uid': [1000, 1000, 1000, 1000],
            'gid': [1000, 1000, 1000, 1000],
            'fdsize': 256,
            'groups': [4, 24, 27, 29, 30, 46, 113, 130, 131, 132, 136, 1000],
            'nstgid': [24167],
            'nspid': [24167],
            'nspgid': [2287],
            'nssid': [2287],
            'vmpeak': 19488708,
            'vmsize': 3523068,
            'vmlck': 0,
            'vmpin': 0,
            'vmhwm': 608460,
            'vmrss': 520744,
            'rssanon': 370924,
            'rssfile': 73148,
            'rssshmem': 76672,
            'vmdata': 578248,
            'vmstk': 132,
            'vmexe': 1972,
            'vmlib': 232128,
            'vmpte': 2604,
            'vmpmd': 280,
            'vmswap': 0,
            'hugetlbpages': 0,
            'coredumping': None,
            'threads': 57,
            'sigq': [1, 31038],
            'sigpnd': 0,
            'shdpnd': 0,
            'sigblk': 0,
            'sigign': 553652224,
            'sigcgt': 66572010751,
            'capinh': 0,
            'capprm': 0,
            'capeff': 0,
            'capbnd': 274877906943,
            'capamb': 0,
            'nonewprivs': 0,
            'seccomp': 0,
            'speculation_store_bypass': 'thread vulnerable',
            'cpus_allowed': 255,
            'cpus_allowed_list': '0-7',
            'mems_allowed': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            ],
            'mems_allowed_list': '0',
            'voluntary_ctxt_switches': 1443497,
            'nonvoluntary_ctxt_switches': 724507
        }
        actual = procfile.read_status(content)
        self.assertEqual(expected, actual)

    def test_read_status_3_16(self):
        content = (
            b'Name:\tpython3.7\n'
            b'State:\tS (sleeping)\n'
            b'Tgid:\t28463\n'
            b'Ngid:\t0\n'
            b'Pid:\t28463\n'
            b'PPid:\t28445\n'
            b'TracerPid:\t0\n'
            b'Uid:\t689824  689824  689824  689824\n'
            b'Gid:\t689824  689824  689824  689824\n'
            b'FDSize:\t64\n'
            b'Groups:\t689824 689825 689826 689827 689828 689830 '
            b'689834 689835 689844 689850 689851\n'
            b'VmPeak:\t    42152 kB\n'
            b'VmSize:\t    42152 kB\n'
            b'VmLck:\t         0 kB\n'
            b'VmPin:\t         0 kB\n'
            b'VmHWM:\t     29940 kB\n'
            b'VmRSS:\t     19220 kB\n'
            b'VmData:\t    31784 kB\n'
            b'VmStk:\t       132 kB\n'
            b'VmExe:\t         8 kB\n'
            b'VmLib:\t      4912 kB\n'
            b'VmPTE:\t       100 kB\n'
            b'VmSwap:\t    10772 kB\n'
            b'Threads:\t7\n'
            b'SigQ:\t0/7968\n'
            b'SigPnd:\t0000000000000000\n'
            b'ShdPnd:\t0000000000000000\n'
            b'SigBlk:\t0000000000000000\n'
            b'SigIgn:\t0000000001001000\n'
            b'SigCgt:\t0000000000000002\n'
            b'CapInh:\t00000000a80425fb\n'
            b'CapPrm:\t00000000a80425fb\n'
            b'CapEff:\t00000000a80425fb\n'
            b'CapBnd:\t00000000a80425fb\n'
            b'Seccomp:\t0\n'
            b'Cpus_allowed:\t1\n'
            b'Cpus_allowed_list:\t0\n'
            b'Mems_allowed:\t00000000,00000001\n'
            b'Mems_allowed_list:\t0\n'
            b'voluntary_ctxt_switches:\t288015\n'
            b'nonvoluntary_ctxt_switches:\t60055\n'
        )
        expected = {
            'name': 'python3.7',
            'umask': None,
            'state': 'S',
            'tgid': 28463,
            'ngid': 0,
            'pid': 28463,
            'ppid': 28445,
            'tracerpid': 0,
            'uid': [689824, 689824, 689824, 689824],
            'gid': [689824, 689824, 689824, 689824],
            'fdsize': 64,
            'groups': [
                689824, 689825, 689826, 689827, 689828, 689830, 689834,
                689835, 689844, 689850, 689851,
            ],
            'nstgid': None,
            'nspid': None,
            'nspgid': None,
            'nssid': None,
            'vmpeak': 42152,
            'vmsize': 42152,
            'vmlck': 0,
            'vmpin': 0,
            'vmhwm': 29940,
            'vmrss': 19220,
            'rssanon': None,
            'rssfile': None,
            'rssshmem': None,
            'vmdata': 31784,
            'vmstk': 132,
            'vmexe': 8,
            'vmlib': 4912,
            'vmpte': 100,
            'vmpmd': None,
            'vmswap': 10772,
            'hugetlbpages': None,
            'coredumping': None,
            'threads': 7,
            'sigq': [0, 7968],
            'sigpnd': 0,
            'shdpnd': 0,
            'sigblk': 0,
            'sigign': 16781312,
            'sigcgt': 2,
            'capinh': 2818844155,
            'capprm': 2818844155,
            'capeff': 2818844155,
            'capbnd': 2818844155,
            'capamb': None,
            'nonewprivs': None,
            'seccomp': 0,
            'speculation_store_bypass': None,
            'cpus_allowed': 1,
            'cpus_allowed_list': '0',
            'mems_allowed': [0, 1],
            'mems_allowed_list': '0',
            'voluntary_ctxt_switches': 288015,
            'nonvoluntary_ctxt_switches': 60055
        }
        actual = procfile.read_status(content)
        self.assertEqual(expected, actual)

    def test_read_status_3_2(self):
        content = (
            b'Name:\tnginx\n'
            b'State:\tS (sleeping)\n'
            b'Tgid:\t2913\n'
            b'Pid:\t2913\n'
            b'PPid:\t1\n'
            b'TracerPid:\t0\n'
            b'Uid:\t0       0       0       0\n'
            b'Gid:\t0       0       0       0\n'
            b'FDSize:\t32\n'
            b'Groups:\t\n'
            b'VmPeak:\t    10448 kB\n'
            b'VmSize:\t    10448 kB\n'
            b'VmLck:\t         0 kB\n'
            b'VmPin:\t         0 kB\n'
            b'VmHWM:\t      1212 kB\n'
            b'VmRSS:\t       680 kB\n'
            b'VmData:\t      748 kB\n'
            b'VmStk:\t       136 kB\n'
            b'VmExe:\t       740 kB\n'
            b'VmLib:\t      8164 kB\n'
            b'VmPTE:\t        32 kB\n'
            b'VmSwap:\t      488 kB\n'
            b'Threads:\t1\n'
            b'SigQ:\t0/3939\n'
            b'SigPnd:\t0000000000000000\n'
            b'ShdPnd:\t0000000000000000\n'
            b'SigBlk:\t0000000000000000\n'
            b'SigIgn:\t0000000040001000\n'
            b'SigCgt:\t0000000198016a07\n'
            b'CapInh:\t0000000000000000\n'
            b'CapPrm:\tffffffffffffffff\n'
            b'CapEff:\tffffffffffffffff\n'
            b'CapBnd:\tffffffffffffffff\n'
            b'Cpus_allowed:\t1\n'
            b'Cpus_allowed_list:\t0\n'
            b'Mems_allowed:\t1\n'
            b'Mems_allowed_list:\t0\n'
            b'voluntary_ctxt_switches:\t767\n'
            b'nonvoluntary_ctxt_switches:\t3\n'
        )
        expected = {
            'name': 'nginx',
            'umask': None,
            'state': 'S',
            'tgid': 2913,
            'ngid': None,
            'pid': 2913,
            'ppid': 1,
            'tracerpid': 0,
            'uid': [0, 0, 0, 0],
            'gid': [0, 0, 0, 0],
            'fdsize': 32,
            'groups': [],
            'nstgid': None,
            'nspid': None,
            'nspgid': None,
            'nssid': None,
            'vmpeak': 10448,
            'vmsize': 10448,
            'vmlck': 0,
            'vmpin': 0,
            'vmhwm': 1212,
            'vmrss': 680,
            'rssanon': None,
            'rssfile': None,
            'rssshmem': None,
            'vmdata': 748,
            'vmstk': 136,
            'vmexe': 740,
            'vmlib': 8164,
            'vmpte': 32,
            'vmpmd': None,
            'vmswap': 488,
            'hugetlbpages': None,
            'coredumping': None,
            'threads': 1,
            'sigq': [0, 3939],
            'sigpnd': 0,
            'shdpnd': 0,
            'sigblk': 0,
            'sigign': 1073745920,
            'sigcgt': 6845196807,
            'capinh': 0,
            'capprm': 18446744073709551615,
            'capeff': 18446744073709551615,
            'capbnd': 18446744073709551615,
            'capamb': None,
            'nonewprivs': None,
            'seccomp': None,
            'speculation_store_bypass': None,
            'cpus_allowed': 1,
            'cpus_allowed_list': '0',
            'mems_allowed': [1],
            'mems_allowed_list': '0',
            'voluntary_ctxt_switches': 767,
            'nonvoluntary_ctxt_switches': 3
        }
        actual = procfile.read_status(content)
        self.assertEqual(expected, actual)

        content += b'Foo: Bar\n'
        actual = procfile.read_status(content)
        self.assertEqual(expected, actual)

    def test_read_status_kthread(self):
        content = (
            b'Name:\tkthreadd\n'
            b'Umask:\t0000\n'
            b'State:\tS (sleeping)\n'
            b'Tgid:\t2\n'
            b'Ngid:\t0\n'
            b'Pid:\t2\n'
            b'PPid:\t0\n'
            b'TracerPid:\t0\n'
            b'Uid:\t0    0    0    0\n'
            b'Gid:\t0    0    0    0\n'
            b'FDSize:\t64\n'
            b'Groups:\t\n'
            b'NStgid:\t2\n'
            b'NSpid:\t2\n'
            b'NSpgid:\t0\n'
            b'NSsid:\t0\n'
            b'Threads:\t1\n'
            b'SigQ:\t0/31038\n'
            b'SigPnd:\t0000000000000000\n'
            b'ShdPnd:\t0000000000000000\n'
            b'SigBlk:\t0000000000000000\n'
            b'SigIgn:\tffffffffffffffff\n'
            b'SigCgt:\t0000000000000000\n'
            b'CapInh:\t0000000000000000\n'
            b'CapPrm:\t0000003fffffffff\n'
            b'CapEff:\t0000003fffffffff\n'
            b'CapBnd:\t0000003fffffffff\n'
            b'CapAmb:\t0000000000000000\n'
            b'NoNewPrivs:\t0\n'
            b'Seccomp:\t0\n'
            b'Speculation_Store_Bypass:\tthread vulnerable\n'
            b'Cpus_allowed:\tff\n'
            b'Cpus_allowed_list:\t0-7\n'
            b'Mems_allowed:\t00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000001\n'
            b'Mems_allowed_list:\t0\n'
            b'voluntary_ctxt_switches:\t3649\n'
            b'nonvoluntary_ctxt_switches:\t203\n'
        )
        expected = {
            'name': 'kthreadd',
            'umask': 0,
            'state': 'S',
            'tgid': 2,
            'ngid': 0,
            'pid': 2,
            'ppid': 0,
            'tracerpid': 0,
            'uid': [0, 0, 0, 0],
            'gid': [0, 0, 0, 0],
            'fdsize': 64,
            'groups': [],
            'nstgid': [2],
            'nspid': [2],
            'nspgid': [0],
            'nssid': [0],
            'vmpeak': None,
            'vmsize': None,
            'vmlck': None,
            'vmpin': None,
            'vmhwm': None,
            'vmrss': None,
            'rssanon': None,
            'rssfile': None,
            'rssshmem': None,
            'vmdata': None,
            'vmstk': None,
            'vmexe': None,
            'vmlib': None,
            'vmpte': None,
            'vmpmd': None,
            'vmswap': None,
            'hugetlbpages': None,
            'coredumping': None,
            'threads': 1,
            'sigq': [0, 31038],
            'sigpnd': 0,
            'shdpnd': 0,
            'sigblk': 0,
            'sigign': 18446744073709551615,
            'sigcgt': 0,
            'capinh': 0,
            'capprm': 274877906943,
            'capeff': 274877906943,
            'capbnd': 274877906943,
            'capamb': 0,
            'nonewprivs': 0,
            'seccomp': 0,
            'speculation_store_bypass': 'thread vulnerable',
            'cpus_allowed': 255,
            'cpus_allowed_list': '0-7',
            'mems_allowed': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            ],
            'mems_allowed_list': '0',
            'voluntary_ctxt_switches': 3649,
            'nonvoluntary_ctxt_switches': 203
        }
        actual = procfile.read_status(content)
        self.assertEqual(expected, actual)

    def test_read_status_multiple_ns(self):
        content = (
            b'Name:\tpython\n'
            b'Umask:\t0022\n'
            b'State:\tS (sleeping)\n'
            b'Tgid:\t15648\n'
            b'Ngid:\t0\n'
            b'Pid:\t15648\n'
            b'PPid:\t15625\n'
            b'TracerPid:\t0\n'
            b'Uid:\t0\t0\t0\t0\n'
            b'Gid:\t0\t0\t0\t0\n'
            b'FDSize:\t64\n'
            b'Groups:\t0 1 2 3 4 6 10 11 20 26 27\n'
            b'NStgid:\t15648\t1\n'
            b'NSpid:\t15648\t1\n'
            b'NSpgid:\t15648\t1\n'
            b'NSsid:\t15648\t1\n'
            b'VmPeak:\t   24240 kB\n'
            b'VmSize:\t   24240 kB\n'
            b'VmLck:\t       0 kB\n'
            b'VmPin:\t       0 kB\n'
            b'VmHWM:\t   21876 kB\n'
            b'VmRSS:\t   21876 kB\n'
            b'RssAnon:\t   16676 kB\n'
            b'RssFile:\t    5200 kB\n'
            b'RssShmem:\t       0 kB\n'
            b'VmData:\t   16824 kB\n'
            b'VmStk:\t     132 kB\n'
            b'VmExe:\t       8 kB\n'
            b'VmLib:\t    3504 kB\n'
            b'VmPTE:\t      60 kB\n'
            b'VmPMD:\t      12 kB\n'
            b'VmSwap:\t       0 kB\n'
            b'HugetlbPages:\t       0 kB\n'
            b'Threads:\t1\n'
            b'SigQ:\t0/31038\n'
            b'SigPnd:\t0000000000000000\n'
            b'ShdPnd:\t0000000000000000\n'
            b'SigBlk:\t0000000000000000\n'
            b'SigIgn:\t0000000001001000\n'
            b'SigCgt:\t0000000000004002\n'
            b'CapInh:\t00000000a80425fb\n'
            b'CapPrm:\t00000000a80425fb\n'
            b'CapEff:\t00000000a80425fb\n'
            b'CapBnd:\t00000000a80425fb\n'
            b'CapAmb:\t0000000000000000\n'
            b'NoNewPrivs:\t0\n'
            b'Seccomp:\t2\n'
            b'Speculation_Store_Bypass:\tthread force mitigated\n'
            b'Cpus_allowed:\t0f\n'
            b'Cpus_allowed_list:\t0-3\n'
            b'Mems_allowed:\t00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,'
            b'00000000,00000000,00000000,00000000,00000000,00000000,00000001\n'
            b'Mems_allowed_list:\t0\n'
            b'voluntary_ctxt_switches:\t1194\n'
            b'nonvoluntary_ctxt_switches:\t440\n'
        )
        expected = {
            'name': 'python',
            'umask': 18,
            'state': 'S',
            'tgid': 15648,
            'ngid': 0,
            'pid': 15648,
            'ppid': 15625,
            'tracerpid': 0,
            'uid': [0, 0, 0, 0],
            'gid': [0, 0, 0, 0],
            'fdsize': 64,
            'groups': [0, 1, 2, 3, 4, 6, 10, 11, 20, 26, 27],
            'nstgid': [15648, 1],
            'nspid': [15648, 1],
            'nspgid': [15648, 1],
            'nssid': [15648, 1],
            'vmpeak': 24240,
            'vmsize': 24240,
            'vmlck': 0,
            'vmpin': 0,
            'vmhwm': 21876,
            'vmrss': 21876,
            'rssanon': 16676,
            'rssfile': 5200,
            'rssshmem': 0,
            'vmdata': 16824,
            'vmstk': 132,
            'vmexe': 8,
            'vmlib': 3504,
            'vmpte': 60,
            'vmpmd': 12,
            'vmswap': 0,
            'hugetlbpages': 0,
            'coredumping': None,
            'threads': 1,
            'sigq': [0, 31038],
            'sigpnd': 0,
            'shdpnd': 0,
            'sigblk': 0,
            'sigign': 16781312,
            'sigcgt': 16386,
            'capinh': 2818844155,
            'capprm': 2818844155,
            'capeff': 2818844155,
            'capbnd': 2818844155,
            'capamb': 0,
            'nonewprivs': 0,
            'seccomp': 2,
            'speculation_store_bypass': 'thread force mitigated',
            'cpus_allowed': 15,
            'cpus_allowed_list': '0-3',
            'mems_allowed': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            ],
            'mems_allowed_list': '0',
            'voluntary_ctxt_switches': 1194,
            'nonvoluntary_ctxt_switches': 440
        }
        actual = procfile.read_status(content)
        self.assertEqual(expected, actual)


class TestSectionProxyChain(unittest.TestCase):

    parser = None

    def setUp(self):
        cfg = '''
            [a]
            x: 1
            y: foo

            [a:b]
            extends: a
            y: bar
            z: True

            [a:b:c]
            extends: a:b
            z: False

            [b]
            x: 2

            [b:c]
            extends: b
            x: 3
            y: 5
        '''
        self.parser = configparser.RawConfigParser(
            default_section=None,
            comment_prefixes=('#',),
            delimiters=(':',),
            converters={'lines': playbook.split_multiline},
        )
        self.parser.read_string(cfg)

    def test_converter(self):
        testee = playbook.SectionProxyChain.fromsection(self.parser['a'])
        self.assertEqual([None, 1], testee.getint('x'))
        self.assertEqual([None, None], testee.getint('z'))
        self.assertEqual([None, True], testee.getboolean('x'))
        self.assertEqual([None, None], testee.getboolean('z'))

        testee = playbook.SectionProxyChain.fromsection(
            self.parser['a'], overrides={'x': '0', 'z': '1'}
        )
        self.assertEqual([0, 1], testee.getint('x'))
        self.assertEqual([1, None], testee.getint('z'))
        self.assertEqual([False, True], testee.getboolean('x'))
        self.assertEqual([True, None], testee.getboolean('z'))

        testee = playbook.SectionProxyChain.fromsection(self.parser['a:b'])
        self.assertEqual([None, None, 1], testee.getint('x'))
        self.assertEqual([None, None, None], testee.getint('zz'))
        self.assertEqual([None, None, True], testee.getboolean('x'))
        self.assertEqual([None, True, None], testee.getboolean('z'))

        testee = playbook.SectionProxyChain.fromsection(self.parser['a:b:c'])
        self.assertEqual([None, None, None, 1], testee.getint('x'))
        self.assertEqual([None, None, None, None], testee.getint('zz'))
        self.assertEqual([None, None, None, True], testee.getboolean('x'))
        self.assertEqual([None, False, True, None], testee.getboolean('z'))

        testee = playbook.SectionProxyChain.fromsection(self.parser['b:c'])
        self.assertEqual([None, 3, 2], testee.getint('x'))
        self.assertEqual([None, 5, None], testee.getint('y'))
        self.assertEqual([None, None, None], testee.getint('z'))

    def test_get(self):
        testee = playbook.SectionProxyChain.fromsection(self.parser['a'])
        self.assertEqual(None, testee.get('z'))
        self.assertEqual('bar', testee.get('z', 'bar'))
        self.assertEqual('1', testee.get('x'))
        self.assertEqual('foo', testee.get('y'))

        testee = playbook.SectionProxyChain.fromsection(self.parser['a:b'])
        self.assertEqual('True', testee.get('z'))
        self.assertEqual('1', testee.get('x'))
        self.assertEqual('bar', testee.get('y'))

        testee = playbook.SectionProxyChain.fromsection(self.parser['a:b:c'])
        self.assertEqual('False', testee.get('z'))
        self.assertEqual('1', testee.get('x'))
        self.assertEqual('bar', testee.get('y'))

        testee = playbook.SectionProxyChain.fromsection(
            self.parser['a:b:c'], overrides={'x': '15'}
        )
        self.assertEqual('False', testee.get('z'))
        self.assertEqual('15', testee.get('x'))
        self.assertEqual('bar', testee.get('y'))

        testee = playbook.SectionProxyChain.fromsection(self.parser['b:c'])
        self.assertEqual(None, testee.get('z'))
        self.assertEqual('3', testee.get('x'))
        self.assertEqual('5', testee.get('y'))

    def test_items(self):
        testee = playbook.SectionProxyChain.fromsection(self.parser['a'])
        self.assertEqual([('x', '1'), ('y', 'foo')], list(testee.items()))

        testee = playbook.SectionProxyChain.fromsection(self.parser['a:b'])
        self.assertEqual([('y', 'bar'), ('z', 'True'), ('x', '1')], list(testee.items()))

        testee = playbook.SectionProxyChain.fromsection(self.parser['a:b:c'])
        self.assertEqual([('z', 'False'), ('y', 'bar'), ('x', '1')], list(testee.items()))

        testee = playbook.SectionProxyChain.fromsection(
            self.parser['a:b:c'], overrides={'x': '15'}
        )
        self.assertEqual([('x', '15'), ('z', 'False'), ('y', 'bar')], list(testee.items()))

        testee = playbook.SectionProxyChain.fromsection(self.parser['b:c'])
        self.assertEqual([('x', '3'), ('y', '5')], list(testee.items()))

    def test_mro(self):
        # See "ex_9" in https://www.python.org/download/releases/2.3/mro/
        cfg = '''
            [a]
            v: a
            [b]
            v: b
            [c]
            v: c
            [d]
            v: d
            [e]
            v: e
            [k1]
            extends:
              a
              b
              c
            v: k1
            [k2]
            extends:
              d
              b
              e
            v: k2
            [k3]
            extends:
              d
              a
            v: k3
            [z]
            extends:
              k1
              k2
              k3
            v: z
        '''

        [self.parser.remove_section(s) for s in list(self.parser)]
        self.parser.read_string(cfg)

        testee = playbook.SectionProxyChain.fromsection(self.parser['z'])
        self.assertEqual(
            [None, ['z'], ['k1'], ['k2'], ['k3'], ['d'], ['a'], ['b'], ['c'], ['e']],
            testee.getlines('v'),
        )


class TestQueryCommand(unittest.TestCase):

    def test_query_query_node_list_json_output(self):
        output_file = io.StringIO()
        query.run(
            procfile_list=['stat'],
            output_file=output_file,
            indent=2,
            query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))

    def test_query_no_query_root_output(self):
        output_file = io.StringIO()
        query.run(
            procfile_list=['stat'],
            output_file=output_file,
        )
        roots = json.loads(output_file.getvalue())
        self.assertEqual(1, roots[0]['stat']['pid'])

    def test_query_delimited(self):
        output_file = io.StringIO()
        query.run(
            procfile_list=['stat'],
            output_file=output_file,
            delimiter=',',
            query='$..children[?(@.stat.pid == {})]..pid'.format(os.getppid()),
        )
        pids = output_file.getvalue().split(',')
        self.assertGreaterEqual(len(pids), 1)
        self.assertEqual(os.getppid(), int(pids[0]))

    def test_query_jsonpath_syntax_error(self):
        with self.assertRaises(CommandError):
            query.run(procfile_list=['stat'], output_file=io.StringIO(), query='$!#')

    def test_query_with_sql(self):
        output_file = io.StringIO()
        query.run(
            procfile_list=['stat', 'cmdline'],
            output_file=output_file,
            indent=2,
            query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            sql_query='SELECT SUM(stat_rss) / 1024.0 * 4 total FROM record',
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))
        self.assertEqual(1, len(data[0]))
        self.assertIn('total', data[0])

    def test_query_only_sql(self):
        output_file = io.StringIO()
        query.run(
            procfile_list=['stat', 'cmdline'],
            output_file=output_file,
            indent=2,
            query='',
            sql_query='SELECT SUM(stat_rss) / 1024.0 * 4 total FROM record',
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))
        self.assertEqual(1, len(data[0]))
        self.assertIn('total', data[0])

    def test_query_sql_syntax_error(self):
        with self.assertRaises(CommandError):
            query.run(procfile_list=['stat'], output_file=io.StringIO(), sql_query='$!#')

    def test_query_with_envrionment(self):
        output_file = io.StringIO()
        query.run(
            procfile_list=['stat'],
            output_file=output_file,
            indent=2,
            environment=[['P', 'echo {}'.format(os.getppid())]],
            query='$..children[?(@.stat.pid == $P)]',
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))

        output_file = io.StringIO()
        query.run(
            procfile_list=['stat'],
            output_file=output_file,
            indent=2,
            environment=[['P', 'echo {}'.format(os.getppid())]],
            sql_query='SELECT * FROM record WHERE stat_pid = $P',
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))


class TestRecordCommand(unittest.TestCase):

    def test_record_query(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            record.run(
                procfile_list=['stat'],
                database_file=f.name,
                interval=1,
                recnum=1,
                query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            )
            with contextlib.closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        actual = rows[0]
        self.assertEqual(1, actual.pop('record_id'))
        self.assertAlmostEqual(start, actual.pop('ts'), delta=0.1)

        self.assertEqual(os.getppid(), actual['stat_pid'])
        self.assertEqual(
            list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in actual.keys()],
        )

    def test_record_all(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            record.run(
                procfile_list=['stat', 'cmdline'],
                database_file=f.name,
                interval=1,
                recnum=1,
            )
            with contextlib.closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        root = rows[0]
        self.assertEqual(1, root.pop('record_id'))
        self.assertAlmostEqual(start, root.pop('ts'), delta=0.2)

        self.assertEqual(1, root['stat_pid'])
        self.assertEqual(
            ['cmdline'] + list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in root.keys()],
        )

    @classmethod
    def record_forever(cls, database_file, pid):
        try:
            record.run(
                procfile_list=['stat'],
                database_file=database_file,
                interval=0.1,
                query=f'$..children[?(@.stat.pid == {pid})]',
            )
        except KeyboardInterrupt:
            pass

    def test_record_forever(self):
        with tempfile.NamedTemporaryFile() as f:
            p = multiprocessing.Process(target=self.record_forever, args=(f.name, os.getppid()))
            self.addCleanup(p.terminate)
            start = time.time()
            p.start()

            time.sleep(0.75)
            os.kill(p.pid, signal.SIGINT)
            p.join(1)

            with contextlib.closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))

        self.assertGreaterEqual(sum(1 for r in rows if r['stat_pid'] == os.getppid()), 5)
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=2)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_n_times(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            record.run(
                procfile_list=['stat'],
                database_file=f.name,
                interval=0.01,
                recnum=4,
                query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            )
            with contextlib.closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))

        self.assertEqual(4, sum(1 for r in rows if r['stat_pid'] == os.getppid()))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1.5)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_environment(self):
        with tempfile.NamedTemporaryFile() as f:
            with tempfile.NamedTemporaryFile() as f_log:
                start = time.time()
                record.run(
                    procfile_list=['stat'],
                    database_file=f.name,
                    interval=0.01,
                    recnum=4,
                    reevalnum=2,
                    environment=[['P', 'echo {} | tee -a {}'.format(os.getppid(), f_log.name)]],
                    query='$..children[?(@.stat.pid == $P)]',
                )
                self.assertEqual(''.join(['{}\n'.format(os.getppid())] * 2).encode(), f_log.read())

                with contextlib.closing(sqlite3.connect(f.name)) as conn:
                    conn.row_factory = sqlite3.Row

                    cursor = conn.execute('SELECT * FROM record')
                    rows = list(map(dict, cursor))

        self.assertEqual(4, sum(1 for r in rows if r['stat_pid'] == os.getppid()))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1.5)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_syntax_error(self):
        with self.assertRaises(CommandError):
            record.run(
                procfile_list=['stat'], database_file=':memory:', interval=1, query='$!#'
            )

    def test_record_pid_list(self):
        with mock.patch('procpath.cmd.record.proctree.Forest', ChromiumTree):
            with tempfile.NamedTemporaryFile() as f:
                start = time.time()
                record.run(
                    procfile_list=['stat'],
                    database_file=f.name,
                    interval=1,
                    recnum=1,
                    pid_list='18484, 18529, 18503, 18508,',
                    query='$..children[?(@.stat.pid in [18503, 18508])]',
                )
                with contextlib.closing(sqlite3.connect(f.name)) as conn:
                    conn.row_factory = sqlite3.Row

                    cursor = conn.execute('SELECT * FROM record')
                    rows = list(map(dict, cursor))

        self.assertEqual(3, len(rows))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertEqual([18503, 18517, 18508][i], row['stat_pid'])
            self.assertAlmostEqual(start, row.pop('ts'), delta=1.5)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_pid_list_only(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            record.run(
                procfile_list=['stat'],
                database_file=f.name,
                environment=[['P', 'echo {}'.format(os.getppid())]],
                interval=1,
                recnum=1,
                pid_list='$P',
            )
            with contextlib.closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        root = rows[0]
        self.assertEqual(1, root.pop('record_id'))
        self.assertEqual(1, root['stat_pid'])
        self.assertAlmostEqual(start, root.pop('ts'), delta=0.1)
        self.assertEqual(
            list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in root.keys()],
        )

        for i, row in enumerate(rows):
            if row['stat_pid'] == os.getppid():
                break

            self.assertEqual(1, len([r for r in rows if r['stat_ppid'] == row['stat_pid']]))
        else:
            self.fail('No PPID found')

        self.assertLessEqual(i, len(rows) - 1)

        ppid = os.getppid()
        self.assertTrue(all(r['stat_ppid'] == ppid or r['stat_pid'] == ppid for r in rows[i:]))

    def test_record_stop_without_result(self):
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        self.addCleanup(loop.close)

        async def test():
            with tempfile.NamedTemporaryFile() as f:
                target_start = time.time()
                process = await asyncio.create_subprocess_exec('sleep', '0.2')
                await asyncio.sleep(0.1)

                record_start = time.time()
                record_fn = functools.partial(
                    record.run,
                    procfile_list=['stat'],
                    database_file=f.name,
                    interval=0.01,
                    recnum=100,
                    pid_list=str(process.pid),
                    stop_without_result=True,
                )
                await loop.run_in_executor(None, record_fn)

                self.assertTrue(target_start + 0.2 <= time.time() < target_start + 0.4)
                self.assertEqual(0, process.returncode)
                with contextlib.closing(sqlite3.connect(f.name)) as conn:
                    conn.row_factory = sqlite3.Row

                    cursor = conn.execute('SELECT * FROM record')
                    rows = list(map(dict, cursor))
                    self.assertGreaterEqual(len(rows), 1)
                    self.assertLess(len(rows), 10)

                for i, row in enumerate(rows, start=1):
                    self.assertEqual(process.pid, row['stat_pid'])
                    self.assertEqual(i, row.pop('record_id'))
                    self.assertAlmostEqual(record_start, row.pop('ts'), delta=0.1)
                    self.assertEqual(
                        list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                        [k.replace('stat_', '') for k in row.keys()],
                    )

        loop.run_until_complete(test())


class TestPlotCommand(unittest.TestCase):

    database_file = None

    @classmethod
    def setUpClass(cls):
        cls.database_file = tempfile.NamedTemporaryFile()
        cls.database_file.__enter__()

        storage = procrec.SqliteStorage(cls.database_file.name, ['stat'], utility.get_meta())
        data = proctree.flatten(get_chromium_node_list(), storage._procfile_list)
        with storage:
            for ts in range(1567504800, 1567504800 + 4):
                storage.record(ts, data)

    @classmethod
    def tearDownClass(cls):
        cls.database_file.close()

    def test_plot(self):
        with tempfile.NamedTemporaryFile() as f:
            plot.run(self.database_file.name, f.name, query_name_list=['rss'])

            svg_bytes = f.read()
            self.assertIn(b'<svg', svg_bytes)
            self.assertIn(b'Resident Set Size, MiB', svg_bytes)
            self.assertGreater(len(svg_bytes), 15_000)

    @unittest.skipUnless(apsw or sqlite3.sqlite_version_info >= (3, 25), 'sqlite3 is too old')
    def test_plot_logarithmic_two_axes(self):
        with tempfile.NamedTemporaryFile() as f:
            plot.run(
                self.database_file.name,
                f.name,
                logarithmic=True,
                query_name_list=['cpu', 'rss'],
                formatter='integer',
                style='LightGreenStyle',
            )

            svg_bytes = f.read()
            self.assertIn(b'<svg', svg_bytes)
            self.assertIn(b'CPU usage, % vs Resident Set Size, MiB', svg_bytes)
            self.assertGreater(len(svg_bytes), 30_000)

    def test_plot_query_count_error(self):
        with self.assertRaises(CommandError) as ctx:
            plot.run(self.database_file.name, '/dev/null')
        self.assertEqual('No or more than 2 queries to plot', str(ctx.exception))

        with self.assertRaises(CommandError) as ctx:
            plot.run(
                self.database_file.name, '/dev/null', query_name_list=['rss', 'rss', 'rss']
            )
        self.assertEqual('No or more than 2 queries to plot', str(ctx.exception))

    def test_plot_unknown_named_query(self):
        with self.assertRaises(CommandError) as ctx:
            plot.run(self.database_file.name, '/dev/null', query_name_list=['cpu', 'foo'])
        self.assertEqual('Unknown query foo', str(ctx.exception))

    @mock.patch('procpath.plotting.plot')
    def test_plot_title_override(self, plot_mock):
        plot.run(
            self.database_file.name,
            '/fake',
            query_name_list=['rss'],
            pid_list=[18467],
            title='The Strain',
        )
        plot_mock.assert_called_once_with(
            pid_series1={18467: [
                (1567504800.0, 208.2265625),
                (1567504801.0, 208.2265625),
                (1567504802.0, 208.2265625),
                (1567504803.0, 208.2265625),
            ]},
            pid_series2=None,
            plot_file='/fake',
            title='The Strain',
            style=None,
            formatter=None,
            logarithmic=False,
        )

    @mock.patch('procpath.plotting.plot')
    def test_plot_custom_query_file(self, plot_mock):
        with tempfile.NamedTemporaryFile() as f:
            f.write(b'''
                SELECT 1 ts, 2 pid, 3 value
                UNION
                SELECT 2 ts, 2 pid, 4 value
            ''')
            f.seek(0)

            plot.run(
                self.database_file.name,
                '/fake',
                query_name_list=['rss'],
                pid_list=[2, 18482],
                custom_query_file_list=[f.name],
                title='RSS vs Custom query',
            )
            plot_mock.assert_called_once_with(
                pid_series1={
                    18482: [
                        (1567504800.0, 53.76953125),
                        (1567504801.0, 53.76953125),
                        (1567504802.0, 53.76953125),
                        (1567504803.0, 53.76953125),
                    ]
                },
                pid_series2={2: [(1, 3), (2, 4)]},
                plot_file='/fake',
                style=None,
                formatter=None,
                title='RSS vs Custom query',
                logarithmic=False,
            )

    @mock.patch('procpath.plotting.plot')
    def test_plot_custom_value_expr(self, plot_mock):
        plot.run(
            self.database_file.name,
            '/fake',
            pid_list=[18467, 18482],
            custom_value_expr_list=['10', 'stat_minflt / 1000.0'],
        )
        plot_mock.assert_called_once_with(
            pid_series1={
                18467: [(1567504800, 10), (1567504801, 10), (1567504802, 10), (1567504803, 10)],
                18482: [(1567504800, 10), (1567504801, 10), (1567504802, 10), (1567504803, 10)],
            },
            pid_series2={
                18467: [
                    (1567504800.0, 51.931),
                    (1567504801.0, 51.931),
                    (1567504802.0, 51.931),
                    (1567504803.0, 51.931),
                ],
                18482: [
                    (1567504800.0, 3.572),
                    (1567504801.0, 3.572),
                    (1567504802.0, 3.572),
                    (1567504803.0, 3.572),
                ],
            },
            plot_file='/fake',
            style=None,
            formatter=None,
            logarithmic=False,
            title='Custom expression vs Custom expression',
        )

    @mock.patch('procpath.plotting.plot')
    def test_plot_rdp_epsilon(self, plot_mock):
        plot.run(
            self.database_file.name,
            '/fake',
            query_name_list=['rss'],
            pid_list=[18467],
            epsilon=0.1,
        )
        plot_mock.assert_called_once_with(
            pid_series1={18467: [
                (1567504800.0, 208.2265625),
                (1567504803.0, 208.2265625)
            ]},
            pid_series2=None,
            plot_file='/fake',
            title='Resident Set Size, MiB',
            style=None,
            formatter=None,
            logarithmic=False,
        )

    @mock.patch('procpath.plotting.plot')
    def test_plot_moving_average_window(self, plot_mock):
        plot.run(
            self.database_file.name,
            '/fake',
            query_name_list=['rss'],
            pid_list=[18467],
            moving_average_window=2,
        )
        plot_mock.assert_called_once_with(
            pid_series1={18467: [
                (1567504800.5, 208.2265625),
                (1567504801.5, 208.2265625),
                (1567504802.5, 208.2265625)
            ]},
            pid_series2=None,
            plot_file='/fake',
            title='Resident Set Size, MiB',
            style=None,
            formatter=None,
            logarithmic=False,
        )


class TestWatchCommand(unittest.TestCase):

    forest = None

    def setUp(self):
        self.forest = proctree.Forest({'stat': procfile.registry['stat']}, skip_self=False)

        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        self.addCleanup(loop.close)

    @classmethod
    def run_watch(cls, **kwargs):
        try:
            watch.run(**kwargs)
        except KeyboardInterrupt:
            pass

    def test_watch_verbatim_commands(self):
        with tempfile.NamedTemporaryFile() as f1, tempfile.NamedTemporaryFile() as f2:
            p = multiprocessing.Process(target=self.run_watch, kwargs={
                'interval': 0.2,
                'command_list': [
                    f'sleep 0.2 && echo abc >> {f1.name}',
                    f'sleep 0.2 && echo xyz >> {f2.name}',
                ],
                'procfile_list': ['stat', 'cmdline'],
                'stop_signal': 'SIGINT',
            })
            self.addCleanup(p.terminate)
            p.start()
            time.sleep(0.15)

            query = '$..children[?(@.stat.ppid == {})]..pid'.format(os.getpid())
            pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
            self.assertEqual(5, len(pids))  # 1 subprocess, 2 shells, 2 sleeps

            time.sleep(0.45)
            os.kill(p.pid, signal.SIGINT)
            p.join(1)
            self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

            self.assertEqual(b'abc\nabc\n', f1.read())
            self.assertEqual(b'xyz\nxyz\n', f2.read())

    def test_watch_environment(self):
        with tempfile.NamedTemporaryFile() as f1, tempfile.NamedTemporaryFile() as f2:
            p = multiprocessing.Process(target=self.run_watch, kwargs={
                'interval': 0.2,
                'command_list': [
                    f'sleep 0.2 && echo $D0 >> {f1.name}',
                    f'sleep 0.2 && echo $D1 >> {f2.name}',
                ],
                'procfile_list': ['stat'],
                'environment': [['D0', 'echo 1'], ['D1', 'echo ${D0}000']],
                'stop_signal': 'SIGINT',
            })
            self.addCleanup(p.terminate)
            p.start()
            time.sleep(0.15)

            query = '$..children[?(@.stat.ppid == {})]..pid'.format(os.getpid())
            pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
            self.assertEqual(5, len(pids))  # 1 subprocess, 2 shells, 2 sleeps

            time.sleep(0.45)
            os.kill(p.pid, signal.SIGINT)
            p.join(1)
            self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

            self.assertEqual(b'1\n1\n', f1.read())
            self.assertEqual(b'1000\n1000\n', f2.read())

    def test_watch_query(self):
        with tempfile.NamedTemporaryFile() as f1:
            ppid = os.getppid()
            p = multiprocessing.Process(target=self.run_watch, kwargs={
                'interval': 0.25,
                'command_list': [f'sleep 0.2 && echo $L >> {f1.name}'],
                'procfile_list': ['stat'],
                'environment': [['P', f'echo {ppid}']],
                'query_list': [['L', '$..children[?(@.stat.pid == $P)].stat.comm']],
                'stop_signal': 'SIGINT',
            })
            self.addCleanup(p.terminate)
            p.start()
            time.sleep(0.2)

            query = '$..children[?(@.stat.ppid == {})]..pid'.format(os.getpid())
            pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
            self.assertEqual(3, len(pids))  # 1 subprocess, 1 shells, 1 sleeps

            time.sleep(0.1)
            os.kill(p.pid, signal.SIGINT)
            p.join(1)
            self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

            query = f'$..children[?(@.stat.pid == {ppid})].stat.comm'
            stat_comm = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
            self.assertEqual(f'{stat_comm[0]}\n'.encode(), f1.read())

    def test_watch_tree_cleanup_on_sigint(self):
        p = multiprocessing.Process(target=self.run_watch, kwargs={
            'interval': 0.2,
            'command_list': ['sleep 10', 'sleep 10'],
            'procfile_list': ['stat', 'cmdline'],
            'stop_signal': 'SIGINT',
        })
        self.addCleanup(p.terminate)
        p.start()
        time.sleep(0.15)

        query = '$..children[?(@.stat.ppid == {})]..pid'.format(os.getpid())
        pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
        self.assertEqual(5, len(pids))  # 1 subprocess, 2 shells, 2 sleeps

        time.sleep(0.45)
        os.kill(p.pid, signal.SIGINT)
        p.join(1)
        self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

    def test_watch_tree_cleanup_on_repeat_end(self):
        p = multiprocessing.Process(target=self.run_watch, kwargs={
            'interval': 0.2,
            'command_list': ['sleep 10', 'sleep 10'],
            'procfile_list': ['stat'],
            'repeat': 1,
            'stop_signal': 'SIGINT',
        })
        self.addCleanup(p.terminate)
        p.start()
        time.sleep(0.15)

        query = '$..children[?(@.stat.ppid == {})]..pid'.format(os.getpid())
        pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
        self.assertEqual(5, len(pids))  # 1 subprocess, 2 shells, 2 sleeps

        p.join(1)
        self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

    def test_watch_tree_cleanup_on_error(self):
        async def test():
            with tempfile.NamedTemporaryFile() as f:
                f.write(b'-1')
                f.flush()

                process = await asyncio.create_subprocess_exec(
                    *[
                        sys.executable, '-m', 'procpath', 'watch',
                        '-i', '2',
                        '-e', f'P=cat {f.name}',
                        '-q', 'L=$..children[?(@.stat.pid == $P)]..pid',
                        '-c', 'echo $L',
                        '-c', 'sleep 666',
                    ],
                    stderr=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                )
                await asyncio.sleep(1.5)

                query = '$..children[?(@.stat.ppid == {})]..pid'.format(process.pid)
                pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
                self.assertEqual(2, len(pids))

            await asyncio.sleep(0.5)
            stdout, stderr = await process.communicate()
            self.assertEqual(b'', stdout)
            self.assertIn('Query L evaluated empty', stderr.decode())
            self.assertIn('No such file or directory', stderr.decode())
            self.assertIn('Variable P evaluated empty', stderr.decode())
            self.assertIn('Python syntax error', stderr.decode())

            self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

        asyncio.get_event_loop().run_until_complete(test())

    def test_watch_tree_cleanup_by_sigterm(self):
        p = multiprocessing.Process(target=self.run_watch, kwargs={
            'interval': 0.2,
            'command_list': ['sleep 10', 'sleep 10'],
            'procfile_list': ['stat'],
            'repeat': 1,
            'stop_signal': 'SIGTERM',
        })
        self.addCleanup(p.terminate)
        p.start()
        time.sleep(0.15)

        query = '$..children[?(@.stat.ppid == {})]..pid'.format(os.getpid())
        pids = jsonpyth.jsonpath(self.forest.get_roots(), query, always_return_list=True)
        self.assertEqual(5, len(pids))  # 1 subprocess, 2 shells, 2 sleeps

        p.join(1)
        self.assertTrue(all(not proctree.process_exists(pid) for pid in pids))

    def test_watch_empty_env_command_result(self):
        with self.assertLogs('procpath', 'INFO') as ctx:
            watch.run(
                interval=0,
                procfile_list=['stat'],
                command_list=['true'],
                environment=[['P', 'echo']],
                repeat=1,
                stop_signal='SIGINT',
            )
        self.assertEqual(1, len(ctx.records))
        self.assertEqual('Variable P evaluated empty', ctx.records[0].message)

    def test_watch_empty_query_result(self):
        with self.assertLogs('procpath', 'INFO') as ctx:
            watch.run(
                interval=0,
                procfile_list=['stat'],
                command_list=['true'],
                query_list=[['L', '$..children[?(@.stat.pid == -1)].stat.comm']],
                repeat=1,
                stop_signal='SIGINT',
            )
        self.assertEqual(1, len(ctx.records))
        self.assertEqual('Query L evaluated empty', ctx.records[0].message)

    def test_watch_query_error(self):
        with self.assertRaises(CommandError) as ctx:
            watch.run(
                interval=0,
                procfile_list=['stat'],
                command_list=['true'],
                query_list=[['L', '!@#$']],
                repeat=1,
                stop_signal='SIGINT',
            )
        self.assertEqual(
            'JSONPath syntax error - Expected {target set | child step | recurse step}, here:'
            '\n!@#$\n^',
            str(ctx.exception),
        )

    def test_watch_std_stream_logging(self):
        with self.assertLogs('procpath', 'INFO') as ctx:
            watch.run(
                interval=0.1,
                procfile_list=['stat'],
                command_list=[
                    'echo "Carousel"',
                    'sleep 0.05 && echo "A Glutton for Punishment" 1>&2',
                ],
                repeat=1,
                stop_signal='SIGINT',
            )
        self.assertEqual(2, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('№1: Carousel', ctx.records[0].message)
        self.assertEqual('WARNING', ctx.records[1].levelname)
        self.assertEqual('№2: A Glutton for Punishment', ctx.records[1].message)

    def test_watch_std_stream_write_after_stop(self):
        with tempfile.NamedTemporaryFile() as f:
            now = datetime.datetime.now().isoformat()
            f.write(now.encode())
            f.flush()

            with self.assertLogs('procpath', 'INFO') as ctx:
                watch.run(
                    interval=0,
                    repeat=1,
                    procfile_list=['stat'],
                    command_list=[f'sleep 0.005 && cat {f.name}'],
                    stop_signal='SIGINT',
                )

        self.assertEqual(1, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual(f'№1: {now}', ctx.records[0].message)

    def test_watch_process_pids_exposed(self):
        class serialnumber:
            """RFC 1982 comparison for PIDs."""

            with open('/proc/sys/kernel/pid_max') as f:
                max_pid = int(f.read())

            _half = max_pid // 2

            def __init__(self, i):
                self.i = i

            def __eq__(self, other):
                return self.i == other.i

            def __gt__(self, other):
                return (
                    self.i < other.i and (other.i - self.i > self._half)
                    or self.i > other.i and (self.i - other.i < self._half)
                )

        with tempfile.NamedTemporaryFile() as f:
            watch.run(
                interval=0,
                repeat=2,
                procfile_list=['stat'],
                command_list=[
                    'sleep 0.005 && echo "target process 1"',
                    'sleep 0.005 && echo "target process 2"',
                    f'env | grep WPS >> {f.name}',
                ],
                stop_signal='SIGINT',
            )

            prev_pid = None
            for i, line in enumerate(f.read().decode().splitlines()):
                name, value = line.split('=')
                self.assertEqual('WPS{}'.format(i % 2 + 1), name)

                if prev_pid:
                    self.assertGreater(serialnumber(int(value)), serialnumber(int(prev_pid)))

                prev_pid = int(value)

    def test_watch_no_restart(self):
        with tempfile.NamedTemporaryFile() as f:
            watch.run(
                interval=0,
                repeat=1000,
                procfile_list=['stat'],
                command_list=[f'sleep 0.005 && echo "On to Tarmac" >> {f.name}'],
                stop_signal='SIGINT',
                no_restart=True,
            )
            self.assertEqual(b'On to Tarmac\n', f.read())


class TestPlayCommand(unittest.TestCase):

    playbook_file = None

    def setUp(self):
        self.playbook_file = tempfile.NamedTemporaryFile('w')
        self.addCleanup(self.playbook_file.close)
        self.playbook_file.write(r'''
            [group1:query]
            environment:
              L=docker ps -f status=running -f name='^project_name' -q | xargs -I{} -- \
                docker inspect -f '{{.State.Pid}}' {} | tr '\n' ,
              TS=date +%s
            query: $..children[?(@.stat.pid in [$L])]
            sql_query: SELECT SUM(stat_rss) / 1024.0 * 4 total FROM record
            procfile_list: stat,cmdline,status

            [group1:record]
            environment:
              C1=docker inspect -f "{{.State.Pid}}" project_db_1
              C2=docker inspect -f "{{.State.Pid}}" project_app_1
            interval: 1
            recnum: 60
            reevalnum: 30
            database_file: out.sqlite
            query: $..children[?(@.stat.pid in [$C1, $C2])]

            [group1:plot]
            database_file: out.sqlite
            plot_file: rss.svg
            logarithmic: 1
            query_name: rss
            epsilon: 0.5
            moving_average_window: 10

            [group2:watch]
            interval: 601
            environment:
              S1=systemctl show --property MainPID redis-server | cut -d "=" -f 2
              C1=docker inspect -f "{{.State.Pid}}" app_gunicorn_1
            query:
              L1=$..children[?(@.stat.pid == $S1)]..pid
            command:
              smemstat -q -o redis-memdiff-$TS.json -p $L1 30 20
              timeout --foreground --signal SIGINT 600 \
                py-spy record --subprocesses --output app-flamegraph-$TS.svg --pid $C1
        ''')
        self.playbook_file.flush()

        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        self.addCleanup(loop.close)

    def test_play_all_mocked(self):
        output_file = io.StringIO()
        with contextlib.ExitStack() as stack:
            query_mock = stack.enter_context(mock.patch('procpath.cmd.query.run'))
            record_mock = stack.enter_context(mock.patch('procpath.cmd.record.run'))
            plot_mock = stack.enter_context(mock.patch('procpath.cmd.plot.run'))
            watch_mock = stack.enter_context(mock.patch('procpath.cmd.watch.run'))

            play.run(
                playbook_file=self.playbook_file.name,
                output_file=output_file,
                list_sections=False,
                dry_run=False,
                target=['*'],
            )

            query_mock.assert_called_once_with(
                delimiter=None,
                environment=[
                    [
                        'L',
                        (
                            "docker ps -f status=running -f name='^project_name' -q | xargs"
                            " -I{} -- docker inspect -f '{{.State.Pid}}' {} | tr '\\n' ,"
                        ),
                    ],
                    ['TS', 'date +%s'],
                ],
                indent=None,
                query='$..children[?(@.stat.pid in [$L])]',
                output_file=output_file,
                procfile_list=['stat', 'cmdline', 'status'],
                sql_query='SELECT SUM(stat_rss) / 1024.0 * 4 total FROM record'
            )
            record_mock.assert_called_once_with(
                database_file='out.sqlite',
                environment=[
                    ['C1', 'docker inspect -f "{{.State.Pid}}" project_db_1'],
                    ['C2', 'docker inspect -f "{{.State.Pid}}" project_app_1']
                ],
                interval=1.0,
                procfile_list=['stat', 'cmdline'],
                query='$..children[?(@.stat.pid in [$C1, $C2])]',
                recnum=60,
                reevalnum=30,
                pid_list=None,
                stop_without_result=False,
            )
            plot_mock.assert_called_once_with(
                after=None,
                before=None,
                custom_query_file_list=None,
                custom_value_expr_list=None,
                database_file='out.sqlite',
                epsilon=0.5,
                formatter=None,
                logarithmic=True,
                moving_average_window=10,
                pid_list=None,
                plot_file='rss.svg',
                query_name_list=['rss'],
                style=None,
                title=None,
            )
            watch_mock.assert_called_once_with(
                command_list=[
                    'smemstat -q -o redis-memdiff-$TS.json -p $L1 30 20',
                    (
                        'timeout --foreground --signal SIGINT 600 py-spy record '
                        '--subprocesses --output app-flamegraph-$TS.svg --pid $C1'
                    )
                ],
                environment=[
                    ['S1', 'systemctl show --property MainPID redis-server | cut -d "=" -f 2'],
                    ['C1', 'docker inspect -f "{{.State.Pid}}" app_gunicorn_1']
                ],
                interval=601.0,
                procfile_list=['stat', 'cmdline'],
                query_list=[['L1', '$..children[?(@.stat.pid == $S1)]..pid']],
                repeat=None,
                stop_signal='SIGINT',
                no_restart=False,
            )

        self.assertEqual('', output_file.getvalue())

    def test_play_list_sections(self):
        output_file = io.StringIO()
        play.run(
            playbook_file=self.playbook_file.name,
            output_file=output_file,
            list_sections=True,
            dry_run=False,
            target=['*'],
        )
        self.assertEqual(
            ['group1:query', 'group1:record', 'group1:plot', 'group2:watch'],
            output_file.getvalue().splitlines(),
        )

        output_file = io.StringIO()
        play.run(
            playbook_file=self.playbook_file.name,
            output_file=output_file,
            list_sections=True,
            dry_run=False,
            target=['group1:*'],
        )
        self.assertEqual(
            ['group1:query', 'group1:record', 'group1:plot'], output_file.getvalue().splitlines()
        )

        output_file = io.StringIO()
        play.run(
            playbook_file=self.playbook_file.name,
            output_file=output_file,
            list_sections=True,
            dry_run=False,
            target=['*:watch'],
        )
        self.assertEqual(['group2:watch'], output_file.getvalue().splitlines())

        output_file = io.StringIO()
        play.run(
            playbook_file=self.playbook_file.name,
            output_file=output_file,
            list_sections=True,
            dry_run=False,
            target=['group1:record', 'group2:watch'],
        )
        self.assertEqual(['group1:record', 'group2:watch'], output_file.getvalue().splitlines())

    def test_play_list_non_command_section(self):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('''
                [group1:query]
                query: $..children[?(@.stat.pid == 42)]
                procfile_list: stat,status

                [foo]
                a: b

                [bar]
                c: d
            ''')
            f.flush()

            output_file = io.StringIO()
            play.run(
                playbook_file=f.name,
                output_file=output_file,
                list_sections=True,
                dry_run=False,
                target=['*', 'foo'],
            )
            self.assertEqual(['group1:query'], output_file.getvalue().splitlines())

    def test_play_dry_run(self):
        output_file = io.StringIO()
        with self.assertLogs('procpath', 'INFO') as ctx:
            play.run(
                playbook_file=self.playbook_file.name,
                output_file=output_file,
                list_sections=False,
                dry_run=True,
                target=['group1:record', 'group1:plot'],
            )
        self.assertEqual(2, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('Executing section group1:record', ctx.records[0].message)
        self.assertEqual('INFO', ctx.records[1].levelname)
        self.assertEqual('Executing section group1:plot', ctx.records[1].message)

        self.assertEqual([
            '{',
            '  "database_file": "out.sqlite",',
            '  "environment": [',
            '    [',
            '      "C1",',
            '      "docker inspect -f \\"{{.State.Pid}}\\" project_db_1"',
            '    ],',
            '    [',
            '      "C2",',
            '      "docker inspect -f \\"{{.State.Pid}}\\" project_app_1"',
            '    ]',
            '  ],',
            '  "interval": 1.0,',
            '  "pid_list": null,',
            '  "procfile_list": [',
            '    "stat",',
            '    "cmdline"',
            '  ],',
            '  "query": "$..children[?(@.stat.pid in [$C1, $C2])]",',
            '  "recnum": 60,',
            '  "reevalnum": 30,',
            '  "stop_without_result": false',
            '}',
            '{',
            '  "after": null,',
            '  "before": null,',
            '  "custom_query_file_list": null,',
            '  "custom_value_expr_list": null,',
            '  "database_file": "out.sqlite",',
            '  "epsilon": 0.5,',
            '  "formatter": null,',
            '  "logarithmic": true,',
            '  "moving_average_window": 10,',
            '  "pid_list": null,',
            '  "plot_file": "rss.svg",',
            '  "query_name_list": [',
            '    "rss"',
            '  ],',
            '  "style": null,',
            '  "title": null',
            '}'
        ], output_file.getvalue().splitlines())

    def test_play_negative_flag(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f, mock.patch('procpath.cmd.plot.run') as pm:
            f.write('''
                [plot]
                database_file: out.sqlite
                plot_file: rss.svg
                logarithmic: 0
                query_name: cpu
            ''')
            f.flush()

            play.run(
                playbook_file=f.name,
                output_file=output_file,
                list_sections=False,
                dry_run=False,
                target=['plot'],
            )
            pm.assert_called_once_with(
                after=None,
                before=None,
                custom_query_file_list=None,
                custom_value_expr_list=None,
                database_file='out.sqlite',
                epsilon=None,
                formatter=None,
                logarithmic=False,
                moving_average_window=None,
                pid_list=None,
                plot_file='rss.svg',
                query_name_list=['cpu'],
                style=None,
                title=None,
            )

        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f, mock.patch('procpath.cmd.record.run') as rm:
            with tempfile.NamedTemporaryFile('w') as db_f:
                f.write(f'''
                    [record]
                    stop_without_result: 1
                    database_file: {db_f.name}
                ''')
                f.flush()
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['record'],
                )
            rm.assert_called_once_with(
                database_file=db_f.name,
                environment=None,
                interval=10.0,
                pid_list=None,
                procfile_list=['stat', 'cmdline'],
                query='',
                recnum=None,
                reevalnum=None,
                stop_without_result=True,
            )

        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f, mock.patch('procpath.cmd.watch.run') as wm:
            f.write('''
                [watch]
                interval: 1
                command: echo
                no_restart: yes
            ''')
            f.flush()
            play.run(
                playbook_file=f.name,
                output_file=output_file,
                list_sections=False,
                dry_run=False,
                target=['watch'],
            )
            wm.assert_called_once_with(
                command_list=['echo'],
                environment=None,
                interval=1.0,
                no_restart=True,
                procfile_list=['stat', 'cmdline'],
                query_list=None,
                repeat=None,
                stop_signal='SIGINT',
            )

    def test_play_watch(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('''
                [watch]
                environment: V=echo 123
                command: echo $V
                interval: 0
                repeat: 1
            ''')
            f.flush()

            with self.assertLogs('procpath', 'INFO') as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['watch'],
                )
        self.assertEqual(2, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('Executing section watch', ctx.records[0].message)
        self.assertEqual('INFO', ctx.records[1].levelname)
        self.assertEqual('№1: 123', ctx.records[1].message)

        self.assertEqual('', output_file.getvalue())

    def test_play_watch_override(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('''
                [watch]
                environment: V=echo 123
                command: echo $V $W $X
                interval: 0
                repeat: 1
            ''')
            f.flush()

            with self.assertLogs('procpath', 'INFO') as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['watch'],
                    option_override_list=[['environment', 'W=echo 234\nX=echo 345']]
                )
        self.assertEqual(2, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('Executing section watch', ctx.records[0].message)
        self.assertEqual('INFO', ctx.records[1].levelname)
        self.assertEqual('№1: 123 234 345', ctx.records[1].message)

        self.assertEqual('', output_file.getvalue())

    def test_play_query(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('''
                [foo:query]
                environment:
                  L=echo \\
                    {}
                query: $..children[?(@.stat.pid == $L)]
                sql_query: SELECT SUM(status_vmrss) total FROM record
                procfile_list: stat,status
            '''.format(os.getppid()))
            f.flush()

            with self.assertLogs('procpath', 'INFO') as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['*:query'],
                )
        self.assertEqual(1, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('Executing section foo:query', ctx.records[0].message)

        actual = json.loads(output_file.getvalue())
        self.assertEqual(1, len(actual))
        self.assertEqual({'total'}, actual[0].keys())
        self.assertGreater(actual[0]['total'], 1024)

    def test_play_record_plot(self):
        output_file = io.StringIO()
        with contextlib.ExitStack() as stack:
            playbook_file = stack.enter_context(tempfile.NamedTemporaryFile('w'))
            database_file = stack.enter_context(tempfile.NamedTemporaryFile())
            plot_file = stack.enter_context(tempfile.NamedTemporaryFile())

            playbook_file.write(f'''
                [group1:record]
                interval: 0.1
                recnum: 2
                query: $..children[?(@.stat.pid == {os.getppid()})]

                [group1:plot]
                plot_file: {plot_file.name}
                logarithmic: 1
                query_name:
                  rss
                  rss
            ''')
            playbook_file.flush()

            with self.assertLogs('procpath', 'INFO') as ctx:
                play.run(
                    playbook_file=playbook_file.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['group1:*'],
                    option_override_list=[['database_file', database_file.name]],
                )

                svg_bytes = plot_file.read()
                self.assertIn(b'<svg', svg_bytes)
                self.assertIn(b'Resident Set Size, MiB', svg_bytes)
                self.assertGreater(len(svg_bytes), 15_000)

        self.assertEqual(2, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('Executing section group1:record', ctx.records[0].message)
        self.assertEqual('INFO', ctx.records[1].levelname)
        self.assertEqual('Executing section group1:plot', ctx.records[1].message)

        self.assertEqual('', output_file.getvalue())

    def test_play_section_inheritance(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f, mock.patch('procpath.cmd.query.run') as m:
            f.write(r'''
                [stack_rss]
                environment:
                  L=docker ps -f status=running -f name='^staging' -q | xargs -I{} -- \
                    docker inspect -f '{{.State.Pid}}' {} | tr '\n' ,
                query: $..children[?(@.stat.pid in [$L])]
                procfile_list: stat

                [stack_rss:status]
                extends: stack_rss
                environment: TS=date +%s
                procfile_list: stat,status

                [stack_rss:status:query]
                extends: stack_rss:status
                sql_query: SELECT SUM(status_vmrss) total FROM record

                [stack_rss:stat:query]
                extends: stack_rss
                sql_query: SELECT SUM(stat_rss) * 4 total FROM record
            ''')
            f.flush()

            play.run(
                playbook_file=f.name,
                output_file=output_file,
                list_sections=False,
                dry_run=False,
                target=['stack_rss:*'],
            )

        self.assertEqual(
            [
                mock.call(
                    environment=[
                        [
                            'L',
                            (
                                "docker ps -f status=running -f name='^staging' -q | xargs"
                                " -I{} -- docker inspect -f '{{.State.Pid}}' {} | tr '\\n' ,"
                            )
                        ],
                        ['TS', 'date +%s'],
                    ],
                    query='$..children[?(@.stat.pid in [$L])]',
                    output_file=output_file,
                    procfile_list=['stat', 'status'],
                    sql_query='SELECT SUM(status_vmrss) total FROM record',
                    delimiter=None,
                    indent=None,
                ),
                mock.call(
                    environment=[
                        [
                            'L',
                            (
                                "docker ps -f status=running -f name='^staging' -q | xargs"
                                " -I{} -- docker inspect -f '{{.State.Pid}}' {} | tr '\\n' ,"
                            )
                        ],
                    ],
                    query='$..children[?(@.stat.pid in [$L])]',
                    output_file=output_file,
                    procfile_list=['stat'],
                    sql_query='SELECT SUM(stat_rss) * 4 total FROM record',
                    delimiter=None,
                    indent=None,
                )
            ],
            m.call_args_list,
        )

    def test_play_explicit_extends(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write(r'''
                [rss:query]
                sql_query: SELECT SUM(stat_rss) * 4 total FROM record

                [python]
                environment:
                  PIDS=docker ps -f status=running -f name='^staging' -q | xargs -I{} -- \
                       docker inspect -f '{{.State.Pid}}' {} | tr '\n' ,
                query: $..children[?(@.stat.pid in [$PIDS] and 'python' in @.stat.comm)]

                [container]
                query: $..children[?(@.stat.pid == $P)]

                [container:redis]
                extends: container
                environment:
                  P=docker inspect -f '{{.State.Pid}}' staging_redis_1

                [container:mysql]
                extends: container
                environment:
                  P=docker inspect -f '{{.State.Pid}}' staging_mysql_1

                [container:nginx]
                extends: container
                environment:
                  P=docker inspect -f '{{.State.Pid}}' staging_nginx_1

                [python:rss:query]
                extends:
                  python
                  rss:query

                [container:redis:rss:query]
                extends:
                  container:redis
                  rss:query

                [container:mysql:rss:query]
                extends:
                  container:mysql
                  rss:query

                [container:nginx:rss:query]
                extends:
                  container:nginx
                  rss:query
            ''')
            f.flush()

            with self.assertLogs('procpath', 'INFO') as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=True,
                    target=['container:redis:*', 'python:rss:query'],
                )

        self.assertEqual(2, len(ctx.records))
        self.assertEqual('INFO', ctx.records[0].levelname)
        self.assertEqual('Executing section container:redis:rss:query', ctx.records[0].message)
        self.assertEqual('INFO', ctx.records[1].levelname)
        self.assertEqual('Executing section python:rss:query', ctx.records[1].message)

        decoder = json.JSONDecoder()
        actual = []
        idx = 0
        while idx < len(output_file.getvalue()):
            obj, idx = decoder.raw_decode(output_file.getvalue(), idx)
            idx += 1
            actual.append(obj)

        self.assertEqual([
            {
                'delimiter': None,
                'environment': [['P', "docker inspect -f '{{.State.Pid}}' staging_redis_1"]],
                'indent': None,
                'procfile_list': ['stat', 'cmdline'],
                'query': '$..children[?(@.stat.pid == $P)]',
                'sql_query': 'SELECT SUM(stat_rss) * 4 total FROM record'
            }, {
                'delimiter': None,
                'indent': None,
                'environment': [
                    [
                        'PIDS',
                        "docker ps -f status=running -f name='^staging' -q | xargs "
                        "-I{} -- docker inspect -f '{{.State.Pid}}' {} | tr '\\n' ,"
                    ]
                ],
                'procfile_list': ['stat', 'cmdline'],
                'query': "$..children[?(@.stat.pid in [$PIDS] and 'python' in @.stat.comm)]",
                'sql_query': 'SELECT SUM(stat_rss) * 4 total FROM record'
            }
        ], actual)

    def test_play_missing_arguments(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('[foo:record]\nprocfile_list: stat')
            f.flush()

            with self.assertRaises(CommandError) as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['*'],
                )
            self.assertEqual(
                'Invalid section: the following arguments are required: database-file',
                str(ctx.exception),
            )
        self.assertEqual('', output_file.getvalue())

    def test_play_unrecognised_arguments(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('[foo:query]\nbar: baz')
            f.flush()

            with self.assertRaises(CommandError) as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['*'],
                )
            self.assertEqual(
                'Invalid section: unrecognized arguments: bar',
                str(ctx.exception),
            )
        self.assertEqual('', output_file.getvalue())

    def test_play_invalid_file(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('!@#$')
            f.flush()

            with self.assertRaises(CommandError) as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['*'],
                )
            self.assertTrue(str(ctx.exception).startswith('File contains no section headers.'))
        self.assertEqual('', output_file.getvalue())

    def test_play_invalid_section(self):
        output_file = io.StringIO()
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('[foo]\n!@#$')
            f.flush()

            with self.assertRaises(CommandError) as ctx:
                play.run(
                    playbook_file=f.name,
                    output_file=output_file,
                    list_sections=False,
                    dry_run=False,
                    target=['*'],
                )
            self.assertTrue(
                str(ctx.exception).startswith(f'Source contains parsing errors: {f.name!r}')
            )
        self.assertEqual('', output_file.getvalue())

    def test_play_absent(self):
        output_file = io.StringIO()
        with self.assertRaises(CommandError) as ctx:
            play.run(
                playbook_file=self.playbook_file.name,
                output_file=output_file,
                list_sections=False,
                dry_run=False,
                target=['foo:bar'],
            )
        self.assertEqual('No section matches the target(s)', str(ctx.exception))

    def test_split_multiline(self):
        self.assertEqual(['foo'], playbook.split_multiline('foo'))
        self.assertEqual(['a', 'b'], playbook.split_multiline('a\nb'))

        expected = [
            "L=docker ps -f status=running -f name='^project_name' -q | xargs -I{} --   "
            "docker inspect -f '{{.State.Pid}}' {} | tr '\\n' ,"
        ]
        actual = playbook.split_multiline(
            "L=docker ps -f status=running -f name='^project_name' -q | xargs -I{} -- \\\n"
            "  docker inspect -f '{{.State.Pid}}' {} | tr '\\n' ,"
        )
        self.assertEqual(expected, actual)

        self.assertEqual(['echo 12', 'echo 3'], playbook.split_multiline("echo 1\\\n2\necho 3"))
        self.assertEqual(['echo \\\\', 'echo /'], playbook.split_multiline('echo \\\\\necho /'))

        with self.assertRaises(ValueError) as ctx:
            playbook.split_multiline("echo 1\\")
        self.assertEqual('Line continuation end expected', str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            playbook.split_multiline("echo '")
        self.assertEqual('No closing quotation', str(ctx.exception))


class TestExploreCommand(unittest.TestCase):

    def test_explore(self):
        with tempfile.NamedTemporaryFile() as tmpf:
            with zipfile.ZipFile(tmpf, 'w') as myzip:
                with myzip.open('index.html', 'w') as f:
                    f.write(b'<html/>')
                with myzip.open('queries.json', 'w') as f:
                    f.write(b'[]')

            with tempfile.TemporaryDirectory() as tmpd:
                os.environ['XDG_CACHE_HOME'] = tmpd
                with mock.patch('procpath.cmd.explore.serve_dir') as httpd:
                    with mock.patch('procpath.cmd.explore.webbrowser') as webb:
                        with self.assertLogs('procpath', 'INFO') as ctx:
                            explore.run(
                                bind='127.0.0.1',
                                port=1234,
                                reinstall=False,
                                open_in_browser=False,
                                build_url='file://' + tmpf.name,
                            )
                    httpd.assert_called_once_with('127.0.0.1', 1234, f'{tmpd}/procpath/sqliteviz')
                    self.assertEqual([], webb.method_calls)

                self.assertEqual(
                    ['index.html', 'queries.json'],
                    sorted(os.listdir(f'{tmpd}/procpath/sqliteviz')),
                )
                with open(f'{tmpd}/procpath/sqliteviz/index.html') as f:
                    self.assertEqual('<html/>', f.read())
                with open(f'{tmpd}/procpath/sqliteviz/queries.json') as f:
                    self.assertEqual(
                        json.dumps(explore.get_visualisation_bundle(), sort_keys=True), f.read()
                    )

                self.assertEqual(2, len(ctx.records))
                self.assertEqual(
                    f'Downloading file://{tmpf.name} into {tmpd}/procpath/sqliteviz',
                    ctx.records[0].message,
                )
                self.assertEqual(
                    'Serving Sqliteviz at http://127.0.0.1:1234/', ctx.records[1].message
                )

                # Cannot be downloaded again
                tmpf.close()

                with mock.patch('procpath.cmd.explore.serve_dir') as httpd:
                    with mock.patch('procpath.cmd.explore.webbrowser') as webb:
                        with self.assertLogs('procpath', 'INFO') as ctx:
                            explore.run(
                                bind='',
                                port=8000,
                                reinstall=False,
                                open_in_browser=True,
                                build_url='file://' + tmpf.name,
                            )
                    httpd.assert_called_once_with('', 8000, f'{tmpd}/procpath/sqliteviz')
                    self.assertEqual([mock.call.open('http://localhost:8000/')], webb.method_calls)

                self.assertEqual(
                    ['index.html', 'queries.json'],
                    sorted(os.listdir(f'{tmpd}/procpath/sqliteviz')),
                )
                with open(f'{tmpd}/procpath/sqliteviz/index.html') as f:
                    self.assertEqual('<html/>', f.read())
                with open(f'{tmpd}/procpath/sqliteviz/queries.json') as f:
                    self.assertEqual(
                        json.dumps(explore.get_visualisation_bundle(), sort_keys=True), f.read()
                    )

                self.assertEqual(2, len(ctx.records))
                self.assertEqual(
                    f'Serving existing Sqliteviz from {tmpd}/procpath/sqliteviz',
                    ctx.records[0].message,
                )
                self.assertEqual(
                    'Serving Sqliteviz at http://localhost:8000/', ctx.records[1].message
                )

    @classmethod
    def explore(cls, build_url, env):
        os.environ.update(env)
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                explore.run(
                    build_url=build_url,
                    open_in_browser=False,
                    bind='',
                    port=18000,
                    reinstall=False,
                )
        except KeyboardInterrupt:
            pass

    def test_explore_serve(self):
        with tempfile.NamedTemporaryFile() as tmpf:
            with zipfile.ZipFile(tmpf, 'w') as myzip, myzip.open('index.html', 'w') as f:
                f.write(b'<html/>')

            with tempfile.TemporaryDirectory() as tmpd:
                os.environ['XDG_CACHE_HOME'] = tmpd
                p = multiprocessing.Process(
                    target=self.explore, args=('file://' + tmpf.name, os.environ)
                )
                self.addCleanup(p.terminate)
                p.start()
                time.sleep(0.2)

                response = urllib.request.urlopen('http://localhost:18000/')
                self.assertEqual(b'<html/>', response.read())

                os.kill(p.pid, signal.SIGINT)
                p.join(1)


def get_chromium_node_list():
    """
    Get procpath search sample of Chromium browser process tree.

    ::

        chromium-browser ...
        ├─ chromium-browser --type=utility ...
        ├─ chromium-browser --type=gpu-process ...
        │  └─ chromium-browser --type=broker
        └─ chromium-browser --type=zygote
           └─ chromium-browser --type=zygote
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=utility ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              └─ chromium-browser --type=renderer ...

    """

    pid_18467 = {
        'stat': {
            'pid': 18467,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 1,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194560,
            'minflt': 51931,
            'cminflt': 24741,
            'majflt': 721,
            'cmajflt': 13,
            'utime': 455,
            'stime': 123,
            'cutime': 16,
            'cstime': 17,
            'priority': 20,
            'nice': 0,
            'num_threads': 40,
            'itrealvalue': 0,
            'starttime': 62870630,
            'vsize': 2981761024,
            'rss': 53306,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser ...',
    }
    pid_18482 = {
        'stat': {
            'pid': 18482,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194560,
            'minflt': 3572,
            'cminflt': 0,
            'majflt': 49,
            'cmajflt': 0,
            'utime': 3,
            'stime': 2,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870663,
            'vsize': 460001280,
            'rss': 13765,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote',
    }
    pid_18484 = {
        'stat': {
            'pid': 18484,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18482,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194624,
            'minflt': 278,
            'cminflt': 4862,
            'majflt': 0,
            'cmajflt': 15,
            'utime': 0,
            'stime': 1,
            'cutime': 27,
            'cstime': 4,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870674,
            'vsize': 460001280,
            'rss': 3651,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote',
    }
    pid_18529 = {
        'stat': {
            'pid': 18529,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 3285,
            'cminflt': 0,
            'majflt': 78,
            'cmajflt': 0,
            'utime': 16,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870743,
            'vsize': 5411180544,
            'rss': 19849,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18531 = {
        'stat': {
            'pid': 18531,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 18231,
            'cminflt': 0,
            'majflt': 183,
            'cmajflt': 0,
            'utime': 118,
            'stime': 18,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870744,
            'vsize': 16164175872,
            'rss': 26117,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18555 = {
        'stat': {
            'pid': 18555,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 62472,
            'cminflt': 0,
            'majflt': 136,
            'cmajflt': 0,
            'utime': 1166,
            'stime': 59,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 14,
            'itrealvalue': 0,
            'starttime': 62870769,
            'vsize': 14124892160,
            'rss': 63235,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18569 = {
        'stat': {
            'pid': 18569,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 2695,
            'cminflt': 0,
            'majflt': 8,
            'cmajflt': 0,
            'utime': 7,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 11,
            'itrealvalue': 0,
            'starttime': 62870779,
            'vsize': 5407739904,
            'rss': 18979,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18571 = {
        'stat': {
            'pid': 18571,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 930,
            'cminflt': 0,
            'majflt': 20,
            'cmajflt': 0,
            'utime': 6,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 5,
            'itrealvalue': 0,
            'starttime': 62870781,
            'vsize': 5057503232,
            'rss': 8825,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...',
    }
    pid_18593 = {
        'stat': {
            'pid': 18593,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 12212,
            'cminflt': 0,
            'majflt': 2,
            'cmajflt': 0,
            'utime': 171,
            'stime': 11,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870786,
            'vsize': 5419442176,
            'rss': 22280,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18757 = {
        'stat': {
            'pid': 18757,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 1624,
            'cminflt': 0,
            'majflt': 0,
            'cmajflt': 0,
            'utime': 2,
            'stime': 0,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 11,
            'itrealvalue': 0,
            'starttime': 62871186,
            'vsize': 5389012992,
            'rss': 12882
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...'
    }
    pid_18769 = {
        'stat': {
            'pid': 18769,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 78483,
            'cminflt': 0,
            'majflt': 3,
            'cmajflt': 0,
            'utime': 906,
            'stime': 34,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871227,
            'vsize': 5497511936,
            'rss': 54376,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18770 = {
        'stat': {
            'pid': 18770,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 24759,
            'cminflt': 0,
            'majflt': 2,
            'cmajflt': 0,
            'utime': 260,
            'stime': 15,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871228,
            'vsize': 5438599168,
            'rss': 31106,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18942 = {
        'stat': {
            'pid': 18942,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 12989,
            'cminflt': 0,
            'majflt': 16,
            'cmajflt': 0,
            'utime': 77,
            'stime': 5,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871410,
            'vsize': 5436309504,
            'rss': 27106,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18503 = {
        'stat': {
            'pid': 18503,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194304,
            'minflt': 14361,
            'cminflt': 0,
            'majflt': 46,
            'cmajflt': 0,
            'utime': 112,
            'stime': 21,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 6,
            'itrealvalue': 0,
            'starttime': 62870711,
            'vsize': 877408256,
            'rss': 27219,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=gpu-process ...',
    }
    pid_18517 = {
        'stat': {
            'pid': 18517,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18503,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194368,
            'minflt': 86,
            'cminflt': 0,
            'majflt': 0,
            'cmajflt': 0,
            'utime': 0,
            'stime': 0,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870723,
            'vsize': 524230656,
            'rss': 4368,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=broker',
    }
    pid_18508 = {
        'stat': {
            'pid': 18508,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936128,
            'minflt': 9993,
            'cminflt': 0,
            'majflt': 55,
            'cmajflt': 0,
            'utime': 151,
            'stime': 47,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870714,
            'vsize': 1302757376,
            'rss': 20059,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...',
    }

    return [
        {
            **pid_18467,
            'children': [
                {
                    **pid_18482,
                    'children': [
                        {
                            **pid_18484,
                            'children': [
                                pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                                pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
                            ]
                        }
                    ]
                },
                {
                    **pid_18503,
                    'children': [pid_18517]
                },
                pid_18508
            ]
        },
        {
            **pid_18482,
            'children': [
                {
                    **pid_18484,
                    'children': [
                        pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                        pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
                    ]
                }
            ]
        },
        {
            **pid_18503,
            'children': [pid_18517]
        },
        pid_18508,
        {
            **pid_18484,
            'children': [
                pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
            ]
        },
        pid_18517,
        pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
        pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
    ]
