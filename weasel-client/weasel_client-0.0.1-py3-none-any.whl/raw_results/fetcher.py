import copy
import datetime
import json
import lzma
import os
import requests
import shutil
import sqlite3


class ResultClient:
    def __init__(self, url, storage, pseudonym_path=None):
        self.url = url
        self.storage = storage
        self.index = set()
        self._get_index()
        self._pseudonym_path = pseudonym_path

        if pseudonym_path:
            if not os.path.exists(pseudonym_path):
                raise ValueError('Pseudonym path does not exist')
            self._sql_conn = sqlite3.connect(pseudonym_path)

    def _get_index(self):
        resp = requests.get(self.url + '/index.txt')
        resp.raise_for_status()
        self.index = set(d for d in resp.iter_lines(decode_unicode=True))

    def _get_cleartext_url(self, pseudonym):
        if self._pseudonym_path is None:
            raise ValueError('No path to pseudonym database given')

        cursor = self._sql_conn.cursor()
        res = cursor.execute('SELECT cleartext FROM pseudonyms_urls WHERE hash=?',
                             (pseudonym,)).fetchone()
        if res:
            return res[0]

    def _get_cleartext_domain(self, pseudonym):
        if self._pseudonym_path is None:
            raise ValueError('No path to pseudonym database given')

        cursor = self._sql_conn.cursor()
        res = cursor.execute('SELECT cleartext FROM pseudonyms_domains WHERE hash=?',
                             (pseudonym,)).fetchone()
        if res:
            return res[0]

    @property
    def results(self):
        return RangeSet(self)

    def get_day_result(self, day):
        return DayResults(self, day)


class RangeSet:
    _begin_year, _begin_month, _begin_day = None, None, None
    _end_year, _end_month, _end_day = None, None, None

    def __init__(self, client: ResultClient):
        self.client = client

    def range_from(self, year=None, month=None, day=None):
        c = copy.copy(self)
        if year:
            c._begin_year = year
        if month:
            c._begin_month = month
        if day:
            c._begin_day = day

        return c

    def range_to(self, year=None, month=None, day=None):
        c = copy.copy(self)
        if year:
            c._end_year = year
        if month:
            c._end_month = month
        if day:
            c._end_day = day

        return c

    def select_date(self, year, month, day):
        res = self.range_from(year, month, day)
        return res.range_to(year, month, day)

    def __iter__(self):
        first_day = "{:04d}-{:02d}-{:02d}".format(
            self._begin_year if self._begin_year else 0,
            self._begin_month if self._begin_month else 0,
            self._begin_day if self._begin_day else 0
        )

        last_day = "{:04d}-{:02d}-{:02d}".format(
            self._end_year if self._end_year else 9999,
            self._end_month if self._end_month else 12,
            self._end_day if self._end_day else 31
        )

        for day in sorted(self.client.index):
            if day < first_day:
                continue

            if day > last_day:
                return

            yield self.client.get_day_result(day)


class DayResults:
    def __init__(self, client: ResultClient, day):
        self.client = client
        self.day = day
        self.year, self.month, _ = self.day.split('-')

    def __str__(self):
        return "<DayResults({})>".format(self.day)

    @property
    def url(self):
        return f'{self.client.url}/{self.year}/{self.month}/{self.day}_Polecat.xz'

    def iter(self, path=None, stream=False):
        if stream:
            for res in self._stream_results():
                yield res
            return

        if path is None:
            path = self._prepare_path()

        if not os.path.isfile(path):
            path = self.download()

        with lzma.open(path) as fp:
            for line in fp:
                yield Result(client, json.loads(line))

    def _stream_results(self):
        resp = requests.get(self.url, stream=True)
        resp.raise_for_status()

        with lzma.LZMAFile(resp.raw) as fp:
            for line in fp:
                yield Result(self.client, json.loads(line))

    def download(self, path=None, override=False):
        if self.client.storage is None and path is None:
            raise ValueError('Path is set neither on function call nor in the ResultClient')

        resp = requests.get(self.url, stream=True)
        resp.raise_for_status()

        out_path = path if path else self._prepare_path()
        if os.path.exists(out_path) and not override:
            return out_path

        try:
            with open(out_path, 'wb') as fp:
                resp.raw.decode = True
                shutil.copyfileobj(resp.raw, fp)
        except:
            os.remove(out_path)
            raise

        return out_path

    def _prepare_path(self):
        try:
            os.mkdir(os.path.join(self.client.storage, self.year))
        except FileExistsError:
            pass

        try:
            os.mkdir(os.path.join(self.client.storage, self.year, self.month))
        except FileExistsError:
            pass

        return os.path.join(self.client.storage, self.year, self.month,
                            '{}_Polecat.xz'.format(self.day))


class Result:
    def __init__(self, client: ResultClient, raw: dict):
        self.client = client
        self.raw = raw

    @property
    def url(self):
        return self.client._get_cleartext_url(self.raw['url'])

    @property
    def domain(self):
        return self.client._get_cleartext_domain(self.raw['domain'])

    @property
    def matches(self):
        return self.raw['matches'] if 'matches' in self.raw else None

    @property
    def datetime(self):
        return datetime.datetime.strptime(self.raw['date'], '%Y-%m-%d %H:%M:%S.%f')


if __name__ == '__main__':
    # Create client connection and list available dates
    client = ResultClient('https://weasel.cs.uni-bonn.de/polecat/', 'cache',
                          'pseudonyms_prod.sqlite')
    print(client.index)

    # Iterate over a RangeSet
    for results in client.results.select_date(2020, 6, 1):
        print(results)
        i, j = 0, 0

        # Iter over day results
        for match in results.iter(stream=True):
            if match.url is None or match.domain is None:
                j += 1

            i += 1
            if i % 500000 == 0:
                print('Processed ', i)

        print('Results with missing pseudonyms: ', j)
