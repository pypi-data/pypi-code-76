import logging
import datetime as dt


class NrqlApiResponse:
    """
    Response object from nrql_api

    """
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)

    def __init__(self, status, json_body, headers, method, content_type, exec_time, is_ok, is_debug=False, query_type='raw'):
        self.status = status
        self.json_body = json_body
        self.headers = headers
        self.method = method
        self.content_type = content_type
        self.exec_time = exec_time
        self.is_ok = is_ok
        self.query_type = query_type
        if is_debug:
            NrqlApiResponse.logger.setLevel(logging.DEBUG)

    def __repr__(self):
        return str(self.json_body)

    @property
    def is_error(self):
        return not self.is_ok or "errors" in self.json_body

    @property
    def error_message(self) -> str:
        """
        Return first message from errors array inside json_body

        """
        if self.is_error:
            try:
                message = self.json_body["errors"][0]["message"]
                return message
            except KeyError as e:
                NrqlApiResponse.logger.exception(e)
                return f"Exception {e}"
        else:
            return ""

    @property
    def errors(self) -> list:
        """
        Return all errors array

        """
        if self.is_error:
            try:
                l = self.json_body["errors"]
                return l
            except KeyError as e:
                NrqlApiResponse.logger.exception(e)
                return [f"Exception {e}"]
        else:
            return []

    @property
    def results(self) -> dict:
        return self.json_body["data"]["actor"]["account"]["nrql"]["results"]

    @property
    def is_empty_result(self) -> bool:
        return len(self.results) == 0

    @results.setter
    def results(self, new_results):
        self.json_body["data"]["actor"]["account"]["nrql"]["results"] = new_results

    @property
    def metadata(self) -> dict:
        """
        Returns dict of metadata

        """
        if self.is_error:
            return {"metadata": "this is error result"}
        else:
            return self.json_body["data"]["actor"]["account"]["nrql"]["metadata"]

    @property
    def is_facet_query(self) -> bool:
        if self.is_error:
            return False
        else:
            return not (self.metadata["facets"] is None)

    def _raw_query_to_flat_format(self) -> tuple:
        headers = set()
        for row in self.results:
            for key in row.keys():
                headers.add(key)
        headers = tuple(headers)

        result_list = []
        for row in self.results:
            # clickhouse needs this format 2012-03-16 03:53:12
            row["timestamp"] = round(row["timestamp"] / 1000, 0)
            res = [row.get(h) for h in headers]

            result_list.append(tuple(res))

        return headers, result_list

    def _metric_query_to_flat_format(self) -> tuple:
        # sample data in self.results = {'beginTimeSeconds': 1613553420, 'endTimeSeconds': 1613553480, 'facet': ['hybris1p.komus.net', 'GC/ParNew'], 'hostmetricTimesliceName': ['hybris1p.komus.net', 'GC/ParNew'], 'average.newrelic.timeslice.value': 0.20255556040339998}
        headers = ('timestamp', 'host', 'metric_name', 'metric_value')
        result_list = []
        for row in self.results:
            result_list.append(tuple([row['beginTimeSeconds'], row['facet'][0],row['facet'][1],row['metric_value']]))
        return headers, result_list

    def to_flat_format(self) -> tuple:
        """
        Returns (headers,  list of tuples of data)

        """
        if self.is_error:
            return ("error",), (self.error_message,)
        elif self.is_empty_result:
            return (), []
        elif self.query_type == 'raw':
            return self._raw_query_to_flat_format()
        elif self.query_type == 'metric':
            return self._metric_query_to_flat_format()



