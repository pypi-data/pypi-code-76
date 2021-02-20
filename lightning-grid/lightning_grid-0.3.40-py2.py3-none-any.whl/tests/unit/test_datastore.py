import json
import math
import os
from tempfile import TemporaryDirectory

import pytest

from grid.datastore import DatastoreUploadSession
from grid.datastore import DatastoreUploadSteps
from grid.datastore import UnsupportedDatastoreImplementationError
import grid.datastore as datastore
from grid.tar import TarResults


class TestDatastore:
    @classmethod
    def setup_class(cls):
        datastore.gql = lambda x: x

    @staticmethod
    def test_datastore_recover(monkeypatch):
        with TemporaryDirectory() as tempdir:
            session = DatastoreUploadSession(name="test",
                                             source_dir="test_dir",
                                             credential_id="cc-abcdef")
            session.last_completed_step = DatastoreUploadSteps.GET_PRESIGNED_URLS
            session.session_file = os.path.join(tempdir, "session.json")
            session.presigned_urls = {
                1: "http://www.grid.ai/1",
                2: "http://www.grid.ai/2",
                3: "http://www.grid.ai/3",
                4: "http://www.grid.ai/4"
            }
            session.etags = {2: "etag2", 3: "etag3"}
            session.part_count = 4
            session._write_session()
            recovered_session = DatastoreUploadSession.recover(tempdir)
            assert session.last_completed_step == recovered_session.last_completed_step
            assert session.presigned_urls == recovered_session.presigned_urls
            assert session.part_count == recovered_session.part_count
            assert session.etags == recovered_session.etags

    @staticmethod
    def test_datastore_outdated_Version(monkeypatch):
        with TemporaryDirectory() as tempdir:
            session = DatastoreUploadSession(name="test",
                                             source_dir="test_dir",
                                             credential_id="cc-abcdef")
            session.last_completed_step = DatastoreUploadSteps.GET_PRESIGNED_URLS
            session.session_file = os.path.join(tempdir, "session.json")
            session.presigned_urls = {
                1: "http://www.grid.ai/1",
                2: "http://www.grid.ai/2",
                3: "http://www.grid.ai/3",
                4: "http://www.grid.ai/4"
            }
            session.etags = {2: "etag2", 3: "etag3"}
            session.part_count = 4
            session.DATASTORE_VERSION = 0
            session._write_session()
            with pytest.raises(UnsupportedDatastoreImplementationError):
                DatastoreUploadSession.recover(tempdir)

    @staticmethod
    def test_datastore_steps(monkeypatch):
        session = DatastoreUploadSession(name="test",
                                         source_dir="test_dir",
                                         credential_id="cc-abcdef")

        class MockS3Uploader:
            def __init__(self, session):
                self.session = session

            def upload(self):
                self.session.upload_part_completed(1, "etag1")
                self.session.upload_part_completed(2, "etag2")

        class MockClient:
            def execute(self, query, variable_values):
                if "GetPresignedUrls" in query:
                    assert variable_values == {
                        'credentialId': 'cc-abcdef',
                        'datastoreName': 'test',
                        'count': 50
                    }

                    return {
                        'getPresignedUrls': {
                            'datastoreVersion': 1,
                            'presignedUrls': [],
                            'uploadId': "upload1",
                            'datastoreId': "abcde"
                        }
                    }
                if "uploadDatastore" in query:
                    assert variable_values == {
                        'name': 'test',
                        'version': 1,
                        'uploadId': 'upload1',
                        'credentialId': 'cc-abcdef',
                        'parts': json.dumps({
                            1: "etag1",
                            2: "etag2"
                        }),
                        'size': math.ceil((1024 * 1000 * 1000) / (1024**2))
                    }

                    return {
                        'uploadDatastore': {
                            'success': True,
                            'message': ''
                        }
                    }

                raise ValueError(f"Unexpected query {query}")

        client = MockClient()
        session.configure(client=client)

        def tar_directory(**kwargs):
            return TarResults(before_size=1024 * 1000 * 1000,
                              after_size=1024 * 1000 * 1000)

        def create_uploader(presigned_urls):
            return MockS3Uploader(session)

        monkeypatch.setattr('grid.datastore.tar_directory', tar_directory)
        monkeypatch.setattr(session, '_create_uploader', create_uploader)

        session.upload()
