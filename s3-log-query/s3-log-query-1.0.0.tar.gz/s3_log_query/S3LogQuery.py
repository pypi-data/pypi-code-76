import logging
import boto3
import re
import pandas as pd
import concurrent.futures
from itertools import repeat
from typing import Dict, List, Union
from datetime import datetime
from dateutil.parser import parse

__author__ = "mikethoun"
__copyright__ = "mikethoun"
__license__ = "apache license 2.0"


class LogQuery:
    """
    This object fetches, aggregates, and returns log files from S3.

    :param Dict[str, str] log_paths: Dict of key-value pairs that represent the server name and the log file path in S3.
    :param str s3_bucket: Name of S3 bucket
    :param str timestamp_format: Format of timestamps in the log files.
    :param str log_format_regex: Regex to split log messages into fields.
    :param str fields: List of names that represent log file fields.
    """

    def __init__(self, log_paths: Dict[str, str], s3_bucket: str, timestamp_format: str = '%m/%d/%Y %-H:%M:%S.%f',
                 log_format_regex: str = '\[(.*?)\]|((?<=] ).*$)', fields=None) -> None:
        self.s3_bucket = s3_bucket
        self.log_paths = log_paths
        self.timestamp_format = timestamp_format
        self.log_format_regex = log_format_regex
        self.fields = ['timestamp', 'severity', 'message', 'server'] if fields is None else fields

    @staticmethod
    def __create_severity_filter(severity: int) -> str:
        """Creates a severity filter.

        This function returns a dynamic SQL string that can be used to filter for messages of a minimum severity
        level in S3 Select queries.

        :param int severity: Logging level constant for minimum severity to include e.g. logging.WARN
        :return: Returns a dynamic SQL WHERE clause condition.
        :rtype: str
        """
        severity_filter = ""

        for k, v in logging._nameToLevel.items():
            severity_filter += f" _1 LIKE '%[{k.lower()}]%' OR " if v >= severity else ""

        if severity_filter:
            return "AND (" + severity_filter[:-3] + ")"
        else:
            return severity_filter

    def __execute_s3select(self, server: str, start_time: str, severity_filter: int, entries: int) -> pd.DataFrame:
        """Execute S3 Select query.

        This function executes an S3 Select query and returns the results as a Pandas DataFrame.

        :param str server: Name of server.
        :param str start_time: Minimum log timestamp to fetch.
        :param int severity_filter: Minimum log severity to fetch.
        :param int entries: Number of log entries to fetch.
        :return: Returns a dataframe containing selected log messages for server.
        :rtype: pd.DataFrame
        """
        s3 = boto3.session.Session().client('s3')

        try:
            r = s3.select_object_content(
                Bucket=self.s3_bucket,
                Key=self.log_paths[server],
                ExpressionType='SQL',
                Expression=f"select _1 from s3object WHERE _1 >= '[{start_time}]' {severity_filter} LIMIT {entries}",
                InputSerialization={'CSV': {"FileHeaderInfo": "NONE"}},
                OutputSerialization={'CSV': {}},
            )
        except s3.exceptions.NoSuchKey:
            return pd.DataFrame()

        data = []
        for event in r['Payload']:
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8').splitlines()
                for x in records:
                    data.append([''.join(t) for t in re.findall(self.log_format_regex, x)] + [server])

        df = pd.DataFrame(data, columns=self.fields)
        df.set_index('timestamp', inplace=True)
        return df

    def query(self, keys: List[str], start: str = None, entries: int = 100, min_severity: int = logging.ERROR,
              output: str = 'string') -> Union[str, pd.DataFrame]:
        """ Download and aggregate log files from S3.

        This function downloads and aggregates log files from S3 using S3 Select and Multi-Threading.

        :param str keys: List of server names.
        :param str start: Minimum log timestamp to fetch.
        :param int entries: Number of log entries to fetch.
        :param int min_severity: Minimum log severity to fetch.
        :param str output: Determines the type returned by the function. Accepts 'string' or 'dataframe' as an argument.
        :return: Returns fetched logged messages.
        :rtype: str or pd.DataFrame
        """
        start_time = datetime.strftime(parse(start), self.timestamp_format)[:-2]
        severity = self.__create_severity_filter(severity=min_severity)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.__execute_s3select, keys, repeat(start_time), repeat(severity), repeat(entries))

        log_df = pd.concat(results)
        log_df.sort_index(inplace=True)
        if output == 'dataframe':
            return log_df
        else:
            return "No Log Messages Found." if log_df.empty else log_df.to_string()
