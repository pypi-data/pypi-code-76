# copyright 2018-2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

"""custom storages for S3"""

import uuid
from logging import getLogger

from six import PY3
import os
import boto3

from cubicweb import Binary, set_log_methods
from cubicweb.server.sources.storages import Storage
from cubicweb.server.edition import EditedEntity
from cubicweb.server.hook import DataOperationMixIn, LateOperation


class S3Storage(Storage):
    is_source_callback = True

    def __init__(self, bucket, suffix='.tmp'):
        self.s3cnx = self._s3_client()
        self.bucket = bucket
        self.suffix = suffix

    @classmethod
    def _s3_client(cls):
        endpoint_url = os.environ.get('AWS_S3_ENDPOINT_URL')
        if endpoint_url:
            cls.debug('Using custom S3 endpoint url {}'.format(endpoint_url))
        return boto3.client('s3',
                            endpoint_url=endpoint_url)

    def callback(self, source, cnx, value):
        """see docstring for prototype, which vary according to is_source_callback
        """
        key = source.binary_to_str(value).decode('utf-8')
        if cnx.commit_state == 'precommit':
            # download suffixed key if it exists
            # FIXME need a way to check that the attribute is actually edited
            try:
                suffixed_key = self.suffixed_key(key)
                return self.download(suffixed_key)
            except Exception:
                pass
        try:
            return self.download(key)
        except Exception as ex:
            source.critical("can't retrieve S3 object %s: %s", value, ex)
            return None

    def entity_added(self, entity, attr):
        """an entity using this storage for attr has been added"""
        if entity._cw.transaction_data.get('fs_importing'):
            # fs_importing allows to change S3 key saved in database
            entity._cw_dont_cache_attribute(attr, repo_side=True)
            key = entity.cw_edited[attr].getvalue()
            if PY3:
                key = key.decode('utf-8')
            try:
                return self.download(key)
            except Exception:
                return None

        binary = entity.cw_edited.pop(attr)
        if binary is None:
            # remove S3 key
            entity.cw_edited.edited_attribute(attr, None)
            self.entity_deleted(entity, attr)
        else:
            key = self.get_s3_key(entity, attr)
            if key is None:
                key = self.new_s3_key(entity, attr)
            # save S3 key
            entity.cw_edited.edited_attribute(
                attr, Binary(key.encode('utf-8')))

            # copy Binary value, workaround for boto3 bug
            # https://github.com/boto/s3transfer/issues/80
            # .read() is required since Binary can't wrap itself
            binary.seek(0)
            buffer = Binary(binary.read())
            binary.seek(0)
            suffixed_key = self.suffixed_key(key)
            extra_args = self.get_upload_extra_args(entity, attr, key)
            self.s3cnx.upload_fileobj(buffer, self.bucket, suffixed_key,
                                      ExtraArgs=extra_args)
            buffer.close()

            # move to final key in post commit event
            S3AddFileOp.get_instance(entity._cw).add_data(
                (self, key, entity.eid, attr))
            self.info('Temporary uploaded %s.%s (%s/%s) to S3',
                      entity.eid, attr, self.bucket, suffixed_key)
        return binary

    def get_upload_extra_args(self, _entity, _attr, _key):
        """Additional options for boto3's upload_fileobj method.
        Documentation for supported options can be found at:
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#the-extraargs-parameter
        """
        return {}

    def entity_updated(self, entity, attr):
        """an entity using this storage for attr has been updatded"""
        return self.entity_added(entity, attr)

    def entity_deleted(self, entity, attr):
        """an entity using this storage for attr has been deleted"""
        if entity._cw.repo.config['s3-auto-delete']:
            key = self.get_s3_key(entity, attr)
            if key is None:
                # no key to remove
                return
            # delete key in a post commit event
            S3DeleteFileOp.get_instance(entity._cw).add_data(
                (self, key, entity.eid, attr))
            self.info('Delaying deletion for %s.%s (%s/%s) in S3',
                      entity.eid, attr, self.bucket, key)

    def migrate_entity(self, entity, attribute):
        """migrate an entity attribute to the storage"""
        entity.cw_edited = EditedEntity(entity, **entity.cw_attr_cache)
        binary = self.entity_added(entity, attribute)
        if binary is not None:
            cnx = entity._cw
            source = cnx.repo.system_source
            attrs = source.preprocess_entity(entity)
            sql = source.sqlgen.update('cw_' + entity.cw_etype, attrs,
                                       ['cw_eid'])
            source.doexec(cnx, sql, attrs)
        entity.cw_edited = None

    def get_s3_key(self, entity, attr):
        """
        Return the S3 key of the S3 object storing the content of attribute
        attr of the entity.
        """
        try:
            rset = entity._cw.execute(
                'Any stkey(D) WHERE X eid %s, X %s D' %
                (entity.eid, attr))
        except NotImplementedError:
            # may occur when called from migrate_entity, ie. when the storage
            # has not yet been installed
            rset = None
        if rset and rset.rows[0][0]:
            key = rset.rows[0][0].getvalue()
            if PY3:
                key = key.decode('utf-8')
            return key
        return None

    def new_s3_key(self, entity, attr):
        """Generate a new key for given entity attr.

        This implementation just returns a random UUID"""
        return str(uuid.uuid1())

    def suffixed_key(self, key):
        return key + self.suffix

    def download(self, key):
        result = self.s3cnx.get_object(Bucket=self.bucket, Key=key)
        self.info('Downloaded %s/%s from S3', self.bucket, key)
        return Binary(result['Body'].read())


class S3AddFileOp(DataOperationMixIn, LateOperation):
    containercls = list

    def postcommit_event(self):
        consumed_keys = set()
        for storage, key, eid, attr in self.get_data():
            if key in consumed_keys:
                continue
            consumed_keys.add(key)
            suffixed_key = storage.suffixed_key(key)
            storage.s3cnx.copy_object(
                Bucket=storage.bucket,
                CopySource={'Bucket': storage.bucket, 'Key': suffixed_key},
                Key=key)
            storage.s3cnx.delete_object(
                Bucket=storage.bucket, Key=suffixed_key)
            self.info('Moved temporary object for %s.%s (%s/%s to %s/%s)'
                      ' in S3', eid, attr, storage.bucket, suffixed_key,
                      storage.bucket, key)

    def rollback_event(self):
        for storage, key, eid, attr in self.get_data():
            suffixed_key = storage.suffixed_key(key)
            storage.s3cnx.delete_object(
                Bucket=storage.bucket, Key=suffixed_key)
            self.info('Deleted temporary object for %s.%s (%s/%s) in S3',
                      eid, attr, storage.bucket, suffixed_key)


class S3DeleteFileOp(DataOperationMixIn, LateOperation):
    containercls = list

    def postcommit_event(self):
        for storage, key, eid, attr in self.get_data():
            self.info('Deleting object %s.%s (%s/%s) from S3',
                      eid, attr, storage.bucket, key)
            resp = storage.s3cnx.delete_object(Bucket=storage.bucket, Key=key)
            if resp.get('ResponseMetadata', {}).get('HTTPStatusCode') >= 300:
                self.error('S3 object deletion FAILED: %s', resp)
            else:
                self.debug('S3 object deletion OK: %s', resp)


set_log_methods(S3Storage,
                getLogger('cube.s3storage.storages.s3storage'))
