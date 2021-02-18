"""collection_client.py
============
The extended client module for collection campaigns.
"""

import os
import datetime
from random import random
import time
import uuid
import json
from uuid import uuid4
from io import IOBase
from tempfile import NamedTemporaryFile
from google.resumable_media.requests import ChunkedDownload
from google.resumable_media.common import InvalidResponse, DataCorruption
from typing import Any, Callable, Optional, Union, List, Dict, Tuple

from requests.adapters import prepend_scheme_if_needed

from .util import (
    requests_retry,
    raise_resp_exception_error,
    _is_one_gb_available,
    create_temp_directory,
    mark_temp_directory_complete,
    MAX_CHUNK_SIZE,
)
from .client import Client
from .dataset import LabeledDataset, LabeledFrame
from .inference import Inferences, InferencesFrame
from .sampling_agent import RandomSamplingAgent

from .embedding_distance_sampling import EmbeddingDistanceSamplingAgent


class CollectionClient(Client):
    """Client class that interacts with the Aquarium REST API.
    Also handles extra work around collecting samples for collection campigns

    Args:
        api_endpoint (str, optional): The API endpoint to hit. Defaults to "https://illume.aquariumlearning.com/api/v1".
    """

    def __init__(self, *args, **kwargs) -> "CollectionClient":
        super().__init__(*args, **kwargs)
        self.active_coll_camp_summaries = []

        self.sampling_agent = EmbeddingDistanceSamplingAgent
        self.camp_id_to_sample_agent = {}

        self.frame_batch_uuid_to_temp_file_path = {}
        self.frame_batch_uuid_to_camp_id_to_probability_score_info = {}

        self.temp_file_path = create_temp_directory()

    def _save_content_to_temp(
        self, file_name_prefix: str, writefunc: Callable, mode: str = "w"
    ) -> Optional[str]:
        """saves whatever the write function wants to a temp file and returns the file path

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush dataset to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=self.temp_file_path
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def write_to_file(self, frames: List[Dict[str, any]], filelike: IOBase) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in frames:
            filelike.write(json.dumps(frame) + "\n")

    def download_to_file(self, signed_url: str, filelike: IOBase) -> None:
        xml_api_headers = {
            "content-type": "application/octet-stream",
        }
        download = ChunkedDownload(signed_url, MAX_CHUNK_SIZE, filelike)
        while not download.finished:
            try:
                download.consume_next_chunk(requests_retry)
            except (InvalidResponse, DataCorruption, ConnectionError):
                if download.invalid:
                    continue
                continue

    def _read_rows_from_disk(self, file_path: str) -> List[Dict[str, Any]]:
        """reads temp files from disk and loads the dicts in them into memory

        Args:
            file_path (str): file path to read from

        Returns:
            List[Dict[str, Any]]: List of LabeledFrames in a dict structure
        """
        with open(file_path, "r") as frame_file:
            return [json.loads(line.strip()) for line in frame_file.readlines()]

    def _get_all_campaigns(self) -> List[Dict[str, Any]]:
        """Gets all collection campaign summaries

        Returns:
            List[Dict[str, Any]]: List of dicts containing collection campaign summaries
        """
        r = requests_retry.get(
            self.api_endpoint + "/collection_campaigns/summaries",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return r.json()

    def _post_collection_frames(self, collection_frames: Dict[str, Any]) -> None:
        """takes frames for collection and posts it to the API

        Args:
            collection_frames (Dict[str, Any]): Dict structure containing all the collected frames for a campaign to post
        """
        r = requests_retry.post(
            self.api_endpoint + "/projects/blah/collection_frames",
            headers=self._get_creds_headers(),
            json=collection_frames,
        )

        raise_resp_exception_error(r)

    def _is_postprocessing_complete(self, campaign_summary: Dict[str, Any]) -> bool:
        return campaign_summary.get("pca_signed_url") and campaign_summary.get(
            "microcluster_info_signed_url"
        )

    def sync_state(self) -> None:
        """Downloads all collection campaigns and preps sampler with sample frames"""
        print("Starting Sync")
        all_coll_camps = self._get_all_campaigns()

        # Skip over collection campaigns that still need to be post-processed
        processing_coll_camps_issue_uuids = [
            c.get("issue_uuid")
            for c in all_coll_camps
            if c["active"] and not self._is_postprocessing_complete(c)
        ]
        if len(processing_coll_camps_issue_uuids) > 0:
            print(
                f"{len(processing_coll_camps_issue_uuids)} collection campaigns still awaiting postprocessing."
            )
            for issue_uuid in processing_coll_camps_issue_uuids:
                print(f" - issue uuid: {issue_uuid}")

        self.active_coll_camp_summaries = [
            c
            for c in all_coll_camps
            if c["active"] and self._is_postprocessing_complete(c)
        ]
        print(
            f"Found {len(self.active_coll_camp_summaries)} Active Collection Campaigns"
        )

        # Initialize a sampling agent per active, postprocessed campaign
        self.camp_id_to_sample_agent = {
            c["id"]: self.sampling_agent() for c in self.active_coll_camp_summaries
        }

        print(f"Downloading assets for each Collection Campaign")
        for campaign in self.active_coll_camp_summaries:
            # download each of the preprocessed files for the example dataset locally
            signed_urls = {
                "pca_signed_url": campaign.get("pca_signed_url"),
                "microcluster_info_signed_url": campaign.get(
                    "microcluster_info_signed_url"
                ),
            }

            url_key_to_downloaded_file_path = {}
            for url_key, signed_url in signed_urls.items():
                if signed_url is None:
                    url_key_to_downloaded_file_path[url_key] = None
                    continue
                current_time = datetime.datetime.now()
                random_uuid = uuid4().hex
                temp_file_prefix = "al_{}_{}_{}_{}".format(
                    current_time.strftime("%Y%m%d_%H%M%S_%f"),
                    str(campaign.get("id")),
                    url_key,
                    random_uuid,
                )
                file_path = self._save_content_to_temp(
                    temp_file_prefix,
                    lambda x: self.download_to_file(signed_url, x),
                    mode="wb",
                )
                url_key_to_downloaded_file_path[url_key] = file_path

            path_key_to_downloaded_file_path = {
                k[:-10] + "path": v for k, v in url_key_to_downloaded_file_path.items()
            }

            # Load data into agent for each campaign
            agent = self.camp_id_to_sample_agent[campaign.get("id")]
            agent.load_sampling_dataset(
                element_type=campaign.get("element_type"),
                preprocessed_info=path_key_to_downloaded_file_path,
            )

    def sample_probabilities(self, frames: List[LabeledFrame]) -> None:
        """Takes a list of Labeled Frames and stores scores for each based on each synced collection campaigns

        Args:
            frames (List[LabeledFrame]): a List of Labeled frames to score based on synced Collection Campaigns
        """
        batch_uuid = uuid4().hex

        self.frame_batch_uuid_to_camp_id_to_probability_score_info[batch_uuid] = {
            campaign["id"]: [
                # A dict with fields (similarity_score, similarity_score_version, sampled_element_id)
                self.camp_id_to_sample_agent[campaign["id"]].score_frame(frame)
                for frame in frames
            ]
            for campaign in self.active_coll_camp_summaries
        }
        current_time = datetime.datetime.now()
        temp_frame_prefix = "al_{}_collection_campaign_candidate_frames_{}_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f"), batch_uuid
        )
        frame_path = self._save_content_to_temp(
            temp_frame_prefix,
            lambda x: self.write_to_file([frame.to_dict() for frame in frames], x),
        )
        self.frame_batch_uuid_to_temp_file_path[batch_uuid] = frame_path
        return self.frame_batch_uuid_to_camp_id_to_probability_score_info[batch_uuid]

    def save_for_collection(self, score_threshold: float = 0.5) -> None:
        """Based on the score threshold, take all sampled frames and upload those that score above
        the score threshold for each Collection Campaign.

        Args:
            score_threshold (float, optional): Score threshold for all campaigns to save to server. Defaults to 0.7.
        """
        for frame_batch_uuid in self.frame_batch_uuid_to_temp_file_path.keys():
            frames = self._read_rows_from_disk(
                self.frame_batch_uuid_to_temp_file_path[frame_batch_uuid]
            )
            camp_id_to_probability_score_info = (
                self.frame_batch_uuid_to_camp_id_to_probability_score_info[
                    frame_batch_uuid
                ]
            )
            for campaign in self.active_coll_camp_summaries:
                scores = camp_id_to_probability_score_info[campaign["id"]]
                filtered_frame_indexes_and_scores = filter(
                    lambda score: score[1].get("similarity_score") >= score_threshold,
                    enumerate(scores),
                )
                filtered_frame_indexes = map(
                    lambda score: score[0], filtered_frame_indexes_and_scores
                )
                filtered_frames_dict = []
                for idx in filtered_frame_indexes:
                    frame_dict = frames[idx]
                    frame_dict["similarity_score"] = scores[idx].get("similarity_score")
                    frame_dict["sampled_element_id"] = scores[idx].get(
                        "sampled_element_id"
                    )
                    frame_dict["similarity_score_version"] = scores[idx].get(
                        "similarity_score_version"
                    )
                    filtered_frames_dict.append(frame_dict)

                if len(filtered_frames_dict) == 0:
                    continue

                print(f"Uploading Frames for Collection Campaign ID {campaign['id']}")

                payload = {
                    "collection_campaign_id": campaign["id"],
                    "issue_uuid": campaign["issue_uuid"],
                    "dataframes": filtered_frames_dict,
                }
                self._post_collection_frames(payload)

        mark_temp_directory_complete(self.temp_file_path)
