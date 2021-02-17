import collections

import pandas as pd
from dataclasses import asdict

from qalx_orcaflex.data_models import (
    TimeHistory,
    TimeHistorySummary,
    RangeGraph,
    RangeGraphSummary,
    OrcaFlexJobState,
    LoadCaseInfo,
)


def max_min_df(df):
    df_max = df.max().max()
    df_idxmax = df.max().idxmax()
    ind_max = df[df_idxmax].idxmax()
    df_min = df.min().min()
    df_idxmin = df.min().idxmin()
    ind_min = df[df_idxmin].idxmin()
    return df_idxmax, df_idxmin, df_max, df_min, ind_max, ind_min


def to_df(res_series) -> pd.DataFrame:
    data = [_[2] for _ in res_series]
    ix = [(_[0], _[1]) for _ in res_series]
    df = pd.DataFrame(data, ix)
    return df


class Summary:
    def __init__(self):
        self.info_v_results = collections.defaultdict(
            lambda: collections.defaultdict(
                lambda: pd.DataFrame(columns=["max", "min"])
            )
        )
        self.result_meta = {}
        self.summary = {}

    def _info_dict(self):
        self._clean_info_v_results = {}
        for res, info in self.info_v_results.items():
            self._clean_info_v_results[res] = {}
            for info_key, df in info.items():
                self._clean_info_v_results[res][info_key] = df.to_dict("split")

    def _extract_meta(self, key) -> dict:
        meta = self.result_meta[key]
        res_name = meta.name
        res_stat = meta.stat
        max_limit = meta.limit.get("max")
        min_limit = meta.limit.get("min")
        full_name = meta.var_details.get("full_name")
        units = meta.var_details.get("units")
        return {
            "result_key": key,
            "stat": res_stat,
            "units": units,
            "short_name": res_name,
            "full_name": full_name,
            "limits": {"max": max_limit, "min": min_limit},
        }


class THSummary(Summary):
    def __init__(self):
        super().__init__()
        self.summary_data = collections.defaultdict(list)

    def process_result(self, result_key, task, result_item, load_case_info):
        r = TimeHistory.from_dict(result_item["data"])
        if r.extracted:
            series_th = pd.Series(
                r.extracted.y_values + [r.extracted.static_value],
                r.extracted.time + ["static"],
            )
            self.summary_data[result_key].append((task, result_item.guid, series_th))
            th_max = series_th.max()
            th_min = series_th.min()

            for info in load_case_info:
                self.info_v_results[result_key][info.key].loc[
                    info.value, "max"
                ] = th_max
                self.info_v_results[result_key][info.key].loc[
                    info.value, "min"
                ] = th_min
        self.result_meta[result_key] = r.meta
        return r

    def aggregate(self, case_data):
        for key, data in self.summary_data.items():
            df = to_df(data)
            (
                t_max_value,
                t_min_value,
                max_value,
                min_value,
                ind_max,
                ind_min,
            ) = max_min_df(df)
            max_case, max_result_guid = ind_max
            min_case, min_result_guid = ind_min
            max_case_info = case_data[max_case].to_dict()
            min_case_info = case_data[min_case].to_dict()
            self.summary[key] = asdict(
                TimeHistorySummary(
                    result_meta=self._extract_meta(key),
                    max_value=max_value,
                    time_max_value=t_max_value,
                    max_case_info=max_case_info,
                    max_result_guid=max_result_guid,
                    min_value=min_value,
                    time_min_value=t_min_value,
                    min_case_info=min_case_info,
                    min_result_guid=min_result_guid,
                    vs_info=self._clean_info_v_results.get(key, {}),
                )
            )


class RGSummary(Summary):
    def __init__(self):
        super().__init__()
        self.summary_data = collections.defaultdict(
            lambda: {"max": [], "min": [], "static": []}
        )

    def process_result(self, result_key, task, result_item, load_case_info):
        r = RangeGraph.from_dict(result_item["data"])
        if r.extracted:
            series_rg_max = pd.Series(r.extracted.y_max, r.extracted.arc)
            self.summary_data[result_key]["max"].append(
                (task, result_item.guid, series_rg_max)
            )
            rg_max = series_rg_max.max()

            series_rg_min = pd.Series(r.extracted.y_min, r.extracted.arc)
            self.summary_data[result_key]["min"].append(
                (task, result_item.guid, series_rg_min)
            )
            rg_min = series_rg_min.min()

            for info in load_case_info:
                self.info_v_results[result_key][info.key].loc[
                    info.value, "max"
                ] = rg_max
                self.info_v_results[result_key][info.key].loc[
                    info.value, "min"
                ] = rg_min

            series_rg_static = pd.Series(r.extracted.y_static, r.extracted.arc)
            self.summary_data[result_key]["static"].append(
                (task, result_item.guid, series_rg_static)
            )
        self.result_meta[result_key] = r.meta
        return r

    def aggregate(self, case_data):
        for key, data in self.summary_data.items():
            df_max = to_df(data["max"])
            max_value = df_max.max().max()
            arc_max_value = df_max.max().idxmax()
            max_case_name, max_result_guid = df_max[arc_max_value].idxmax()
            max_case_info = case_data[max_case_name].to_dict()

            df_min = to_df(data["min"])
            min_value = df_min.min().min()
            arc_min_value = df_min.min().idxmin()
            min_case_name, min_result_guid = df_min[arc_min_value].idxmin()
            min_case_info = case_data[min_case_name].to_dict()

            df_static = to_df(data["static"])
            (
                static_arc_max,
                static_arc_min,
                static_max_value,
                static_min_value,
                ind_max,
                ind_min,
            ) = max_min_df(df_static)
            static_max_case, static_max_result_guid = ind_max
            static_min_case, static_min_result_guid = ind_min
            static_max_case_info = case_data[static_max_case].to_dict()
            static_min_case_info = case_data[static_min_case].to_dict()
            self.summary[key] = asdict(
                RangeGraphSummary(
                    result_meta=self._extract_meta(key),
                    max_value=max_value,
                    arc_max_value=arc_max_value,
                    max_case_info=max_case_info,
                    max_result_guid=max_result_guid,
                    min_value=min_value,
                    arc_min_value=arc_min_value,
                    min_case_info=min_case_info,
                    min_result_guid=min_result_guid,
                    static_max_value=static_max_value,
                    arc_static_max_value=static_arc_max,
                    static_max_case_info=static_max_case_info,
                    static_max_result_guid=static_max_result_guid,
                    static_min_value=static_min_value,
                    arc_static_min_value=static_arc_min,
                    static_min_case_info=static_min_case_info,
                    static_min_result_guid=static_min_result_guid,
                    vs_info=self._clean_info_v_results.get(key, {}),
                )
            )


class ResultsSummariser:
    def __init__(self, job):
        self.job = job
        self.case_data = {}

        self.th_summary = THSummary()
        self.rg_summary = RGSummary()

    def summarise_batch(self, batch):
        for task, case_set in batch.items():
            state = OrcaFlexJobState(**case_set["meta"].get("state", {}))
            lci = LoadCaseInfo.from_dict(case_set.get_item_data("load_case_info"))
            lci_values = [state.state, case_set["guid"]] + [i.value for i in lci]
            lci_keys = ["state", "case_guid"] + [i.key for i in lci]
            self.case_data[task] = pd.Series(lci_values, lci_keys)
            result_items = case_set.get_item_data("results")
            if result_items:
                for result_key, guid in result_items.items():
                    result_item = self.job.session.item.get(guid=guid)
                    if result_item["data"]["_type"] == "th":
                        self.th_summary.process_result(
                            result_key, task, result_item, lci
                        )
                    else:
                        self.rg_summary.process_result(
                            result_key, task, result_item, lci
                        )
        self._aggregate_results()
        self._save_summary()

    def _aggregate_results(self):
        self.th_summary._info_dict()
        self.rg_summary._info_dict()
        self.th_summary.aggregate(self.case_data)
        self.rg_summary.aggregate(self.case_data)

    def _save_summary(self):
        summary_item = self.job.session.item.add(
            data={
                "Time Histories": self.th_summary.summary,
                "Range Graphs": self.rg_summary.summary,
            },
            meta={
                "_class": "orcaflex.results.summary",
                "batch_guid": self.job.e["guid"],
            },
        )
        self.job.session.item.save(summary_item)
        self.job.entity["meta"]["results_summary"] = summary_item["guid"]
        self.job.log.debug(f"Saved summary results with guid: {summary_item['guid']}")
