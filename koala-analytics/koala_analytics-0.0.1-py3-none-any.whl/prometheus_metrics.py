import requests
import datetime


from koala_analytics.base_metrics import BaseMetrics


class PrometheusMetrics(BaseMetrics):

    def __init__(self, api_url: str, metric_names: list, table_id: str, credential_dict: dict):
        super().__init__(credential_dict)
        self._table_id = table_id
        self._metric_names = metric_names
        self._api_url = api_url

    def get_metrics(self):
        latest_timestamp = self._get_latest_timestamp()
        start, end = self._get_times(latest_timestamp)

        start_dt = datetime.datetime.fromtimestamp(start).strftime("%d-%m-%Y %H:%M:%S")
        end_dt = datetime.datetime.fromtimestamp(end).strftime("%d-%m-%Y %H:%M:%S")

        formatted_data = []

        self._logger.info(f"Fetching prometheus metrics from {start_dt} to {end_dt}\n")

        for metric in self._metric_names:
            self._logger.info(f"* Fetching prometheus metric {metric} *")

            raw_data = self._get_data(metric_name=metric,
                                      start=start,
                                      end=end)

            data = self._format_metric_data(raw_data)
            self._logger.info(f"    Fetched {len(data)} rows.")
            formatted_data.extend(data)

        self._logger.info(f"\n** Fetched {len(formatted_data)} rows in total **")
        return formatted_data

    def _get_data(self, metric_name: str, start: int, end: int, step: int = 60) -> dict:
        response = requests.get(self._api_url, params={"query": metric_name,
                                                       "start": start,
                                                       "end": end,
                                                       "step": step})
        response.raise_for_status()
        return response.json()

    def _get_latest_timestamp(self) -> int:
        now = datetime.datetime.now()
        today_midnight = int(datetime.datetime(year=now.year,
                                               month=now.month,
                                               day=now.day,
                                               hour=0,
                                               minute=0).timestamp())

        bq_query = f"select max(timestamp) as latest_timestamp from {self._table_id}"
        latest_timestamp_result = self.execute_bq_query(query=bq_query)[0]["latest_timestamp"]

        if latest_timestamp_result is None:
            return today_midnight
        else:
            return latest_timestamp_result

    @staticmethod
    def _get_times(timestamp: int) -> tuple:
        start = timestamp + 60
        end = int(datetime.datetime.now().timestamp())
        return start, end

    @staticmethod
    def _format_metric_data(data: dict) -> list:
        formatted_data = []

        metric_name = data["data"]["result"][0]["metric"]["__name__"]
        raw_data = data["data"]["result"]
        for result in raw_data:
            for row in result["values"]:
                formatted_data.append({"timestamp": row[0],
                                       "metric": metric_name,
                                       "value": row[1]})
        return formatted_data
