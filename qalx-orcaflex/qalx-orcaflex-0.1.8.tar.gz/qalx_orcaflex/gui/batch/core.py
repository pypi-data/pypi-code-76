import os
import warnings
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
from pyqalx import Set

from qalx_orcaflex.data_models import JobState
from qalx_orcaflex.helpers import nice_time

# These two warnings can be suppressed. We might have all NaN in the
# remaining time array for the "Running Dynamics" state
warnings.filterwarnings("ignore", r"All-NaN (slice|axis) encountered")
warnings.filterwarnings("ignore", "Mean of empty slice")


def pretty_time(time):
    """Show the time in the tables in pretty form"""
    if time is None or np.isnan(time):
        return "N/A"
    return nice_time(time) or "\u221E"  # infinity symbol


def date_format(date):
    return date.strftime("%Y/%m/%d-%H:%M:%S")


@dataclass
class BatchTuple:
    """Simple data class that bundles batch guid and created on attributes"""

    guid: str = None
    created_on: datetime = None


class BatchOverview:
    """Class that provides all the functionality to get batch summary data"""

    df_columns = ["case", "state", "remaining", "updated", "complete"]
    possible_states = [_.value for _ in JobState]
    warn_for_requeue = {
        JobState.PROCESSING.value,
        JobState.RUNNING_STATICS.value,
        JobState.QUEUED.value,
        JobState.LOADING_MODEL_DATA.value,
        JobState.PRE_PROCESSING.value,
        JobState.RUNNING_DYNAMICS.value,
    }

    def __init__(self, session, batch_name, batches):
        self.session = session
        # optimum ratio between number of queries and URI length for array of
        # guid's that is passed to match sets and items
        self.query_limit = 110
        self.batch_name = batch_name
        self.batches = batches

    @classmethod
    def get_batches(cls, session, batch_name):
        """Get the batch group. We do not need it unpacked"""
        result = session.group.find(
            query={
                "metadata.data.name": batch_name,
                "metadata.data._class": "orcaflex.batch",
            },
            child_fields=["meta"],
            unpack=False,
        )
        batches = result["data"]
        if not batches:
            raise ValueError(f'No batches with name "{batch_name}" found.')
        batches.sort(key=lambda x: x["info"]["created"]["on"])
        return [BatchTuple(str(b["guid"]), b["info"]["created"]["on"]) for b in batches]

    @staticmethod
    def get_summary_stats(remaining_array):
        """Helper to get the summary statistics for the remaining time"""
        try:
            rem_max = np.nanmax(remaining_array)
            rem_mean = np.nanmean(remaining_array)
            rem_q1 = np.nanquantile(remaining_array, 0.25)
            rem_q3 = np.nanquantile(remaining_array, 0.75)
        # We are getting statistics ignoring nans for an array that can be empty
        # or full of nans. Need to catch ValueError and TypeError respectively
        except (ValueError, TypeError):
            rem_max = rem_mean = rem_q1 = rem_q3 = np.nan
        return rem_max, rem_mean, rem_q1, rem_q3

    def get_batch(self, guid, child_fields=None, unpack=False):
        if child_fields is None:
            child_fields = ["meta"]
        return self.session.group.get(guid, child_fields=child_fields, unpack=unpack)

    def get_existing_sim_queue(self, guid):
        return self.session.group.get(guid)["meta"]["options"]["sim_queue"]

    def get_progress_items_dict(self, item_guids):
        """Get a map of <progress_item_guid>: <time_to_go>"""
        items, start = [], 0
        for _ in range(int(np.ceil(len(item_guids) / self.query_limit))):
            result = self.session.item.find(
                query={
                    "guid": {"$in": item_guids[start : start + self.query_limit]},
                    "metadata.data._class": "orcaflex.job.progress",
                },
                fields=["data.time_to_go"],
                limit=self.query_limit,
            )
            start += self.query_limit
            items += result["data"]
        return {item["guid"]: item["data"]["time_to_go"] for item in items}

    def get_summary_df(self, batch_index):
        """
        Populate the summary dataframe from the jobs meta and progress data
        """
        batch = self.get_batch(self.batches[batch_index].guid)
        set_guids = [_ for _ in batch["sets"].values()]
        jobs, start = [], 0
        for _ in range(int(np.ceil(len(set_guids) / self.query_limit))):
            result = self.session.set.find(
                query={
                    "guid": {"$in": set_guids[start : start + self.query_limit]},
                    "metadata.data._class": "orcaflex.job",
                },
                fields=[
                    "meta.case_name",
                    "meta.processing_complete",
                    "meta.state.state",
                    "items.progress",
                ],
                unpack=False,
                limit=self.query_limit,
            )
            start += self.query_limit
            jobs += result["data"]
        progress_item_guids = [_["items"]["progress"] for _ in jobs]
        progress_map = self.get_progress_items_dict(progress_item_guids)
        data = []
        for q_set in jobs:
            data_row = [
                q_set["meta"]["case_name"],
                q_set["meta"]["state"]["state"],
                progress_map[q_set["items"]["progress"]],
                date_format(datetime.now()),
                (q_set["meta"]["processing_complete"] or False),
            ]
            data.append(data_row)
        df = pd.DataFrame(data, columns=self.df_columns)
        # Remaining time value is valid only if the state is running dynamics
        df.loc[df["state"] != "Running dynamics", "remaining"] = np.nan
        df["remaining"].fillna(value=np.nan, inplace=True)
        return df, batch_index

    def download_files(self, batch_ind, file_type, jobs, file_name, save_path):
        """Helper to download files from the provided jobs"""
        batch = self.get_batch(self.batches[batch_ind].guid, unpack=False)
        for job in jobs:
            job_set = self.session.set.get(batch["sets"][job], unpack=False)
            if file_type == "sim":
                file_guid = job_set["items"]["simulation_file"]
            else:  # data file
                file_guid = job_set["items"]["data_file"]
            file_item = self.session.item.get(file_guid)
            # If the full path is provided, the save path is inferred from it
            if save_path is None:
                save_path = os.path.dirname(file_name)
                file_name = os.path.basename(file_name)
            # Full save path is None, so the file name is taken from the item
            else:
                file_name = file_item["file"]["name"]
            file_item.save_file_to_disk(filepath=save_path, filename=file_name)

    def requeue_jobs(self, batch_ind, jobs, queue_name):
        """Requeue jobs. Gets or creates the queue from the provided name"""
        # Error as early as possible for non-existing queue
        queue = self.session.queue.get_by_name(queue_name)
        batch = self.get_batch(self.batches[batch_ind].guid, unpack=False)
        for job in jobs:
            job_set = self.session.set.get(batch["sets"][job], unpack=False)
            job_set["meta"]["state"]["state"] = "Queued"
            job_set["meta"]["processing_complete"] = False
            self.session.set.save(job_set)
            Set.add_to_queue(job_set, queue=queue)
