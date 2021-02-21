import http.server
import io
import json
import logging
import os
import pathlib
import shutil
import threading
import webbrowser
import zipfile
from functools import partial
from urllib.request import urlopen


__all__ = 'run',

logger = logging.getLogger('procpath')


def install_sqliteviz(zip_url: str, target_dir: pathlib.Path):
    response = urlopen(zip_url)
    with zipfile.ZipFile(io.BytesIO(response.read())) as z:
        z.extractall(target_dir)

    (target_dir / 'queries.json').write_text(
        json.dumps(get_visualisation_bundle(), sort_keys=True)
    )


def get_visualisation_bundle():
    """Get Sqliteviz import-able visualisation bundle."""

    return [{
        'id': '3LwnE0pWobvqGM3ieE5Cz',
        'createdAt': '2020-11-22T18:19:38.042Z',
        'name': 'RSS per PID',
        'query': '''
            SELECT
              datetime(ts, 'unixepoch', 'localtime') ts,
              stat_pid,
              stat_rss / 1024.0 / 1024 * (SELECT value FROM meta WHERE key = 'page_size') rss
            FROM record
        ''',
        'chart': {
            'data': [{
                'meta': {'columnNames': {'x': 'ts', 'y': 'rss'}},
                'mode': 'lines',
                'type': 'scatter',
                'x': None,
                'xsrc': 'ts',
                'y': None,
                'ysrc': 'rss',
                'transforms': [{
                    'groups': None,
                    'groupssrc': 'stat_pid',
                    'meta': {'columnNames': {'groups': 'stat_pid'}},
                    'styles': [],
                    'type': 'groupby',
                }],
            }],
            'frames': [],
            'layout': {
                'autosize': True,
                'title': {'text': 'RSS per PID, MiB'},
                'xaxis': {
                    'autorange': True,
                    'range': [],
                    'type': 'date'
                },
                'yaxis': {
                    'autorange': True,
                    'range': [],
                    'type': 'linear'
                },
            },
        },
    }, {
        'id': 'ZHRGHpyWv6JVXkz3bDO40',
        'createdAt': '2020-11-22T18:22:05.114Z',
        'name': 'CPU per PID',
        'query': '''
            WITH diff AS (
              SELECT
                ts,
                stat_pid,
                stat_utime + stat_stime - LAG(stat_utime + stat_stime) OVER (
                  PARTITION BY stat_pid
                  ORDER BY record_id
                ) tick_diff,
                ts - LAG(ts) OVER (
                  PARTITION BY stat_pid
                  ORDER BY record_id
                ) ts_diff
              FROM record
            )
            SELECT
              datetime(ts, 'unixepoch', 'localtime') ts,
              stat_pid,
              100.0 * tick_diff / (SELECT value FROM meta WHERE key = 'clock_ticks') / ts_diff
            cpu_load
            FROM diff
        ''',
        'chart': {
            'data': [{
                'meta': {'columnNames': {'x': 'ts', 'y': 'cpu_load'}},
                'mode': 'lines',
                'type': 'scatter',
                'x': None,
                'xsrc': 'ts',
                'y': None,
                'ysrc': 'cpu_load',
                'transforms': [{
                    'groups': None,
                    'groupssrc': 'stat_pid',
                    'meta': {'columnNames': {'groups': 'stat_pid'}},
                    'styles': [],
                    'type': 'groupby'
                }],
            }],
            'frames': [],
            'layout': {
                'autosize': True,
                'title': {'text': 'CPU per PID, %'},
                'xaxis': {
                    'autorange': True,
                    'range': [],
                    'type': 'date'
                },
                'yaxis': {
                    'autorange': True,
                    'range': [],
                    'type': 'linear'
                },
            },
        },
    }]


def serve_dir(bind: str, port: int, directory: str):
    try:
        server_cls = http.server.ThreadingHTTPServer
        handler_cls = partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    except AttributeError:
        # py36
        server_cls = http.server.HTTPServer
        handler_cls = http.server.SimpleHTTPRequestHandler
        os.chdir(directory)

    with server_cls((bind, port), handler_cls) as httpd:
        httpd.serve_forever()


def run(bind: str, port: int, open_in_browser: bool, reinstall: bool, build_url: str):
    user_cache_dir = pathlib.Path(os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache')))
    sqliteviz_dir = user_cache_dir / 'procpath' / 'sqliteviz'
    if not sqliteviz_dir.exists() or reinstall:
        shutil.rmtree(sqliteviz_dir, ignore_errors=True)
        sqliteviz_dir.mkdir(parents=True)
        logger.info('Downloading %s into %s', build_url, sqliteviz_dir)
        install_sqliteviz(build_url, sqliteviz_dir)
    else:
        logger.info('Serving existing Sqliteviz from %s', sqliteviz_dir)

    url = 'http://{host}:{port}/'.format(port=port, host=bind or 'localhost')
    logger.info('Serving Sqliteviz at %s', url)

    server_fn = partial(serve_dir, bind, port, str(sqliteviz_dir))
    server = threading.Thread(target=server_fn, daemon=True)
    server.start()

    if open_in_browser:
        webbrowser.open(url)

    server.join()
