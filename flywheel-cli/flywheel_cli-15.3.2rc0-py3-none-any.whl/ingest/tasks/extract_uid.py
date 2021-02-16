"""Provides ExtractUIDTask class"""

import logging
import typing as t
from uuid import UUID

import fs.path
from flywheel_migration.dcm import DicomFile
from pydantic import ValidationError
from pydicom.tag import Tag

from ... import util
from .. import detect_duplicates, errors
from .. import schemas as s
from ..scanners import dicom
from .abstract import Task

log = logging.getLogger(__name__)

# Specifying just the list of tags we're interested in speeds up dicom scanning
DICOM_TAGS = [
    "SeriesInstanceUID",
    "StudyInstanceUID",
    "SOPInstanceUID",
    "AcquisitionNumber",
]


class ExtractUIDTask(Task):
    """Extract metadata from the files for a given ingest item.

    Supported metadata:
      - DICOM UIDs (StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_uids = self.db.batch_writer_insert_uid()
        self.update_items = self.db.batch_writer_update_item()
        self.insert_errors = self.db.batch_writer_insert_error()

    def _run(self):
        # pylint: disable=R0912
        item = self.db.get_item(self.task.item_id)
        buffer_size = self.worker_config.buffer_size

        dicom_paths = []
        for filepath in item.files:
            if util.is_dicom_file(filepath):
                dicom_paths.append(filepath)

        if len(dicom_paths) == 0:
            # no dicom files found
            return

        tags = [Tag(keyword) for keyword in DICOM_TAGS]

        uids = []
        for filepath in dicom_paths:
            with self.walker.open(
                fs.path.combine(item.dir, filepath), "rb", buffering=buffer_size
            ) as fileobj:
                result = self._scan_dicom_file(fileobj, tags, filepath, item.id)
                if isinstance(result, s.UIDIn):
                    self.insert_uids.push(result.dict(exclude_none=True))
                    uids.append(result)

                    if item.context.session and not item.context.session.uid:
                        item.context.session.uid = result.study_instance_uid

                    if item.context.acquisition and not item.context.acquisition.uid:
                        item.context.acquisition.uid = result.series_instance_uid

                    self.update_items.push(
                        {"id": item.id, "context": item.context.dict(exclude_none=True)}
                    )
                elif isinstance(result, s.Error):
                    self.insert_errors.push(result.dict())
                else:
                    raise ValueError(f"Unexpected type: {type(result)}")

        # update item context
        detect_duplicates.detect_uid_conflicts_in_item(item, uids, self.insert_errors)

        self.insert_uids.flush()
        self.update_items.flush()
        self.insert_uids.flush()
        self.insert_errors.flush()

    def _scan_dicom_file(
        self,
        fp: t.IO[t.AnyStr],
        tags: t.List[Tag],
        filename: str,
        item_id: UUID,
    ) -> t.Union[s.Error, s.UIDIn]:
        """Scan a single dicom file, and extract UIDs

        Args:
            fp     (BinaryIO): File like object
            tags   (list): Dicom tags

        """
        # Don't decode while scanning, stop as early as possible
        dcm = DicomFile(
            fp,
            parse=False,
            decode=False,
            stop_when=dicom.stop_at_key((0x0020, 0x9056)),
            update_in_place=False,
            specific_tags=tags,
            force=True,
        )
        # dcm.get() return None by default if it does not exist
        data = {
            "item_id": item_id,
            "filename": filename,
            "study_instance_uid": dcm.get("StudyInstanceUID"),
            "series_instance_uid": dcm.get("SeriesInstanceUID"),
            "sop_instance_uid": dcm.get("SOPInstanceUID"),
            "acquisition_number": dcm.get("AcquisitionNumber", None),
        }

        try:
            return s.UIDIn(**data)
        except ValidationError as exc:
            fields = []
            for err in exc.errors():
                fields.append(", ".join((err["loc"])))

            return s.Error(
                code=errors.InvalidDicomFile.code,
                message=f"Skipped file {filename} because of missing {', '.join(fields)}",
                filepath=filename,
                task_id=self.task.id,
                item_id=item_id,
            )

    def _on_success(self):
        self.db.start_resolving()

    def _on_error(self):
        self.db.fail()
