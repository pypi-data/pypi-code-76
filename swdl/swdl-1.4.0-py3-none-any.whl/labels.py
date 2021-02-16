import json
import time
from base64 import b64encode, b64decode
from datetime import datetime
from multiprocessing import Queue, Process, Value
from typing import Optional, Tuple, Iterable

import h5py as h5
import numpy as np
import requests
from google.api_core.exceptions import NotFound, TooManyRequests
from google.cloud import storage

import asyncio
import aiohttp

import logging

logger = logging.getLogger(__name__)

CP_FRAMERATE = 25
CP_DIM = 4
CP_INTERVAL = 10


class CameraPositionError(Exception):
    pass


class InvalidCameraPositionError(CameraPositionError):
    pass


def round_timestamps(array: np.ndarray):
    if array is None:
        return None
    output = np.zeros([CP_FRAMERATE * CP_INTERVAL, CP_DIM], np.float32)
    rounded_ts = np.round(array[:, 0] * CP_FRAMERATE) / CP_FRAMERATE
    array_index = np.round((rounded_ts % CP_INTERVAL) * CP_FRAMERATE).astype(int)
    array_index[array[:, 0] == 0] = -1
    for i, ts in enumerate(array_index):
        if ts == -1:
            continue
        output[ts] = array[i]
        output[ts, 0] = round(output[ts, 0] * CP_FRAMERATE) / CP_FRAMERATE
    return output


def merge_arrays(old: np.ndarray, new: np.ndarray) -> np.ndarray:
    if old is None:
        return new
    for i, item in enumerate(new):
        if item[0] != 0:
            old[i] = item
    return old


def get_segment_indeces(np_data):
    rounded_ts = np.round(np_data[:, 0] * CP_FRAMERATE) / CP_FRAMERATE
    time_indexes = (rounded_ts // CP_INTERVAL).astype(int)
    return time_indexes


class CPManager:
    """Tool to savely push camera positions to a cloud bucket"""

    def __init__(self, bucket_name):
        """
        Args:
            bucket_name: The bucket name
        """
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def _get_manifest(self, match_id: str, virtual_cam_id: int):
        manifest_path = f"{match_id}/camera_positions/{virtual_cam_id}/cp.json"
        blob = self.bucket.blob(manifest_path)
        try:
            manifest_string = blob.download_as_string()
        except NotFound:
            manifest_string = None
        if not manifest_string:
            return None
        try:
            return json.loads(manifest_string)
        except json.JSONDecodeError:
            return None

    def _upload_manifest(self, manifest: dict, match_id: str, virtual_cam_id: int):
        for i in range(5):
            try:
                manifest_path = f"{match_id}/camera_positions/{virtual_cam_id}/cp.json"
                blob = self.bucket.blob(manifest_path)
                blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
                blob.upload_from_string(json.dumps(manifest))
                break
            except TooManyRequests:
                pass

    def _upload_segment(
        self, data: bytes, match_id: str, virtual_camera_id: int, time_id: int
    ):

        upload_path = f"{match_id}/camera_positions/{virtual_camera_id}/{time_id}.cp"
        for i in range(5):
            try:
                blob = self.bucket.blob(upload_path)
                blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
                blob.upload_from_string(data)
                break
            except TooManyRequests:
                pass

    def upload_data(self, cam_data: bytes, match_id: str, virtual_cam_id: int):
        """Push the camera positions to the bucket
        Args:
            cam_data: The camera positions. Must be a base64 encoded float32 array
            match_id: The camera id
            virtual_cam_id: The virtual camera id

        """

        try:
            np_data = np.frombuffer(b64decode(cam_data), np.float32).reshape(-1, CP_DIM)
        except ValueError:
            raise InvalidCameraPositionError(
                f"The provided data data seems not to contain valid camera positions. "
                f"Make sure your data array is of shape (None, {CP_DIM}), 32bit float "
                f"and is base64 encoded."
            )
        time_indexes = get_segment_indeces(np_data)
        time_idx_set = list(set(time_indexes))
        for time_id in sorted(time_idx_set):
            data = np_data[time_indexes == time_id]

            upload_path = f"{match_id}/camera_positions/{virtual_cam_id}/{time_id}.cp"
            blob = self.bucket.blob(upload_path)
            try:
                existing_data = blob.download_as_string()
                existing_data = np.frombuffer(
                    b64decode(existing_data), np.float32
                ).reshape([-1, CP_DIM])
            except (NotFound, ValueError):
                existing_data = None

            data = round_timestamps(data)
            existing_data = round_timestamps(existing_data)
            data = merge_arrays(existing_data, data)
            cam_data = b64encode(data.tobytes())
            self._upload_segment(cam_data, match_id, virtual_cam_id, time_id)

        new_max = int(max(time_idx_set))
        manifest = self._get_manifest(match_id, virtual_cam_id)
        if manifest:
            if "max_index" in manifest:
                old_max = manifest["max_index"]
                if new_max <= old_max:
                    return

        manifest = {
            "max_index": new_max,
            "framerate": CP_FRAMERATE,
            "interval": CP_INTERVAL,
            "dimensions": CP_DIM,
        }
        self._upload_manifest(manifest, match_id, virtual_cam_id)


class Label:
    """
    Structure to store label data, just wraping numpy arrays
    """

    def __init__(self):
        self.positions_dim = 4
        self.events = np.zeros((0, 3), dtype=np.uint32)
        self.status = np.zeros((11,), dtype=np.uint32)
        self.positions = np.zeros((0, self.positions_dim), dtype=np.float32)
        self.player_positions = {0: np.zeros((25, 3), dtype=np.float32)}
        self.label_resolution = 40

    @classmethod
    def from_file(cls, path="labels.h5"):
        """
        Reads from hdf5 file

        # Attributes
        path(str):
        """
        file = h5.File(path, "r")
        label = cls()
        label.positions = file["labels"][:]
        label.events = file["events"][:]
        label.status = file["status"][:]
        file.close()
        return label

    def save(self, path="labels.h5"):
        """
        Saves label to hdf5

        # Attributes
        path(str):
        """
        file = h5.File(path, "w")
        file["events"] = self.events
        file["labels"] = self.positions
        file["status"] = self.status
        file.close()

    def set_position(self, timestamp, pos: np.ndarray):
        """
        Adds a position to the given timestamp

        # Arguments:
        timestamp (int): video time in ms
        target_position (array): x, y and z where the camera should look at
        actual_position (array): x, y and z where the camera actually looking
        at
        """
        row = int(timestamp / self.label_resolution)
        if self.positions.shape[0] < row + 1:
            self.positions.resize((row + 1, self.positions_dim), refcheck=False)
        item = [row * self.label_resolution, pos[0], pos[1], pos[2]]
        self.positions[row] = item


class CPUploader:
    """Tool to push camera positions to the camera position service"""

    def __init__(self, match_id: str, virtual_camera_id: int, auth: Tuple[str, str]):
        """
        Args:
            match_id: The match id
            virtual_camera_id: The virtual camera id
            auth: The authentication. (username, password)
        """
        self.match_id = match_id
        self.virtual_camera_id = virtual_camera_id
        self.label_resolution = 40
        self._position_queue = Queue()
        self._process = Process(target=self._upload_loop, args=(self._position_queue,))
        self.cp_url = (
            "https://europe-west1-sw-sc-de-prod.cloudfunctions.net/"
            "api-camera-positions"
        )
        self.auth = auth
        self._upload_batch = 1000 / self.label_resolution * 10
        self._future = None

    def start(self):
        if not self._process.is_alive():
            self._process.start()

    def stop(self):
        if self._process.is_alive():
            self._position_queue.put(None)
            self._process.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _upload_loop(self, queue: Queue):
        items = []
        while True:
            item = queue.get()
            if item is None:
                self._upload_positions(items)
                break
            items.append(item)
            if len(items) >= self._upload_batch:
                self._upload_positions(items)
                items = []

    def _upload_positions(self, items):
        if not items:
            return
        data = b64encode(np.stack(items).tobytes())

        body = {
            "match_id": self.match_id,
            "vci": self.virtual_camera_id,
            "data": data,
        }

        requests.post(self.cp_url, json=body, auth=self.auth)

    def push_position(self, timestamp: float, pos: np.ndarray):
        """Push one position
        Args:
            timestamp: timestamp of the position in seconds
            pos: [x,y,zoom]

        """

        row = round(timestamp * (1000 / self.label_resolution))
        item = np.array(
            [row * self.label_resolution / 1000, pos[0], pos[1], pos[2]], np.float32
        )
        self._position_queue.put(item)


class CPDownloader:
    """
    Tool to download or stream camera positions

    """

    def __init__(self, match_id: str, virtual_camera_id: int):
        """
        Args:
            match_id: The match id
            virtual_camera_id: The virtual camera id
        """
        self.match_id = match_id
        self.virtual_camera_id = virtual_camera_id
        self._result_queue = Queue()
        self._cp_base_link = (
            f"https://storage.googleapis.com/sw-sc-de-shared/"
            f"{self.match_id}/camera_positions/{self.virtual_camera_id}/"
        )
        self._prefetched_segments = {}

        self._latest_segment = self._get_lastest_segment()
        self._latest_segment_on_timeout = self._latest_segment

        self._process = Process(target=self._loop, args=(self._result_queue,))
        self.stop_flag = Value("b", False)

    def start(self):
        if not self._process.is_alive():
            self.stop_flag.value = False
            self._process.start()

    def stop(self):
        if self._process.is_alive():
            self.stop_flag.value = True
            self._process.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def download_all(self) -> np.ndarray:
        """Downloads all camera positions

        Returns: All positions in an [nx4] array

        """
        num_segments = self._get_lastest_segment() + 1

        segments = self._get_segments(range(num_segments))
        data = np.zeros([num_segments * CP_INTERVAL * CP_FRAMERATE, CP_DIM], np.float32)
        for index, segment in enumerate(segments):
            if segment is None:
                continue
            start = index * CP_FRAMERATE * CP_INTERVAL
            end = start + CP_FRAMERATE * CP_INTERVAL
            data[start:end] = segment
        return data

    def _get_manifest(self):
        data = requests.get(self._cp_base_link + "cp.json")
        if data.status_code == 200:
            return data.json()

    async def _get_segment(self, segment, session: aiohttp.ClientSession):
        async with session.get(self._cp_base_link + f"{segment}.cp") as data:
            if data.status == 200:
                text = await data.text()
                return np.frombuffer(b64decode(text), np.float32).reshape((-1, 4))

    def _get_segments(self, segment_indexes: Iterable):
        loop = asyncio.new_event_loop()

        async def pull():
            async with aiohttp.ClientSession() as session:
                tasks = [self._get_segment(s, session) for s in segment_indexes]

                result = await asyncio.gather(*tasks)
                return result

        segments = loop.run_until_complete(pull())
        return segments

    def _loop(self, result_queue: Queue):
        segment_id = 0
        while not self.stop_flag.value:
            latest_segment = self._get_lastest_segment()
            segments = self._get_segments(range(segment_id, latest_segment))
            for i, s in enumerate(segments):
                result_queue.put([segment_id + i, s])
            segment_id = latest_segment
            time.sleep(5)

    def _process_result_queue(self):
        while not self._result_queue.empty():
            i, segment = self._result_queue.get()
            self._prefetched_segments[i] = segment
            if i > self._latest_segment:
                self._latest_segment = i

    @staticmethod
    def _get_rounded_cam_pos(timestamp: float, segment: np.ndarray) -> np.ndarray:
        row = round(timestamp % CP_INTERVAL * CP_FRAMERATE)
        return segment[row]

    def _get_lastest_segment(self):
        manifest = self._get_manifest()
        total_segments = -1
        if manifest and "max_index" in manifest:
            total_segments = manifest["max_index"]
        return total_segments

    def get_position(
        self, timestamp: float, timeout: float = 0.0
    ) -> Optional[np.ndarray]:
        """Returns the position to the given timestamp

        Downloads the given position from the cloud and prefetches the next positions.
        If you want to random access the positions consider to usw download_all.
        Waits for a certain position if a timeout is given, only if an upload
        activity is recognized.

        Args:
            timestamp: The timestamp of the desired psition.
            timeout: The timeout in seconds to wait for a camera positions if currently
            not available.

        Returns: The position [x,y,zoom]

        """
        if not self._process.is_alive():
            raise RuntimeError(
                "You need to call start() before you can fetch positions"
            )
        timestamp = round(timestamp * CP_FRAMERATE) / CP_FRAMERATE
        segment_id = timestamp // CP_INTERVAL
        start_time = actual_time = 0
        while actual_time - start_time <= timeout:
            self._process_result_queue()
            if segment_id in self._prefetched_segments:
                segment = self._prefetched_segments[segment_id]
                if segment is not None:
                    poi = self._get_rounded_cam_pos(timestamp, segment)
                    if poi[0] != 0:
                        return poi[1:]
                return
            if segment_id - self._latest_segment > timeout / CP_INTERVAL:
                return
            if self._latest_segment_on_timeout == self._latest_segment:
                return
            actual_time = datetime.now().timestamp()
            if start_time == 0:
                start_time = actual_time
            diff = actual_time - start_time
            logger.warning(f"Waiting for position {diff}/{timeout}")
            time.sleep(5)
        self._latest_segment_on_timeout = self._latest_segment

        return
