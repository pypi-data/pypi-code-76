################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
from watson_machine_learning_client.libs.repo.mlrepositoryartifact import MLRepositoryArtifact
from watson_machine_learning_client.libs.repo.mlrepository import MetaProps, MetaNames
import requests
from watson_machine_learning_client.utils import MODEL_DETAILS_TYPE, INSTANCE_DETAILS_TYPE, load_model_from_directory, STR_TYPE, STR_TYPE_NAME, docstring_parameter, meta_props_str_conv, str_type_conv
from watson_machine_learning_client.metanames import ModelMetaNames,LibraryMetaNames
import os
import copy
import json
import urllib.parse
from watson_machine_learning_client.wml_client_error import WMLClientError, ApiRequestFailure
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.libs.repo.util.compression_util import CompressionUtil
from watson_machine_learning_client.libs.repo.util.unique_id_gen import uid_generate
from watson_machine_learning_client.href_definitions import API_VERSION, SPACES,PIPELINES, LIBRARIES, EXPERIMENTS, RUNTIMES, DEPLOYMENTS, SOFTWARE_SPEC


import shutil
import re

_DEFAULT_LIST_LENGTH = 50


class Models(WMLResource):
    """
    Store and manage your models.
    """
    ConfigurationMetaNames = ModelMetaNames()
    LibraryMetaNames = LibraryMetaNames()
    """MetaNames for models creation."""

    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        if not client.ICP and not self._client.WSD:
            Models._validate_type(client.service_instance.details, u'instance_details', dict, True)
            Models._validate_type_of_details(client.service_instance.details, INSTANCE_DETAILS_TYPE)
        self._ICP = client.ICP
        self._CAMS = client.CAMS
        if self._CAMS:
            self.default_space_id = client.default_space_id

    def _save_library_archive(self, ml_pipeline):

        id_length = 20
        gen_id = uid_generate(id_length)
        temp_dir_name = '{}'.format("library" + gen_id)
        # if (self.hummingbird_env == 'HUMMINGBIRD') is True:
        #     temp_dir = os.path.join('/home/spark/shared/wml/repo/extract_', temp_dir_name)
        # else:
        temp_dir = os.path.join('.', temp_dir_name)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        ml_pipeline.write().overwrite().save(temp_dir)
        archive_path = self._compress_artifact(temp_dir)
        shutil.rmtree(temp_dir)
        return archive_path

    def _compress_artifact(self, compress_artifact):
        tar_filename = '{}_content.tar'.format('library')
        gz_filename = '{}.gz'.format(tar_filename)
        CompressionUtil.create_tar(compress_artifact, '.', tar_filename)
        CompressionUtil.compress_file_gzip(tar_filename, gz_filename)
        os.remove(tar_filename)
        return gz_filename

    def _create_pipeline_input(self,lib_href,name,space_uid=None, project_uid=None):

        if self._client.CAMS or self._client.WSD:
            metadata = {
                self._client.pipelines.ConfigurationMetaNames.NAME: name + "_"+uid_generate(8),
                self._client.pipelines.ConfigurationMetaNames.DOCUMENT: {
                    "doc_type": "pipeline",
                    "version": "2.0",
                    "primary_pipeline": "dlaas_only",
                    "pipelines": [
                        {
                            "id": "dlaas_only",
                            "runtime_ref": "spark",
                            "nodes": [
                                {
                                    "id": "repository",
                                    "type": "model_node",
                                    "inputs": [
                                    ],
                                    "outputs": [],
                                    "parameters": {
                                        "training_lib_href": lib_href
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        else:  # for cloud do not change anything
            metadata = {
                self._client.pipelines.ConfigurationMetaNames.NAME: name + "_" + uid_generate(8),
                self._client.pipelines.ConfigurationMetaNames.DOCUMENT: {
                    "doc_type": "pipeline",
                    "version": "2.0",
                    "primary_pipeline": "dlaas_only",
                    "pipelines": [
                        {
                            "id": "dlaas_only",
                            "runtime_ref": "spark",
                            "nodes": [
                                {
                                    "id": "repository",
                                    "type": "model_node",
                                    "inputs": [
                                    ],
                                    "outputs": [],
                                    "parameters": {
                                        "training_lib_href": lib_href + "/content"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }

        if space_uid is not None:
            metadata.update({self._client.pipelines.ConfigurationMetaNames.SPACE_UID: space_uid})

        if self._client.default_project_id is not None:
            metadata.update({'project': {"href": "/v2/projects/" + self._client.default_project_id}})
        return metadata

    def _publish_from_object(self, model, meta_props, training_data=None, training_target=None, pipeline=None, feature_names=None, label_column_names=None, project_id=None):
        """
        Store model from object in memory into Watson Machine Learning repository on Cloud
        """
        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.NAME, STR_TYPE, True)
        if self._client.ICP_30 is None and self._client.WSD_20 is None:
            if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props and \
               self.ConfigurationMetaNames.RUNTIME_UID not in meta_props:
                raise WMLClientError("Invalid input. It is mandatory to provide RUNTIME_UID in meta_props.")
        else:
            if (self.ConfigurationMetaNames.SOFTWARE_SPEC_UID not in meta_props or
                meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] is None) and \
               self.ConfigurationMetaNames.RUNTIME_UID not in meta_props:
                  raise WMLClientError("Invalid input. It is mandatory to provide RUNTIME_UID or "
                                       "SOFTWARE_SPEC_UID in meta_props. RUNTIME_UID is deprecated")

        # self._validate_type(project_id, 'project_id',STR_TYPE, True)
        try:
            if 'pyspark.ml.pipeline.PipelineModel' in str(type(model)):
                if(pipeline is None or training_data is None):
                    raise WMLClientError(u'pipeline and training_data are expected for spark models.')
                if not self._client.CAMS and not self._client.WSD:
                    name = meta_props[self.ConfigurationMetaNames.NAME]
                    version = "1.0"
                    platform = {"name": "python", "versions": ["3.5"]}
                    library_tar = self._save_library_archive(pipeline)
                    lib_metadata = {
                        self.LibraryMetaNames.NAME: name + "_" + uid_generate(8),
                        self.LibraryMetaNames.VERSION: version,
                        self.LibraryMetaNames.PLATFORM: platform,
                        self.LibraryMetaNames.FILEPATH: library_tar
                    }

                    if self.ConfigurationMetaNames.SPACE_UID in meta_props:
                        lib_metadata.update(
                            {self.LibraryMetaNames.SPACE_UID: meta_props[
                                self._client.repository.ModelMetaNames.SPACE_UID]})

                    if self._client.CAMS:
                        if self._client.default_space_id is not None:
                            lib_metadata.update(
                                {self.LibraryMetaNames.SPACE_UID: self._client.default_space_id})
                        else:
                            if self._client.default_project_id is None:
                                raise WMLClientError("It is mandatory is set the space or Project. \
                                                                       Use client.set.default_space(<SPACE_GUID>) to set the space or Use client.set.default_project(<PROJECT_ID)")

                    library_artifact = self._client.runtimes.store_library(meta_props=lib_metadata)
                    lib_href = self._client.runtimes.get_library_href(library_artifact)
                    space_uid = None

                    if self.ConfigurationMetaNames.SPACE_UID in meta_props:
                        space_uid = meta_props[self._client.repository.ModelMetaNames.SPACE_UID]
                    if self._client.CAMS:
                        space_uid = self._client.default_space_id
                    pipeline_metadata = self._create_pipeline_input(lib_href, name, space_uid=space_uid)
                    pipeline_save = self._client.pipelines.store(pipeline_metadata)

                    pipeline_href = self._client.pipelines.get_href(pipeline_save)

                if self._client.CAMS or self._client.WSD:
                    name = meta_props[self.ConfigurationMetaNames.NAME]
                    version = "1.0"
                    import sys
                    version = float(sys.version.split()[0][0:3])
                    if version == 3.7:
                        platform = {"name": "python", "versions": ["3.7"]}
                    else:
                        platform = {"name": "python", "versions": ["3.6"]}
                    library_tar = self._save_library_archive(pipeline)
                    model_definition_props = {
                        self._client.model_definitions.ConfigurationMetaNames.NAME: name + "_" + uid_generate(8),
                        self._client.model_definitions.ConfigurationMetaNames.VERSION: str(version),
                        self._client.model_definitions.ConfigurationMetaNames.PLATFORM: platform,
                    }
                    training_lib = self._client.model_definitions.store(library_tar, model_definition_props)
                    if self._client.WSD:
                        lib_href = "/v2/assets/" + training_lib['metadata']['asset_id']
                        pipeline_metadata = self._create_pipeline_input(lib_href, name, space_uid=None)
                        pipeline_save = self._client.pipelines.store(pipeline_metadata)
                        pipeline_href = "/v2/assets/" + pipeline_save['metadata']['asset_id']
                        meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID] = {
                            "href": pipeline_href}
                    else:
                        lib_href = self._client.model_definitions.get_href(training_lib)
                        lib_href = lib_href.split("?", 1)[0] # temp fix for stripping space_id
                    # space_uid = None

                    # if self.ConfigurationMetaNames.SPACE_UID in meta_props:
                    #     space_uid = meta_props[self._client.repository.ModelMetaNames.SPACE_UID]
                    # if self._client.CAMS:
                    #     space_uid = self._client.default_space_id
                    pipeline_metadata = self._create_pipeline_input(lib_href, name, space_uid=None)
                    pipeline_save = self._client.pipelines.store(pipeline_metadata)

                    pipeline_href = self._client.pipelines.get_href(pipeline_save)

                if not self._client.WSD:
                    meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID] = {"href": pipeline_href}

                if self.ConfigurationMetaNames.SPACE_UID in meta_props and meta_props[self._client.repository.ModelMetaNames.SPACE_UID] is not None:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SPACE_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.SPACE_UID] = {"href": API_VERSION + SPACES + "/" + meta_props[self._client.repository.ModelMetaNames.SPACE_UID]}
                else:
                    if self._client.default_project_id is not None:
                        meta_props['project'] = {"href": "/v2/projects/" + self._client.default_project_id}

                if self.ConfigurationMetaNames.RUNTIME_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.RUNTIME_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID] = {"href": API_VERSION + RUNTIMES + "/" + meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID]}

                if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props:
                    if self._client.ICP_30:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                        meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] = {"id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}
                    elif self._client.WSD_20:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE,
                                                 False)
                        meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] = {
                            "base_id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}
                    else:
                        meta_props.pop(self.ConfigurationMetaNames.SOFTWARE_SPEC_UID)

                if self._client.ICP_30 or self._client.WSD_20:
                    if self.ConfigurationMetaNames.MODEL_DEFINITION_UID in meta_props:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.MODEL_DEFINITION_UID, STR_TYPE, False)
                        meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID] = {"id":meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID]}
                else:
                    if self.ConfigurationMetaNames.TRAINING_LIB_UID in meta_props:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TRAINING_LIB_UID, STR_TYPE, False)
                        meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID] = {"href": API_VERSION + LIBRARIES + "/" + meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID]}

                meta_data = MetaProps(self._client.repository._meta_props_to_repository_v3_style(meta_props))

                model_artifact = MLRepositoryArtifact(model, name=str(meta_props[self.ConfigurationMetaNames.NAME]), meta_props=meta_data, training_data=training_data)
            else:
                if self.ConfigurationMetaNames.SPACE_UID in meta_props and meta_props[self._client.repository.ModelMetaNames.SPACE_UID] is not None:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SPACE_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.SPACE_UID] = {"href": API_VERSION + SPACES + "/" + meta_props[self._client.repository.ModelMetaNames.SPACE_UID]}
                if self._client.CAMS:
                    if self._client.default_space_id is not None:
                        meta_props[self._client.repository.ModelMetaNames.SPACE_UID] = {
                            "href": API_VERSION + SPACES + "/" + self._client.default_space_id}
                    else:
                        if self._client.default_project_id is not None:
                            meta_props['project'] = {"href": "/v2/projects/" + self._client.default_project_id}
                        else:
                            raise WMLClientError("It is mandatory is set the space or Project. \
                             Use client.set.default_space(<SPACE_GUID>) to set the space or Use client.set.default_project(<PROJECT_ID)")
                if self.ConfigurationMetaNames.RUNTIME_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.RUNTIME_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID] = {"href": API_VERSION + RUNTIMES + "/" + meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID]}
                if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props:
                    if self._client.ICP_30:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                        meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] = \
                            {"id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}
                    elif self._client.WSD_20:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE,
                                                 False)
                        meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] = \
                            {"base_id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}
                    else:
                        meta_props.pop(self.ConfigurationMetaNames.SOFTWARE_SPEC_UID)

                if self.ConfigurationMetaNames.PIPELINE_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.PIPELINE_UID, STR_TYPE, False)
                    if self._client.WSD:
                        meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID] = {"href": "/v2/assets/" + meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID]}
                    else:
                        meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID] = {"href": API_VERSION + PIPELINES + "/" + meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID]}

                if self._client.ICP_30 or self._client.WSD_20:
                    if self.ConfigurationMetaNames.MODEL_DEFINITION_UID in meta_props:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.MODEL_DEFINITION_UID, STR_TYPE,
                                                 False)
                        meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID] = {
                            "id": meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID]}
                else:
                    if self.ConfigurationMetaNames.TRAINING_LIB_UID in meta_props:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TRAINING_LIB_UID, STR_TYPE, False)
                        meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID] = {"href": API_VERSION + LIBRARIES + "/" + meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID]}

                if not str(meta_props[self.ConfigurationMetaNames.TYPE]).startswith('tensorflow_2.1'):
                    meta_data = MetaProps(self._client.repository._meta_props_to_repository_v3_style(meta_props))
                    model_artifact = MLRepositoryArtifact(model, name=str(meta_props[self.ConfigurationMetaNames.NAME]), meta_props=meta_data, training_data=training_data, training_target=training_target, feature_names=feature_names, label_column_names=label_column_names)
            if self._client.CAMS:
                if self._client.default_project_id is not None:
                    query_param_for_repo_client = {'project_id': self._client.default_project_id}
                else:
                    query_param_for_repo_client = {'space_id': self._client.default_space_id}

            else:
                if self._client.WSD:
                    if self._client.default_project_id is not None:
                        query_param_for_repo_client = {'project_id': self._client.default_project_id}
                        meta_props['project'] = {"href": "/v2/projects/" + self._client.default_project_id}
                    else:
                        raise WMLClientError(u'Project id is not set.')
                else:
                    query_param_for_repo_client = None
            if self._client.WSD:
                #payload = self._create_model_payload(meta_props)
                wsd_url = self._href_definitions.get_wsd_base_href()

                if str(meta_props[self.ConfigurationMetaNames.TYPE]).startswith('tensorflow_2.1'):
                    saved_model_path = self._wsd_get_tf21_model(model, meta_props)
                    meta_data = MetaProps(self._client.repository._meta_props_to_repository_v3_style(meta_props))
                    model_artifact = MLRepositoryArtifact(saved_model_path, name=str(meta_props[self.ConfigurationMetaNames.NAME]),
                                                          meta_props=meta_data, training_data=training_data,
                                                          training_target=training_target, feature_names=feature_names,
                                                          label_column_names=label_column_names)



                saved_model = self._client.repository._ml_repository_client.models.wsd_save(wsd_url, model_artifact, meta_props, meta_props,
                                                                                             query_param=query_param_for_repo_client,
                                                                                             headers= self._client._get_headers())
                return self.get_details(u'{}'.format(saved_model['asset_id']),ignore_warnings=True)
            else:
                if str(meta_props[self.ConfigurationMetaNames.TYPE]).startswith('tensorflow_2.1') and \
                        (self._client.ICP_30 or self._client.CAMS):
                    saved_model = self._store_tf21_model(model, meta_props)
                    return saved_model
                else:
                    saved_model = self._client.repository._ml_repository_client.models.save(model_artifact, query_param=query_param_for_repo_client)
        except Exception as e:
            raise WMLClientError(u'Publishing model failed.', e)
        else:
            return self.get_details(u'{}'.format(saved_model.uid),ignore_warnings=True)

    def _get_subtraining_object(self,trainingobject,subtrainingId):
        subtrainings = trainingobject["resources"]
        for each_training in subtrainings:
            if each_training["metadata"]["guid"] == subtrainingId:
                return each_training
        raise WMLClientError("The subtrainingId " + subtrainingId + " is not found")

    ##TODO not yet supported

    def _publish_from_training(self, model_uid, meta_props, training_data=None, training_target=None,version=False,artifactId=None,subtrainingId=None):
        """
                Store trained model from object storage into Watson Machine Learning repository on IBM Cloud
        """
        model_meta = self.ConfigurationMetaNames._generate_resource_metadata(
            meta_props,
            client=self._client
        )

        if self.ConfigurationMetaNames.RUNTIME_UID in meta_props:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.RUNTIME_UID, STR_TYPE, False)
            model_meta.update({self.ConfigurationMetaNames.RUNTIME_UID: {
                "href": API_VERSION + RUNTIMES + "/" + meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID]}})
        if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props:
            if self._client.ICP_30:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                model_meta.update({self.ConfigurationMetaNames.SOFTWARE_SPEC_UID: {
                    "id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}})
            elif self._client.WSD_20:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                model_meta.update({self.ConfigurationMetaNames.SOFTWARE_SPEC_UID: {
                    "base_id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}})
            else:
                model_meta.pop(self.ConfigurationMetaNames.SOFTWARE_SPEC_UID)

        if self.ConfigurationMetaNames.SPACE_UID in meta_props and meta_props[self._client.repository.ModelMetaNames.SPACE_UID] is not None:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SPACE_UID, STR_TYPE, False)
            model_meta.update({self.ConfigurationMetaNames.SPACE_UID: {
                "href": API_VERSION + SPACES + "/" + meta_props[self._client.repository.ModelMetaNames.SPACE_UID]}})
        if self.ConfigurationMetaNames.PIPELINE_UID in meta_props:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.PIPELINE_UID, STR_TYPE, False)
            if self._client.WSD:
                model_meta.update({self.ConfigurationMetaNames.PIPELINE_UID: {
                    "href": "/v2/assets/" + meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID]}})
            else:
                model_meta.update({self.ConfigurationMetaNames.PIPELINE_UID: {
                    "href": API_VERSION + PIPELINES + "/" + meta_props[
                        self._client.repository.ModelMetaNames.PIPELINE_UID]}})

        if self._client.ICP_30:
            if self.ConfigurationMetaNames.MODEL_DEFINITION_UID in meta_props:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.MODEL_DEFINITION_UID, STR_TYPE, False)
                meta_props[self.ConfigurationMetaNames.MODEL_DEFINITION_UID] = {
                    "id": meta_props[self.ConfigurationMetaNames.MODEL_DEFINITION_UID]}
        else:
            if self.ConfigurationMetaNames.TRAINING_LIB_UID in meta_props:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TRAINING_LIB_UID, STR_TYPE, False)
                model_meta.update({self.ConfigurationMetaNames.TRAINING_LIB_UID: {
                    "href": API_VERSION + LIBRARIES + "/" + meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID]}})
        if self._client.default_project_id is not None:
            model_meta.update({'project': {"href": "/v2/projects/" + self._client.default_project_id}})

        input_schema = []
        output_schema = []
        if self.ConfigurationMetaNames.INPUT_DATA_SCHEMA in meta_props and \
           meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA] is not None:
            if self._client.ICP_30 or self._client.WSD_20:
                if isinstance(meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA], dict):
                    input_schema = [meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]]
                else:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.INPUT_DATA_SCHEMA, list, False)
                    input_schema = meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.INPUT_DATA_SCHEMA, dict, False)
                input_schema = meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]
            model_meta.pop(self.ConfigurationMetaNames.INPUT_DATA_SCHEMA)
        if self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA in meta_props:
            if str(meta_props[self.ConfigurationMetaNames.TYPE]).startswith('do-') and \
                    (self._client.ICP_30 or self._client.WSD_20):
                try:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, dict, False)
                    output_schema = [meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]]
                except WMLClientError:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA,list, False)
                    output_schema = meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, dict, False)
                output_schema = [meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]]
            model_meta.pop(self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA)

        if len(input_schema) != 0 or len(output_schema) != 0:
            model_meta.update({"schemas": {
                "input": input_schema,
                "output": output_schema}
            })

        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.NAME, STR_TYPE, True)

        details = self._client.training.get_details(model_uid)
        model_type = ""
        runtime_uid = ""

        ##Check if the training is created from pipeline or experiment
        verify = True
        if self._client.ICP:
            verify = False
        if "pipeline" in details["entity"]:
            if self._client.ICP_30:
                pipeline_id = details['entity']['pipeline']['id']
            else:
                href = details["entity"]["pipeline"]["href"]
                pipeline_id = href.split("/")[3]
            if "model_type" in details["entity"]["pipeline"]:
                model_type = details["entity"]["pipeline"]["model_type"]
                #runtime_uid = model_type + "-py3"
        # if "experiment" in details["entity"]:
        #     if subtrainingId is None:
        #         raise WMLClientError("For a training created via experiment, it is mandatory to specify subtrainingId.")
        #     exp_href = details["entity"]["experiment"]["href"]
        #
        #     exp_id = exp_href.split("/")[3]
        #     exp_details = self._client.experiments.get_details(exp_id)
        #
        #     href = exp_details["entity"]["training_references"][0]["pipeline"]["href"]
        #     if "model_type" in  exp_details["entity"]["training_references"][0]["pipeline"]:
        #         model_type = details["entity"]["pipeline"]["model_type"]
        #         #runtime_uid = model_type + "-py3"

        if "experiment" in details["entity"]:

            details_parent = requests.get(
                       self._wml_credentials['url'] + '/v4/trainings?parent_id='+model_uid,
                       params = self._client._params(),
                       headers=self._client._get_headers(),
                       verify = verify
                )
            details_json = self._handle_response(200,"Get training details",details_parent)
            subtraining_object = self._get_subtraining_object(details_json,subtrainingId)
            model_meta.update({"import": subtraining_object["entity"]["results_reference"]})
            if "pipeline" in subtraining_object["entity"]:
                pipeline_id =  subtraining_object["entity"]["pipeline"]["href"].split("/")[3]
                if "model_type" in subtraining_object["entity"]["pipeline"]:
                     model_type = subtraining_object["entity"]["pipeline"]["model_type"]
                    #runtime_uid = model_type + "-py3"
        else:
            model_meta.update({"import": details["entity"]["results_reference"]})

        if "pipeline" in details["entity"] or "experiment" in details["entity"]:
            if "experiment" in details["entity"]:
                details_parent = requests.get(
                    self._wml_credentials['url'] + '/v4/trainings?parent_id=' + model_uid,
                    params=self._client._params(),
                    headers=self._client._get_headers(),
                    verify=verify
                )
                details_json = self._handle_response(200, "Get training details", details_parent)
                subtraining_object = self._get_subtraining_object(details_json, subtrainingId)
                if "pipeline" in subtraining_object["entity"]:
                    definition_details = self._client.pipelines.get_details(pipeline_id)
                    runtime_uid = definition_details["entity"]["document"]["runtimes"][0]["name"] + "_" + \
                                  definition_details["entity"]["document"]["runtimes"][0]["version"].split("-")[0] + "-py3"
                    if model_type == "":
                        model_type = definition_details["entity"]["document"]["runtimes"][0]["name"] + "_" + \
                                     definition_details["entity"]["document"]["runtimes"][0]["version"].split("-")[0]

                    if self.ConfigurationMetaNames.TYPE not in meta_props:
                        model_meta.update({"type": model_type})

                    if self.ConfigurationMetaNames.RUNTIME_UID not in meta_props:
                        model_meta.update({"runtime": {"href": "/v4/runtimes/" + runtime_uid}})
            else:
                definition_details = self._client.pipelines.get_details(pipeline_id)
                runtime_uid = definition_details["entity"]["document"]["runtimes"][0]["name"] + "_" + \
                              definition_details["entity"]["document"]["runtimes"][0]["version"].split("-")[0] + "-py3"
                if model_type == "":
                    model_type = definition_details["entity"]["document"]["runtimes"][0]["name"] + "_" + \
                                 definition_details["entity"]["document"]["runtimes"][0]["version"].split("-")[0]

                if self.ConfigurationMetaNames.TYPE not in meta_props:
                    model_meta.update({"type": model_type})

                if self.ConfigurationMetaNames.RUNTIME_UID not in meta_props:
                    if not self._client.ICP_30:
                        model_meta.update({"runtime": {"href": "/v4/runtimes/" + runtime_uid}})
                    else:
                        if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID not in meta_props:
                            model_meta.update({"runtime": {"href": "/v4/runtimes/" + runtime_uid}})
        if self._client.ICP_30:
            if self.ConfigurationMetaNames.MODEL_DEFINITION_UID in meta_props:
                model_meta[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID] = {
                    "id": model_meta[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID]}
        if not self._ICP:
                creation_response = requests.post(
                       self._wml_credentials['url'] + '/v4/models',
                       headers=self._client._get_headers(),
                       json=model_meta
                )
        else:
                creation_response = requests.post(
                    self._wml_credentials['url'] + '/v4/models',
                    headers=self._client._get_headers(),
                    json=model_meta,
                    verify=False
                )
        if creation_response.status_code == 201:
            model_details = self._handle_response(201, u'creating new model', creation_response)
        elif creation_response.status_code == 200:
            model_details = self._handle_response(200, u'creating new model', creation_response)
        else:
            model_details = self._handle_response(202, u'creating new model', creation_response)
        model_uid = model_details['metadata']['guid']
        return self.get_details(model_uid,ignore_warnings=True)

    def _store_autoAI_model(self,model_path, meta_props, training_data=None, training_target=None,version=False,artifactId=None,subtrainingId=None):
        """
                Store trained model from object storage into Watson Machine Learning repository on IBM Cloud
        """
        model_meta = self.ConfigurationMetaNames._generate_resource_metadata(
            meta_props,
            client=self._client
        )
        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.NAME, STR_TYPE, True)

        # note: remove pipeline-model.json part from the string to allow correct regexp
        if model_path.endswith('pipeline-model.json'):
            x = re.findall(r"[0-9A-Za-z-]+-[0-9A-Za-z-]+", '/'.join(model_path.split('/')[:-1]))
            # --- end note
        else:
            x = re.findall(r"[0-9A-Za-z-]+-[0-9A-Za-z-]+", model_path)

        model_uid = x[-1] if x else ''
        details = self._client.training.get_details(model_uid)

        if self.ConfigurationMetaNames.RUNTIME_UID in meta_props:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.RUNTIME_UID, STR_TYPE, False)
            model_meta.update({self.ConfigurationMetaNames.RUNTIME_UID: {
                "href": API_VERSION + RUNTIMES + "/" + meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID]}})
        if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props:
            if self._client.ICP_30:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                model_meta.update({self.ConfigurationMetaNames.SOFTWARE_SPEC_UID: {
                    "id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}})
            elif self._client.WSD_20:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                model_meta.update({self.ConfigurationMetaNames.SOFTWARE_SPEC_UID: {
                    "base_id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}})
            else:
                model_meta.pop(self.ConfigurationMetaNames.SOFTWARE_SPEC_UID)

        if self.ConfigurationMetaNames.SPACE_UID in meta_props and \
                meta_props[self._client.repository.ModelMetaNames.SPACE_UID] is not None:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SPACE_UID, STR_TYPE, False)
            model_meta.update({self.ConfigurationMetaNames.SPACE_UID: {
                "href": API_VERSION + SPACES + "/" + meta_props[self._client.repository.ModelMetaNames.SPACE_UID]}})
        if self.ConfigurationMetaNames.PIPELINE_UID in meta_props:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.PIPELINE_UID, STR_TYPE, False)
            if self._client.WSD:
                model_meta.update({self.ConfigurationMetaNames.PIPELINE_UID: {
                    "href": "/v2/assets/" + meta_props[
                        self._client.repository.ModelMetaNames.PIPELINE_UID]}})
            else:
                model_meta.update({self.ConfigurationMetaNames.PIPELINE_UID: {
                    "href": API_VERSION + PIPELINES + "/" + meta_props[
                        self._client.repository.ModelMetaNames.PIPELINE_UID]}})
        if self._client.ICP_30:
            if self.ConfigurationMetaNames.MODEL_DEFINITION_UID in meta_props:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.MODEL_DEFINITION_UID, STR_TYPE, False)
                meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID] = {
                    "id": meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID]}
        else:
            if self.ConfigurationMetaNames.TRAINING_LIB_UID in meta_props:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TRAINING_LIB_UID, STR_TYPE, False)
                model_meta.update({self.ConfigurationMetaNames.TRAINING_LIB_UID: {
                    "href": API_VERSION + LIBRARIES + "/" + meta_props[
                        self._client.repository.ModelMetaNames.TRAINING_LIB_UID]}})
        if self._client.default_project_id is not None:
            model_meta.update({'project': {
                "href": "/v2/projects" + self._client.default_project_id}})

        model_meta.update({"import": details["entity"]["results_reference"]})
        model_meta["import"]["location"]["path"] = model_path
        runtime_uid = 'hybrid_0.1'
        model_type = 'wml-hybrid_0.1'

        # print("model_meta b4" + str(model_meta))


        if self.ConfigurationMetaNames.TYPE not in meta_props:
            model_meta.update({"type": model_type})

        if self.ConfigurationMetaNames.RUNTIME_UID not in meta_props and \
                self.ConfigurationMetaNames.SOFTWARE_SPEC_UID not in meta_props:
            model_meta.update({"runtime": {"href": "/v4/runtimes/"+runtime_uid}})

        input_schema = []
        output_schema = []
        if self.ConfigurationMetaNames.INPUT_DATA_SCHEMA in meta_props and \
                meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA] is not None:
            if self._client.ICP_30 or self._client.WSD_20:
                if isinstance(meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA], dict):
                    input_schema = [meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]]
                else:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.INPUT_DATA_SCHEMA, list, False)
                    input_schema = meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.INPUT_DATA_SCHEMA, dict, False)
                input_schema = [meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]]
            model_meta.pop(self.ConfigurationMetaNames.INPUT_DATA_SCHEMA)

        if self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA in meta_props and \
                meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA] is not None:
            if str(meta_props[self.ConfigurationMetaNames.TYPE]).startswith('do-') and \
                    (self._client.ICP_30 or self._client.WSD_20):
                try:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, dict, False)
                    output_schema = [meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]]
                except WMLClientError:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, list, False)
                    output_schema = meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, dict, False)
                output_schema = [meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]]
            model_meta.pop(self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA)

        if len(input_schema) != 0 or len(output_schema) != 0:
            model_meta.update({"schemas": {
                    "input": input_schema,
                    "output": output_schema}
                })
        if not self._ICP:
                creation_response = requests.post(
                       self._wml_credentials['url'] + '/v4/models',
                       headers=self._client._get_headers(),
                       json=model_meta
                )
        else:
                creation_response = requests.post(
                    self._wml_credentials['url'] + '/v4/models',
                    headers=self._client._get_headers(),
                    json=model_meta,
                    verify=False
                )
        if creation_response.status_code == 201:
            model_details = self._handle_response(201, u'creating new model', creation_response)
        elif creation_response.status_code == 200:
            model_details = self._handle_response(200, u'creating new model', creation_response)
        else:
            model_details = self._handle_response(202, u'creating new model', creation_response)
        model_uid = model_details['metadata']['guid']
        return self.get_details(model_uid,ignore_warnings=True)


    def _publish_from_file(self, model, meta_props=None, training_data=None, training_target=None,ver=False,artifactid=None):
        """
        Store saved model into Watson Machine Learning repository on IBM Cloud
        """
        if not self._client.ICP_30 and not self._client.WSD_20:
            if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props and \
              self.ConfigurationMetaNames.RUNTIME_UID not in meta_props:
                raise WMLClientError("Invalid input. It is mandatory to provide RUNTIME_UID in metaprop.")
        else:
            if (self.ConfigurationMetaNames.SOFTWARE_SPEC_UID not in meta_props or
                meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] is None) and \
               self.ConfigurationMetaNames.RUNTIME_UID not in meta_props:
                raise WMLClientError("Invalid input. It is mandatory to provide RUNTIME_UID or "
                                     "SOFTWARE_SPEC_UID in meta_props. RUNTIME_UID is deprecated")

        if(ver==True):
            #check if artifactid is passed
            Models._validate_type(str_type_conv(artifactid), 'model_uid', STR_TYPE, True)
            return self._publish_from_archive(model, meta_props,version=ver,artifactid=artifactid)
        def is_xml(model_filepath):
            if (os.path.splitext(os.path.basename(model_filepath))[-1] == '.pmml'):
                raise WMLClientError('The file name has an unsupported extension. Rename the file with a .xml extension.')
            return os.path.splitext(os.path.basename(model_filepath))[-1] == '.xml'

        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.NAME, STR_TYPE, True)

        import tarfile
        import zipfile

        model_filepath = model
        if os.path.isdir(model):
            # TODO this part is ugly, but will work. In final solution this will be removed
            if "tensorflow" in meta_props[self.ConfigurationMetaNames.TYPE]:
                # TODO currently tar.gz is required for tensorflow - the same ext should be supported for all frameworks
                if os.path.basename(model) == '':
                    model = os.path.dirname(model)
                filename = os.path.basename(model) + '.tar.gz'
                current_dir = os.getcwd()
                os.chdir(model)
                target_path = os.path.dirname(model)

                with tarfile.open(os.path.join('..', filename), mode='w:gz') as tar:
                    tar.add('.')

                os.chdir(current_dir)
                model_filepath = os.path.join(target_path, filename)
                if tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath) or is_xml(model_filepath):
                    if self._client.WSD:
                        return self._wsd_publish_from_archive(model_filepath, meta_props)
                    else:
                        return self._publish_from_archive(model_filepath, meta_props)
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TYPE, STR_TYPE, True)
                if ('caffe' in meta_props[self.ConfigurationMetaNames.TYPE]):
                    raise WMLClientError(u'Invalid model file path  specified for: \'{}\'.'.format(meta_props[self.ConfigurationMetaNames.TYPE]))

                loaded_model = load_model_from_directory(meta_props[self.ConfigurationMetaNames.TYPE], model)
                if self._client.WSD:
                    return self._wsd_publish_from_archive(model_filepath, meta_props)
                else:
                   saved_model = self._publish_from_object(loaded_model, meta_props, training_data, training_target)

                return saved_model

        elif is_xml(model_filepath):
            try:
                if self.ConfigurationMetaNames.SPACE_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SPACE_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.SPACE_UID] = {"href": API_VERSION + SPACES + "/" + meta_props[self._client.repository.ModelMetaNames.SPACE_UID]}

                if self._client.CAMS:
                    if self._client.default_space_id is not None:
                        meta_props[self._client.repository.ModelMetaNames.SPACE_UID] = {
                            "href": API_VERSION + SPACES + "/" + self._client.default_space_id}
                    else:
                        if self._client.default_project_id is not None:
                            meta_props.update({"project": {"href": "/v2/projects/" + self._client.default_project_id}})
                        else:
                            raise WMLClientError(
                                  "It is mandatory to set the space or project." 
                                  " Use client.set.default_space(<SPACE_GUID>) to set the space or Use client.set.default_project(<PROJECT_GUID>).")

                if self.ConfigurationMetaNames.RUNTIME_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.RUNTIME_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID] = {"href": API_VERSION + RUNTIMES + "/" + meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID]}

                if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props:
                    if self._client.ICP_30:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                        meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] = {
                            "id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}
                    elif self._client.WSD_20:
                        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE,
                                                 False)
                        meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID] = {
                            "base_id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}
                    else:
                        meta_props.pop(self.ConfigurationMetaNames.SOFTWARE_SPEC_UID)

                if self.ConfigurationMetaNames.TRAINING_LIB_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TRAINING_LIB_UID, STR_TYPE, False)
                    meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID] = {"href": API_VERSION + LIBRARIES + "/" + meta_props[self._client.repository.ModelMetaNames.TRAINING_LIB_UID]}
                if self.ConfigurationMetaNames.PIPELINE_UID in meta_props:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.PIPELINE_UID, STR_TYPE, False)
                    if self._client.WSD:
                        meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID] = {"href": "/v2/assets/" + meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID]}
                    else:
                        meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID] = {
                            "href": API_VERSION + PIPELINES + "/" + meta_props[
                                self._client.repository.ModelMetaNames.PIPELINE_UID]}

                meta_data = MetaProps(self._client.repository._meta_props_to_repository_v3_style(meta_props))

                model_artifact = MLRepositoryArtifact(str(model_filepath), name=str(meta_props[self.ConfigurationMetaNames.NAME]), meta_props=meta_data)
                if self._client.CAMS:
                    if self._client.default_space_id is not None:
                        query_param_for_repo_client = {'space_id': self._client.default_space_id}
                    else:
                        if self._client.default_project_id is not None:
                            query_param_for_repo_client = {'project_id': self._client.default_project_id}
                        else:
                            query_param_for_repo_client = None
                else:
                    if self._client.WSD:
                        if self._client.default_project_id is not None:
                            query_param_for_repo_client = {'project_id': self._client.default_project_id}
                        else:
                            WMLClientError("Project id is not set for Watson Studio Desktop.")
                    else:
                        query_param_for_repo_client = None
                if self._client.WSD:
                    wsd_url = self._href_definitions.get_wsd_base_href()
                    saved_model = self._client.repository._ml_repository_client.models.wsd_save(wsd_url, model_artifact,
                                                                                                meta_props, meta_props,
                                                                                                query_param=query_param_for_repo_client,
                                                                                                headers=self._client._get_headers())
                    return self.get_details(u'{}'.format(saved_model['asset_id']),ignore_warnings=True)
                else:
                    saved_model = self._client.repository._ml_repository_client.models.save(model_artifact,query_param_for_repo_client)
            except Exception as e:
                raise WMLClientError(u'Publishing model failed.', e)
            else:
                return self.get_details(saved_model.uid, ignore_warnings=True)

        elif tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath):
            if self._client.WSD:
                return self._wsd_publish_from_archive(model, meta_props)
            else:
                return self._publish_from_archive(model, meta_props)

        elif self._is_h5(model_filepath) and self.ConfigurationMetaNames.TYPE in meta_props and \
                meta_props[self.ConfigurationMetaNames.TYPE] == 'tensorflow_2.1' and (self._client.ICP_30 or self._client.CAMS):
            return self._store_tf21_model(model_filepath, meta_props)
        else:
            raise WMLClientError(u'Saving trained model in repository failed. \'{}\' file does not have valid format'.format(model_filepath))

    # TODO make this way when all frameworks will be supported
    # def _publish_from_archive(self, path_to_archive, meta_props=None):
    #     self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_NAME, STR_TYPE, True)
    #     self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_VERSION, STR_TYPE, True)
    #     self._validate_meta_prop(meta_props, self.ModelMetaNames.NAME, STR_TYPE, True)
    #
    #     try:
    #     try:
    #         meta_data = MetaProps(Repository._meta_props_to_repository_v3_style(meta_props))
    #
    #         model_artifact = MLRepositoryArtifact(path_to_archive, name=str(meta_props[self.ModelMetaNames.NAME]), meta_props=meta_data)
    #
    #         saved_model = self._ml_repository_client.models.save(model_artifact)
    #     except Exception as e:
    #         raise WMLClientError(u'Publishing model failed.', e)
    #     else:
    #         return self.get_details(u'{}'.format(saved_model.uid))
    def _create_model_payload(self, meta_props):
        payload = {
            "name": meta_props[self.ConfigurationMetaNames.NAME],
        }
        if self.ConfigurationMetaNames.TAGS in meta_props:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TAGS, list, False)
            payload.update({self.ConfigurationMetaNames.TAGS: meta_props[self.ConfigurationMetaNames.TAGS]})
        if self.ConfigurationMetaNames.SPACE_UID in meta_props and \
                meta_props[self._client.repository.ModelMetaNames.SPACE_UID] is not None:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SPACE_UID, STR_TYPE, False)
            payload.update({self.ConfigurationMetaNames.SPACE_UID: {
                "href": API_VERSION + SPACES + "/" + meta_props[self._client.repository.ModelMetaNames.SPACE_UID]}})
        if self._client.CAMS:
            if self._client.default_space_id is not None:
                meta_props[self._client.repository.ModelMetaNames.SPACE_UID] = {
                    "href": API_VERSION + SPACES + "/" + self._client.default_space_id}
            else:
                if self._client.default_project_id is not None:
                    payload.update({'project': {
                        "href":  "/v2/projects/" + self._client.default_project_id}})
                else:
                    raise WMLClientError(
                        "It is mandatory is set the space. Use client.set.default_space(<SPACE_GUID>) to set the space.")
        if self._client.WSD:
            if self._client.default_project_id is not None:
                payload.update({'project': {
                    "href": "/v2/projects/" + self._client.default_project_id}})
            else:
                raise WMLClientError(
                    "It is mandatory is set the project. Use client.set.default_project(<project id>) to set the project.")
        if self.ConfigurationMetaNames.RUNTIME_UID in meta_props:
            if not self._client.WSD:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.RUNTIME_UID, STR_TYPE, False)
            payload.update({self.ConfigurationMetaNames.RUNTIME_UID: {
                "href": API_VERSION + RUNTIMES + "/" + meta_props[self._client.repository.ModelMetaNames.RUNTIME_UID]}})
        if self.ConfigurationMetaNames.SOFTWARE_SPEC_UID in meta_props:
            if self._client.ICP_30:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                payload.update({self.ConfigurationMetaNames.SOFTWARE_SPEC_UID: {
                    "id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}})
            if self._client.WSD_20:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.SOFTWARE_SPEC_UID, STR_TYPE, False)
                payload.update({self.ConfigurationMetaNames.SOFTWARE_SPEC_UID: {
                    "base_id": meta_props[self.ConfigurationMetaNames.SOFTWARE_SPEC_UID]}})

        if self.ConfigurationMetaNames.PIPELINE_UID in meta_props:
            self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.PIPELINE_UID, STR_TYPE, False)
            if self._client.WSD:
                payload.update({self.ConfigurationMetaNames.PIPELINE_UID: {
                    "href": "/v2/assets/" + meta_props[self._client.repository.ModelMetaNames.PIPELINE_UID]}})
            else:
                payload.update({self.ConfigurationMetaNames.PIPELINE_UID: {
                    "href": API_VERSION + PIPELINES + "/" + meta_props[
                        self._client.repository.ModelMetaNames.PIPELINE_UID]}})

        if self._client.ICP_30 or self._client.WSD_20:
            if self.ConfigurationMetaNames.MODEL_DEFINITION_UID in meta_props:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.MODEL_DEFINITION_UID, STR_TYPE, False)
                payload.update({self.ConfigurationMetaNames.MODEL_DEFINITION_UID: {
                    "id": meta_props[self._client.repository.ModelMetaNames.MODEL_DEFINITION_UID]}})
        else:
            if self.ConfigurationMetaNames.TRAINING_LIB_UID in meta_props:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.TRAINING_LIB_UID, STR_TYPE, False)
                payload.update({self.ConfigurationMetaNames.TRAINING_LIB_UID: {
                    "href": API_VERSION + LIBRARIES + "/" + meta_props[
                        self._client.repository.ModelMetaNames.TRAINING_LIB_UID]}})

        if self.ConfigurationMetaNames.DESCRIPTION in meta_props:
            payload.update({'description': meta_props[self.ConfigurationMetaNames.DESCRIPTION]})

        # if self.ConfigurationMetaNames.LABEL_FIELD in meta_props and \
        #         meta_props[self.ConfigurationMetaNames.LABEL_FIELD] is not None:
        #     payload.update({'label_column': json.loads(meta_props[self.ConfigurationMetaNames.LABEL_FIELD])})

        if self.ConfigurationMetaNames.TYPE in meta_props:
            payload.update({'type': meta_props[self.ConfigurationMetaNames.TYPE]})

        if self.ConfigurationMetaNames.TRAINING_DATA_REFERENCES in meta_props\
                and meta_props[self.ConfigurationMetaNames.TRAINING_DATA_REFERENCES] is not None:
            payload.update(
                {'training_data_references': meta_props[self.ConfigurationMetaNames.TRAINING_DATA_REFERENCES]})

        if self.ConfigurationMetaNames.IMPORT in meta_props and\
                meta_props[self.ConfigurationMetaNames.IMPORT] is not None:
            payload.update({'import': meta_props[self.ConfigurationMetaNames.IMPORT]})
        if self.ConfigurationMetaNames.CUSTOM in meta_props and \
                meta_props[self.ConfigurationMetaNames.CUSTOM] is not None:
            payload.update({'custom': meta_props[self.ConfigurationMetaNames.CUSTOM]})
        if self.ConfigurationMetaNames.DOMAIN in meta_props and\
                meta_props[self.ConfigurationMetaNames.DOMAIN] is not None :
            payload.update({'domain': meta_props[self.ConfigurationMetaNames.DOMAIN]})

        if self.ConfigurationMetaNames.HYPER_PARAMETERS in meta_props and \
                meta_props[self.ConfigurationMetaNames.HYPER_PARAMETERS] is not None:
            payload.update({'hyper_parameters': meta_props[self.ConfigurationMetaNames.HYPER_PARAMETERS]})
        if self.ConfigurationMetaNames.METRICS in meta_props and \
                meta_props[self.ConfigurationMetaNames.METRICS] is not None:
            payload.update({'metrics': meta_props[self.ConfigurationMetaNames.METRICS]})

        input_schema = []
        output_schema = []
        if self.ConfigurationMetaNames.INPUT_DATA_SCHEMA in meta_props and \
                meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA] is not None:
            if self._client.ICP_30 or self._client.WSD_20:
                if isinstance(meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA], dict):
                    input_schema = [meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]]
                else:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.INPUT_DATA_SCHEMA, list, False)
                    input_schema = meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.INPUT_DATA_SCHEMA, dict, False)
                input_schema = [meta_props[self.ConfigurationMetaNames.INPUT_DATA_SCHEMA]]

        if self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA in meta_props and \
                meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA] is not None:
            if str(meta_props[self.ConfigurationMetaNames.TYPE]).startswith('do-') and \
                    (self._client.ICP_30 or self._client.WSD_20):
                try:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, dict, False)
                    output_schema = [meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]]
                except WMLClientError:
                    self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, list, False)
                    output_schema = meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]
            else:
                self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA, dict, False)
                output_schema = [meta_props[self.ConfigurationMetaNames.OUTPUT_DATA_SCHEMA]]

        if len(input_schema) != 0 or len(output_schema) != 0:
            payload.update({"schemas": {
                    "input": input_schema,
                    "output": output_schema}
                })
        return payload

    def _publish_from_archive(self, path_to_archive, meta_props=None,version=False,artifactid=None):
        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.NAME, STR_TYPE, True)
        def is_xml(model_filepath):
            return os.path.splitext(os.path.basename(model_filepath))[-1] == '.xml'

        url = self._href_definitions.get_published_models_href()
        payload = self._create_model_payload(meta_props)
        if(version==True):
            if not self._ICP:
                response = requests.put(
                    url+"/"+str_type_conv(artifactid),
                    json=payload,
                    params=self._client.params(),
                    headers=self._client._get_headers()
                )
            else:
                response = requests.put(
                    url+"/"+str_type_conv(artifactid),
                    json=payload,
                    params=self._client.params(),
                    headers=self._client._get_headers(),
                    verify=False
                )

        else:

            if not self._ICP:
                response = requests.post(
                    url,
                    json=payload,
                    headers=self._client._get_headers()
                    )
            else:
                response = requests.post(
                    url,
                    json=payload,
                    headers=self._client._get_headers(),
                    verify=False
                )

        result = self._handle_response(201, u'creating model', response)
        model_uid = self._get_required_element_from_dict(result, 'model_details', ['metadata', 'guid'])
        url = self._href_definitions.get_published_model_href(model_uid)+"/content"
        with open(path_to_archive, 'rb') as f:
            if is_xml(path_to_archive):
                if not self._ICP:
                    response = requests.put(
                       url,
                       data=f,
                       params=self._client._params(),
                       headers=self._client._get_headers(content_type='application/xml')
                    )
                else:
                    response = requests.put(
                        url,
                        data=f,
                        params=self._client._params(),
                        headers=self._client._get_headers(content_type='application/xml'),
                        verify=False
                    )
            else:
                if not self._ICP:
                    response = requests.put(
                        url,
                        data=f,
                        params=self._client._params(),
                        headers=self._client._get_headers(content_type='application/octet-stream')
                    )
                else:
                    response = requests.put(
                        url,
                        data=f,
                        params=self._client._params(),
                        headers=self._client._get_headers(content_type='application/octet-stream'),
                        verify=False
                    )
            if response.status_code != 200:
                self._delete(model_uid)
            self._handle_response(200, u'uploading model content', response, False)
            if(version==True):
                return self._client.repository.get_details(artifactid+"/versions/"+model_uid)
            return self.get_details(model_uid,ignore_warnings=True)

    def _wsd_publish_from_archive(self, path_to_archive, meta_props=None, artifactid=None):
        self._validate_meta_prop(meta_props, self.ConfigurationMetaNames.NAME, STR_TYPE, True)

        def is_xml(model_filepath):
            return os.path.splitext(os.path.basename(model_filepath))[-1] == '.xml'

        url = self._href_definitions.get_published_models_href()
        payload = self._create_model_payload(meta_props)

        return self._wsd_create_asset("wml_model", payload, meta_props, path_to_archive, True)

    def _print_deprecated_frameworks_msg(self, meta_props):
        if self.ConfigurationMetaNames.TYPE in meta_props:
            meta_type = meta_props[self.ConfigurationMetaNames.TYPE]
            if meta_type == 'scikit-learn_0.20' or meta_type == 'scikit-learn_0.22' or meta_type == 'scikit-learn_0.19':
               print("Note: {} with Python3.6 for Watson Machine Learning is deprecated and support will be discontinued in the future. Use scikit-learn 0.23 with default_py3.7 software specification instead. For details, see https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/wsj/analyze-data/pm_service_supported_frameworks.html.".format(meta_type))
            if meta_type == 'xgboost_0.80' or meta_type == 'xgboost_0.82' or meta_type == 'xgboost_0.90':
               print("Note: {} with Python3.6 for Watson Machine Learning is deprecated and support will be discontinued in the future. Use xgboost_0.90 with default_py3.7 software specification instead. For details, see https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/wsj/analyze-data/pm_service_supported_frameworks.html.".format(meta_type))
            if meta_type == 'tensorflow_1.15':
               print("Note: {} with Python3.6 for Watson Machine Learning is deprecated and support will be discontinued in the future. Use tensorflow_2.1 with default_py3.7 software specification instead. For details, see https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/wsj/analyze-data/pm_service_supported_frameworks.html.".format(meta_type))
            if meta_type == 'keras_2.2.5':
               print("Note: {} with Python3.6 for Watson Machine Learning is deprecated and support will be discontinued in the future. Use tensorflow_2.1 with default_py3.7 software specification instead. For details, see https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/wsj/analyze-data/pm_service_supported_frameworks.html.".format(meta_type))
            if meta_type == 'pytorch_1.2' or meta_type == 'pytorch-onnx_1.2':
               print("Note: {} with Python3.6 for Watson Machine Learning is deprecated and support will be discontinued in the future. Use pytorch_1.3 with default_py3.7 software specification instead. For details, see https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/wsj/analyze-data/pm_service_supported_frameworks.html.".format(meta_type))

    def store(self, model, meta_props=None, training_data=None, training_target=None, pipeline=None,version=False,artifactid=None, feature_names=None, label_column_names=None,subtrainingId=None):
        """g
        Store trained model into Watson Machine Learning repository on Cloud.

        :param model:  The train model object (e.g: spark PipelineModel), or path to saved model in format .tar.gz/.str/.xml or directory containing model file(s), or trained model guid
        :type model: object/{str_type}

        :param meta_props: meta data of the training definition. To see available meta names use:

            >>> client.models.ConfigurationMetaNames.get()

        :type meta_props: dict/{str_type}

        :param training_data:  Spark DataFrame supported for spark models. Pandas dataframe, numpy.ndarray or array supported for scikit-learn models
        :type training_data: spark dataframe, pandas dataframe, numpy.ndarray or array

        :param training_target: array with labels required for scikit-learn models
        :type training_target: array

        :param pipeline: pipeline required for spark mllib models
        :type training_target: object

        :returns: stored model details
        :rtype: dict

        The most simple use is:

        >>> stored_model_details = client.models.store(model, name)

        In more complicated cases you should create proper metadata, similar to this one:

        >>> metadata = {
        >>>        client.repository.ModelMetaNames.NAME: 'customer satisfaction prediction model',
        >>>        client.repository.ModelMetaNames.RUNTIME_UID: 'python',
        >>>        client.repository.ModelMetaNames.RUNTIME_VERSION: '3.5'
        >>>}

        where FRAMEWORK_NAME may be one of following: "spss-modeler", "tensorflow", "xgboost", "scikit-learn", "pmml".

        A way you might use me with local tar.gz containing model:

        >>> stored_model_details = client.models.store(path_to_tar_gz, meta_props=metadata, training_data=None)

        A way you might use me with local directory containing model file(s):

        >>> stored_model_details = client.models.store(path_to_model_directory, meta_props=metadata, training_data=None)

        A way you might use me with trained model guid:

        >>> stored_model_details = client.models.store(trained_model_guid, meta_props=metadata, training_data=None)
        """
        WMLResource._chk_and_block_create_update_for_python36(self)
        if self._client.CAMS and self._client.default_space_id is None and self._client.default_project_id is None:
            raise WMLClientError("It is mandatory is set the space or project. Use client.set.default_space(<SPACE_GUID>) to set the space or client.set.default_project(<PROJECT_GUID>).")
        if self._client.WSD and self._client.default_project_id is None:
            raise WMLClientError("It is mandatory is set the project. Use client.set.default_project(<PROJECT_GUID>).")

        model = str_type_conv(model)
        Models._validate_type(model, u'model', object, True)
        meta_props = copy.deepcopy(meta_props)
        meta_props = str_type_conv(meta_props)  # meta_props may be str, in this situation for py2 it will be converted to unicode
        Models._validate_type(meta_props, u'meta_props', [dict, STR_TYPE], True)
        # Repository._validate_type(training_data, 'training_data', object, False)
        # Repository._validate_type(training_target, 'training_target', list, False)
        meta_props_str_conv(meta_props)

        if type(meta_props) is STR_TYPE:
            meta_props = {
                self.ConfigurationMetaNames.NAME: meta_props
            }
        if self._client.CAMS:
            if self._client.default_space_id is not None:
                meta_props.update(
                    {self._client.repository.ModelMetaNames.SPACE_UID: self._client.default_space_id}
                    )
            if self._client.default_project_id is not None:
                meta_props.update(
                    {'project': {"href": "/v2/projects/" +self._client.default_project_id}}
                )
        if self._client.WSD:
            if self._client.default_project_id is not None:
                meta_props.update(
                    {'project': {"href": "/v2/projects/" +self._client.default_project_id}}
                )
            if "space" in meta_props:
                raise WMLClientError(
                    u'Invalid input SPACE_UID in meta_props. SPACE_UID not supported for WSD.')

        self.ConfigurationMetaNames._validate(meta_props)

        if 'mllib_2.3' in meta_props.get(self._client.repository.ModelMetaNames.RUNTIME_UID, '') \
                or 'mllib_2.3' in meta_props.get(self._client.repository.ModelMetaNames.TYPE, ''):
            raise WMLClientError("Spark 2.3 framework for Watson Machine Learning client is deprecated and will be removed on December 1, 2020. Use Spark 2.4 instead. For details, see https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/pm_service_supported_frameworks.html ")

        if ("frameworkName" in meta_props):
            framework_name = meta_props["frameworkName"].lower()
            if version == True and (framework_name == "mllib" or framework_name == "wml"):
                raise WMLClientError(u'Unsupported framework name: \'{}\' for creating a model version'.format(framework_name))
        if self._client.CAMS:
            if self._client.default_space_id is not None:
                meta_props["space"] = self._client.default_space_id

        if not isinstance(model, STR_TYPE):
            if(version==True):
                raise WMLClientError(u'Unsupported type: object for param model. Supported types: path to saved model, training ID')
            else:
                saved_model = self._publish_from_object(model=model, meta_props=meta_props, training_data=training_data, training_target=training_target, pipeline=pipeline, feature_names=feature_names, label_column_names=label_column_names)
        else:
            # print("model is a string type")
            if ((model.endswith('.pickle') or model.endswith('pipeline-model.json')) and os.path.sep in model):
                # AUTO AI Trained model
                # pipeline-model.json is needed for OBM + KB
                saved_model = self._store_autoAI_model(model_path=model, meta_props=meta_props, training_data=training_data, training_target=training_target, version=version, artifactId=artifactid, subtrainingId=subtrainingId)

            elif (os.path.sep in model) or os.path.isfile(model) or os.path.isdir(model):
                if not os.path.isfile(model) and not os.path.isdir(model):
                    raise WMLClientError(u'Invalid path: neither file nor directory exists under this path: \'{}\'.'.format(model))
                saved_model = self._publish_from_file(model=model, meta_props=meta_props, training_data=training_data, training_target=training_target,ver=version,artifactid=artifactid)
            else:
                 saved_model = self._publish_from_training(model_uid=model, meta_props=meta_props, training_data=training_data, training_target=training_target,version=version,artifactId=artifactid, subtrainingId=subtrainingId)
        if "system" in saved_model:
            print("Note: " + saved_model['system']['warnings'][0]['message'])

        if self._client.WSD:
            self._print_deprecated_frameworks_msg(meta_props)

        return saved_model



    def update(self, model_uid, meta_props=None, update_model=None):
        """
            Update existing model.

           **Parameters**

            #. **model_uid**:  UID of model which define what should be updated\n
               **type**: str\n

            #. **meta_props**:  New set of meta_props that needs to updated.\n
               **type**: dict\n

            #. **update_model**:  archived model content file or path to directory containing archived model file which should be changed for specific model_uid\n.
                                  This parameters is valid only for CP4D 3.0.0.
                                  A way you might use me with local directory containing model file(s):
               **type**: object or model\n

            :returns: updated metadata of model
            :rtype: dict

            A way you might use me is:

            >>> model_details = client.models.update(model_uid, update_model_content)
        """
        WMLResource._chk_and_block_create_update_for_python36(self)
        if self._client.WSD:
            raise WMLClientError('Update operation is not for IBM Watson Studio Desktop')
        Models._validate_type(model_uid, 'model_uid', STR_TYPE, True)
        Models._validate_type(meta_props, 'meta_props', dict, True)

        if meta_props is not None: # TODO
            #raise WMLClientError('Meta_props update unsupported.')
            self._validate_type(meta_props, u'meta_props', dict, True)
            meta_props_str_conv(meta_props)

            url = self._href_definitions.get_published_model_href(model_uid)

            if not self._ICP:
                response = requests.get(
                    url,
                    params=self._client._params(),
                    headers=self._client._get_headers()
                )
            else:
                response = requests.get(
                    url,
                    params=self._client._params(),
                    headers=self._client._get_headers(),
                    verify=False
                )

            if response.status_code != 200:
                if response.status_code == 404:
                    raise WMLClientError(
                        u'Invalid input. Unable to get the details of model_uid provided.')
                else:
                    raise ApiRequestFailure(u'Failure during {}.'.format("getting model to update"), response)

            details = self._handle_response(200, "Get model details", response)
            model_type = details['entity']['type']
            # update the content path for the Auto-ai model.
            if model_type == 'wml-hybrid_0.1' and update_model is not None:
                #TODO: check the condition combination is correct
                if not update_model.endswith('.pickle') and os.path.sep in update_model:
                    raise WMLClientError(
                        u'Invalid model content. The model content file should be ".pickle" file, for the model type\'{}\'.'.format(
                            model_type))
                else:
                    meta_props["import"]["location"]["path"] = update_model

            # with validation should be somewhere else, on the begining, but when patch will be possible
            patch_payload = self.ConfigurationMetaNames._generate_patch_payload(details['entity'], meta_props, with_validation=True)
            if not self._ICP:
                response_patch = requests.patch(url, json=patch_payload, params=self._client._params(),headers=self._client._get_headers())
            else:
                response_patch = requests.patch(url, json=patch_payload, params=self._client._params(),headers=self._client._get_headers(),verify=False)
            updated_details = self._handle_response(200, u'model version patch', response_patch)
            if self._client.ICP_30 and update_model is not None:
                self._update_model_content(model_uid, details, update_model)
            return updated_details

        return self.get_details(model_uid,ignore_warnings=True)


    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def load(self, artifact_uid):
        """
        Load model from repository to object in local environment.

        :param artifact_uid:  stored model UID
        :type artifact_uid: {str_type}

        :returns: trained model
        :rtype: object

        A way you might use me is:

        >>> model = client.models.load(model_uid)
        """
        if self._client.WSD:
            raise WMLClientError('Load model operation is not supported in IBM Watson Studio Desktop.')
        artifact_uid = str_type_conv(artifact_uid)
        Models._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, True)
        # check if this is tensorflow 2.1 model type
        if self._client.CAMS or self._client.ICP_30:
            model_details = self.get_details(artifact_uid)
            if model_details.get('entity').get('type') == 'tensorflow_2.1':
                return self._tf21_load_model_instance(artifact_uid)
        try:
            if self._client.CAMS:
                if self._client.default_space_id is None and self._client.default_project_id is None:
                    raise WMLClientError(
                        "It is mandatory is set the space or project. \
                        Use client.set.default_space(<SPACE_GUID>) to set the space or client.set.default_project(<PROJECT_GUID>).")
                else:
                    if self._client.default_project_id is not None:
                        loaded_model = self._client.repository._ml_repository_client.models.get(artifact_uid,
                                                                                                project_id=self._client.default_project_id)
                    else:
                        loaded_model = self._client.repository._ml_repository_client.models.get(artifact_uid, space_id=self._client.default_space_id)
            else:
                loaded_model = self._client.repository._ml_repository_client.models.get(artifact_uid)
            loaded_model = loaded_model.model_instance()
            self._logger.info(u'Successfully loaded artifact with artifact_uid: {}'.format(artifact_uid))
            return loaded_model
        except Exception as e:
            raise WMLClientError(u'Loading model with artifact_uid: \'{}\' failed.'.format(artifact_uid), e)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def download(self, model_uid, filename='downloaded_model.tar.gz', rev_uid=None):
        """
            Download model from repository to local file.

            :param model_uid: stored model UID
            :type model_uid: {str_type}

            :param filename: name of local file to create (optional)
            :type filename: {str_type}

            :param rev_uid:  Revision id. Applicable only for Cloud Pak For Data 3.0 onwards \n
            :type rev_uid: {str_type}


            A way you might use is:

            >>> client.models.download(model_uid, 'my_model.tar.gz')
        """
        if os.path.isfile(filename):
            raise WMLClientError(u'File with name: \'{}\' already exists.'.format(filename))
        if rev_uid is not None and self._client.ICP_30 is None:
            raise WMLClientError(u'Applicable only for Cloud Pak For Data 3.0 onwards')

        model_uid = str_type_conv(model_uid)
        Models._validate_type(model_uid, u'model_uid', STR_TYPE, True)
        filename = str_type_conv(filename)
        Models._validate_type(filename, u'filename', STR_TYPE, True)

        artifact_url = self._href_definitions.get_model_last_version_href(model_uid)

        try:
            if self._client.WSD:
                import urllib
                #model_details = self.get_details(model_uid)
                model_get_response = requests.get(self._href_definitions.get_data_asset_href(model_uid),
                                              params=self._client._params(),
                                              headers=self._client._get_headers())

                model_details = self._handle_response(200, u'get model', model_get_response)
                attachment_url = model_details['attachments'][0]['object_key']
                artifact_content_url = self._href_definitions.get_wsd_model_attachment_href() + \
                                       urllib.parse.quote('wml_model/' + attachment_url, safe='')
            else:
                artifact_content_url = str(artifact_url + u'/content')
            if not self._client.ICP and not self._client.WSD:
                r = requests.get(artifact_content_url, params=self._client._params(),headers=self._client._get_headers(), stream=True)
            else:
                params = self._client._params()
                if rev_uid is not None:
                    params.update({'revision_id': rev_uid})
                r = requests.get(artifact_content_url, params=params,headers=self._client._get_headers(), stream=True, verify=False)
            if r.status_code != 200:
                raise ApiRequestFailure(u'Failure during {}.'.format("downloading model"), r)

            downloaded_model = r.content
            self._logger.info(u'Successfully downloaded artifact with artifact_url: {}'.format(artifact_url))
        except WMLClientError as e:
            raise e
        except Exception as e:
            raise WMLClientError(u'Downloading model with artifact_url: \'{}\' failed.'.format(artifact_url), e)

        try:
            with open(filename, 'wb') as f:
                f.write(downloaded_model)
            print(u'Successfully saved model content to file: \'{}\''.format(filename))
            return os.getcwd() + "/"+filename
        except IOError as e:
            raise WMLClientError(u'Saving model with artifact_url: \'{}\' failed.'.format(filename), e)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, model_uid):
        """
            Delete model from repository.

            :param model_uid: stored model UID
            :type model_uid: {str_type}

            A way you might use me is:

            >>> client.models.delete(model_uid)
        """
        model_uid = str_type_conv(model_uid)
        Models._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        if self._client.WSD:
            model_endpoint = self._href_definitions.get_model_definition_assets_href() + "/" + model_uid
        else:
            model_endpoint = self._href_definitions.get_published_model_href(model_uid)

        self._logger.debug(u'Deletion artifact model endpoint: {}'.format(model_endpoint))
        if not self._ICP and not self._client.WSD:
            response_delete = requests.delete(model_endpoint, params=self._client._params(),headers=self._client._get_headers())
        else:
            #check if the model as a corresponding deployment
            if not self._client.WSD and self._if_deployment_exist_for_asset(model_uid):
                raise WMLClientError(u'Cannot delete model that has existing deployments. Please delete all associated deployments and try again')
            response_delete = requests.delete(model_endpoint, params=self._client._params(),headers=self._client._get_headers(), verify=False)
        return self._handle_response(204, u'model deletion', response_delete, False)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def _delete(self, model_uid):

        model_uid = str_type_conv(model_uid)
        Models._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        if self._client.WSD:
            model_endpoint = self._href_definitions.get_model_definition_assets_href() + "/" + model_uid
        else:
            model_endpoint = self._href_definitions.get_published_model_href(model_uid)

        self._logger.debug(u'Deletion artifact model endpoint: {}'.format(model_endpoint))
        if not self._ICP and not self._client.WSD:
            response_delete = requests.delete(model_endpoint, params=self._client._params(),
                                              headers=self._client._get_headers())
        else:
            response_delete = requests.delete(model_endpoint, params=self._client._params(),
                                              headers=self._client._get_headers(), verify=False)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, model_uid=None, limit=None, ignore_warnings=False):
        """
           Get metadata of stored models. If model uid is not specified returns all models metadata.

           :param model_uid: stored model, definition or pipeline UID (optional)
           :type model_uid: {str_type}

           :param limit: limit number of fetched records (optional)
           :type limit: int

           :returns: stored model(s) metadata
           :rtype: dict

           A way you might use me is:

           >>> model_details = client.models.get_details(model_uid)
           >>> models_details = client.models.get_details()
        """
        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        model_uid = str_type_conv(model_uid)
        Models._validate_type(model_uid, u'model_uid', STR_TYPE, False)
        Models._validate_type(limit, u'limit', int, False)

        if not self._ICP:
            if self._client.WSD:
                url = self._href_definitions.get_model_definition_assets_href()
                response = self._get_artifact_details(url, model_uid, limit, 'models')
                return self._wsd_get_required_element_from_response(response)
            else:
                url = self._href_definitions.get_published_models_href()
        else:
            url = self._href_definitions.get_published_models_href()
        details = self._get_artifact_details(url, model_uid, limit, 'models')
        if 'system' in details and ignore_warnings is False:
            print("Note: " + details['system']['warnings'][0]['message'])
        return details

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_href(model_details):
        """
            Get url of stored model.

            :param model_details:  stored model details
            :type model_details: dict

            :returns: url to stored model
            :rtype: {str_type}

            A way you might use me is:

            >>> model_url = client.models.get_href(model_details)
        """

        Models._validate_type(model_details, u'model_details', object, True)

        if 'asset_id' in model_details['metadata']:
            return WMLResource._get_required_element_from_dict(model_details, u'model_details', [u'metadata', u'href'])
        else:
            Models._validate_type_of_details(model_details, MODEL_DETAILS_TYPE)
            return WMLResource._get_required_element_from_dict(model_details, u'model_details', [u'metadata', u'href'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(model_details):
        """
            Get uid of stored model.

            :param model_details:  stored model details
            :type model_details: dict

            :returns: uid of stored model
            :rtype: {str_type}

            A way you might use me is:

            >>> model_uid = client.models.get_uid(model_details)
        """
        Models._validate_type(model_details, u'model_details', object, True)

        if 'asset_id' in model_details['metadata']:
            return WMLResource._get_required_element_from_dict(model_details, u'model_details', [u'metadata', u'asset_id'])
        else:
            Models._validate_type_of_details(model_details, MODEL_DETAILS_TYPE)
            return WMLResource._get_required_element_from_dict(model_details, u'model_details', [u'metadata', u'guid'])

    def list(self, limit=None):
        """
           List stored models. If limit is set to None there will be only first 50 records shown.

           :param limit: limit number of fetched records (optional)
           :type limit: int

           A way you might use me is

           >>> client.models.list()
        """
        ##For CP4D, check if either spce or project ID is set
        if self._client.WSD:
            self._wsd_list(limit)
        else:
            self._client._check_if_either_is_set()
            model_resources = self.get_details(limit=limit)[u'resources']
            model_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], m[u'entity'][u'type']) for m in model_resources]

            self._list(model_values, [u'GUID', u'NAME', u'CREATED', u'TYPE'], limit, _DEFAULT_LIST_LENGTH)


    def _wsd_list(self, limit=None):

        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        href = self._href_definitions.get_wsd_asset_search_href("wml_model")
        if limit is None:
            data = {
                "query": "*:*"
            }
        else:
            Models._validate_type(limit, u'limit', int, False)
            data = {
                "query": "*:*",
                "limit": limit
            }

        response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(),
                                     json=data, verify=False)
        self._handle_response(200, u'model list', response)
        asset_details = self._handle_response(200, u'model list', response)["results"]
        model_def_values = [
            (m[u'metadata'][u'name'], m[u'metadata'][u'asset_type'], m[u'metadata'][u'asset_id']) for
            m in asset_details]

        self._list(model_def_values, [u'NAME', u'ASSET_TYPE', u'GUID'], limit, _DEFAULT_LIST_LENGTH)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def create_revision(self, model_uid):
        """
           Creates revision for the given model uid.

           :param model_uid: stored model UID
           :type model_uid: {str_type}

           :returns: stored model revisions metadata
           :rtype: dict

           >>> model_details = client.models.create_revision(model_uid)
        """
        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        model_uid = str_type_conv(model_uid)
        Models._validate_type(model_uid, u'model_uid', STR_TYPE, False)

        if self._client.ICP_30 is None:
            raise WMLClientError(
                u'Revisions APIs are not supported in this release.')
        else:
            url = self._href_definitions.get_published_models_href()
            return self._create_revision_artifact(url, model_uid, 'models')

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def list_revisions(self, model_uid, limit=None):
        """
           List all revision for the given model uid.

           :param model_uid: Unique id of stored model.
           :type model_uid: {str_type}

           :param limit: limit number of fetched records (optional)
           :type limit: int

           :returns: stored model revisions details
           :rtype: table

           >>> client.models.list_revisions(model_uid)
        """
        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        model_uid = str_type_conv(model_uid)

        Models._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        if self._client.ICP_30 is None:
            raise WMLClientError(
                u'Revision APIs are not supported in this release.')
        else:
            url = self._href_definitions.get_published_models_href() + "/" + model_uid
            model_resources = self._get_artifact_details(url, "revisions", limit, 'model revisions')[u'resources']
            model_values = [
                (m[u'metadata'][u'rev'], m[u'metadata'][u'name'], m[u'metadata'][u'created_at']) for m in
                model_resources]

            self._list(model_values, [u'GUID', u'NAME', u'CREATED'], limit, _DEFAULT_LIST_LENGTH)

    def get_revision_details(self, model_uid, rev_uid):
        """
           Get metadata of stored models specific revision.

           :param model_uid: stored model, definition or pipeline UID (optional)
           :type model_uid: {str_type}

           :param rev_uid: Unique Id of the stored model revision
           :type rev_uid: int

           :returns: stored model(s) metadata
           :rtype: dict

           A way you might use me is:

           >>> model_details = client.models.get_revision_details(model_uid, rev_uid)
        """
        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()
        model_uid = str_type_conv(model_uid)
        Models._validate_type(model_uid, u'model_uid', STR_TYPE, True)
        Models._validate_type(rev_uid, u'rev_uid', int, True)
       # Models._validate_type(limit, u'limit', int, False)

        if not self._client.ICP_30:
            raise WMLClientError(
                'Revision APIs are not supported in this release.')
        else:
            url = self._href_definitions.get_published_models_href() + "/" + model_uid
            return self._get_with_or_without_limit(url, limit=None, op_name="model",
                                                   summary=None, pre_defined=None, revision=rev_uid)

    def _update_model_content(self, model_uid, updated_details, update_model):

        model = str_type_conv(update_model)
        model_type = updated_details['entity']['type']

        def is_xml(model_filepath):
            if (os.path.splitext(os.path.basename(model_filepath))[-1] == '.pmml'):
                raise WMLClientError(
                    'The file name has an unsupported extension. Rename the file with a .xml extension.')
            return os.path.splitext(os.path.basename(model_filepath))[-1] == '.xml'

        import tarfile
        import zipfile
        model_filepath = model

        if 'scikit-learn_' in model_type or 'mllib_' in model_type:
            meta_props = updated_details['entity']
            meta_data = MetaProps(self._client.repository._meta_props_to_repository_v3_style(meta_props))
            name = updated_details['entity']['name']
            model_artifact = MLRepositoryArtifact(update_model, name=name,
                                                  meta_props=meta_data, training_data=None)
            model_artifact.uid = model_uid
            self._client.repository._ml_repository_client.models.upload_content(model_artifact,
                                                                                query_param=self._client._params())
        else:
            if (os.path.sep in update_model) or os.path.isfile(update_model) or os.path.isdir(update_model):
                if not os.path.isfile(update_model) and not os.path.isdir(update_model):
                    raise WMLClientError(
                        u'Invalid path: neither file nor directory exists under this path: \'{}\'.'.format(model))

            if os.path.isdir(model):
                if "tensorflow" in model_type:
                    # TODO currently tar.gz is required for tensorflow - the same ext should be supported for all frameworks
                    if os.path.basename(model) == '':
                        model = os.path.dirname(update_model)
                    filename = os.path.basename(update_model) + '.tar.gz'
                    current_dir = os.getcwd()
                    os.chdir(model)
                    target_path = os.path.dirname(model)

                    with tarfile.open(os.path.join('..', filename), mode='w:gz') as tar:
                        tar.add('.')

                    os.chdir(current_dir)
                    model_filepath = os.path.join(target_path, filename)
                    if tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath) or is_xml(model_filepath):
                        path_to_archive = model_filepath
                else:
                    if 'caffe' in model_type:
                        raise WMLClientError(u'Invalid model file path  specified for: \'{}\'.'.format(model_type))
                    loaded_model = load_model_from_directory(model_type, model)
                    path_to_archive = loaded_model
            elif is_xml(model_filepath):
                 path_to_archive = model_filepath
            elif tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath):
                 path_to_archive = model_filepath

            else:
                raise WMLClientError(
                    u'Saving trained model in repository failed. \'{}\' file does not have valid format'.format(
                        model_filepath))

            url = self._href_definitions.get_published_model_href(model_uid) + "/content"
            with open(path_to_archive, 'rb') as f:
                if is_xml(path_to_archive):
                    if not self._ICP:
                        response = requests.put(
                            url,
                            data=f,
                            params=self._client._params(),
                            headers=self._client._get_headers(content_type='application/xml')
                        )
                    else:
                        response = requests.put(
                            url,
                            data=f,
                            params=self._client._params(),
                            headers=self._client._get_headers(content_type='application/xml'),
                            verify=False
                        )
                else:
                    if not self._ICP:
                        response = requests.put(
                            url,
                            data=f,
                            params=self._client._params(),
                            headers=self._client._get_headers(content_type='application/octet-stream')
                        )
                    else:
                        response = requests.put(
                            url,
                            data=f,
                            params=self._client._params(),
                            headers=self._client._get_headers(content_type='application/octet-stream'),
                            verify=False
                        )
                self._handle_response(200, u'uploading model content', response, False)


    def _is_h5(self, model_filepath):
        return os.path.splitext(os.path.basename(model_filepath))[-1] == '.h5'

    def _tf21_load_model_instance(self, model_id):
        artifact_url = self._href_definitions.get_model_last_version_href(model_id)
        params = self._client._params()
        id_length = 20
        gen_id = uid_generate(id_length)
        verify = True
        if self._client.ICP_30 or self._client.CAMS:
            verify = False

        # Step1 :  Download the model content

        url = self._href_definitions.get_published_model_href(model_id)
        # params.update({'content_format': 'native'})
        # artifact_content_url = str(artifact_url + u'/download')
        artifact_content_url = str(artifact_url + u'/content')
        r = requests.get(artifact_content_url, params=params,
                         headers=self._client._get_headers(), stream=True,
                         verify=verify)

        if r.status_code != 200:
            raise ApiRequestFailure(u'Failure during {}.'.format("downloading model"), r)

        downloaded_model = r.content
        self._logger.info(u'Successfully downloaded artifact with artifact_url: {}'.format(artifact_url))

        # Step 2 :  copy the downloaded tar.gz in to a temp folder
        try:
            temp_dir_name = '{}'.format('hdfs' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            gz_filename = temp_dir + "/download.tar.gz"
            tar_filename = temp_dir + "/download.tar"
            with open(gz_filename, 'wb') as f:
                f.write(downloaded_model)

        except IOError as e:
            raise WMLClientError(u'Saving model with artifact_url: \'{}\' failed.'.format(model_id), e)

        # create model instance based on the type using load_model
        try:
            CompressionUtil.decompress_file_gzip(gzip_filepath=gz_filename, filepath=tar_filename)
            CompressionUtil.extract_tar(tar_filename, temp_dir)
            os.remove(tar_filename)
            import tensorflow as tf
            import glob
            h5format = True
            if not glob.glob(temp_dir + '/sequential_model.h5'):
                h5format = False
            if h5format is True:
                model_instance = tf.keras.models.load_model(temp_dir + '/sequential_model.h5', custom_objects=None,
                                                            compile=True)
                return model_instance
            elif glob.glob(temp_dir + '/saved_model.pb'):
                model_instance = tf.keras.models.load_model(temp_dir, custom_objects=None, compile=True)
                return model_instance
            else:
                raise WMLClientError(u'Load model with artifact_url: \'{}\' failed.'.format(model_id), e)

        except IOError as e:
            raise WMLClientError(u'Saving model with artifact_url: \'{}\' failed.'.format(model_id), e)

    def _store_tf21_model(self, model, meta_props):
        # Model type is
        import tensorflow as tf
        url = self._href_definitions.get_published_models_href()
        id_length = 20
        gen_id = uid_generate(id_length)

        tf_meta = None
        options = None
        signature = None
        save_formats = None
        include_optimizer = None
        if 'tf_model_params' in meta_props and meta_props[self.ConfigurationMetaNames.TF_MODEL_PARAMS] is not None:
            tf_meta = copy.deepcop(meta_props[self.ConfigurationMetaNames.TF_MODEL_PARAMS])
            save_formats = tf_meta.get('save_formats')
            options = tf_meta.get('options')
            signature = tf_meta.get('signature')
            include_optimizer = tf_meta.get('include_optimizer')

        if "tensorflow.python.keras.engine.training.Model" in str(type(model)):
            if save_formats is not None and save_formats == 'h5':
                raise WMLClientError(
                    "Invalid save format value provided in tf_model_params to save model, provide 'tf' as the value. ")

            temp_dir_name = '{}'.format('pb' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            import tensorflow as tf
            tf.saved_model.save(model, temp_dir,
                                signatures=signature, options=options)
            ##tf.saved_model.save(model, temp_dir)

        elif "tensorflow.python.keras.engine.sequential.Sequential" in str(type(model)):
            if save_formats is not None and save_formats == 'tf':
                raise WMLClientError("Invalid save format value provided in tf_model_params to save Sequential model "
                                     "Please provide h5 as value for save_formats")

            temp_dir_name = '{}'.format('hdfs' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            model_file = temp_dir + "/sequential_model.h5"
            tf.keras.models.save_model(
                model, model_file, include_optimizer=include_optimizer, save_format='h5',
                signatures=None, options=options)
        elif isinstance(model, STR_TYPE) and os.path.splitext(os.path.basename(model))[-1] == '.h5':
            temp_dir_name = '{}'.format('hdfs' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                import shutil
                os.makedirs(temp_dir)
                shutil.copy2(model, temp_dir)
        else:

            raise WMLClientError(
                'Saving the tensorflow model requires the model of either tf format or h5 format for Sequential model.'
            )

        path_to_archive = self._model_content_compress_artifact(temp_dir_name, temp_dir)
        if self._client.ICP_30 or self._client.ICP:
            verify = False
        else:
            verify = True

        payload = copy.deepcopy(meta_props)
        if self._client.CAMS and self._client.wml_credentials['version'] == '2.5.0':
            params = None
        else:
            params = self._client._params()
        # params = self._client._params()

        # payload = self._create_model_payload(meta_props)
        response = requests.post(
            url,
            json=payload,
            params=params,
            headers=self._client._get_headers(),
            verify=verify
        )
        result = self._handle_response(201, u'creating model', response)
        model_uid = self._get_required_element_from_dict(result, 'model_details', ['metadata', 'id'])

        url = self._href_definitions.get_published_model_href(model_uid) + "/content"

        with open(path_to_archive, 'rb') as f:
            if self._client.CAMS and self._client.wml_credentials['version'] == '2.5.0':
                # qparams = None
                qparams = self._client._params()
            else:
                qparams = self._client._params()
                qparams.update({'content_format': 'native'})
                qparams.update({'version': '2019-10-25'})


            model_type = meta_props[self.ConfigurationMetaNames.TYPE]
            # update the content path for the Auto-ai model.

            response = requests.put(
                url,
                data=f,
                params=qparams,
                headers=self._client._get_headers(content_type='application/octet-stream'),
                verify=False
            )
            if response.status_code != 200 and response.status_code != 201:
                self._delete(model_uid)

            self._handle_response(200, u'uploading model content', response, False)

            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                os.remove(path_to_archive)
            return self.get_details(model_uid, ignore_warnings=True)

    def _model_content_compress_artifact(self, type_name, compress_artifact):
        tar_filename = '{}_content.tar'.format(type_name)
        gz_filename = '{}.gz'.format(tar_filename)
        CompressionUtil.create_tar(compress_artifact, '.', tar_filename)
        CompressionUtil.compress_file_gzip(tar_filename, gz_filename)
        os.remove(tar_filename)
        return gz_filename

    def _wsd_get_tf21_model(self, model, meta_props):
        # Model type is
        import tensorflow as tf
        url = self._href_definitions.get_published_models_href()
        id_length = 20
        gen_id = uid_generate(id_length)

        tf_meta = None
        options = None
        signature = Noneq
        save_formats = None
        include_optimizer = None
        if 'tf_model_params' in meta_props and meta_props[self.ConfigurationMetaNames.TF_MODEL_PARAMS] is not None:
            tf_meta = copy.deepcop(meta_props[self.ConfigurationMetaNames.TF_MODEL_PARAMS])
            save_formats = tf_meta.get('save_formats')
            options = tf_meta.get('options')
            signature = tf_meta.get('signature')
            include_optimizer = tf_meta.get('include_optimizer')

        if "tensorflow.python.keras.engine.training.Model" in str(type(model)):
            if save_formats is not None and save_formats == 'h5':
                raise WMLClientError(
                    "Invalid save format value provided in tf_model_params to save model, provide 'tf' as the value. ")

            temp_dir_name = '{}'.format('pb' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            import tensorflow as tf
            tf.saved_model.save(model, temp_dir,
                                signatures=signature, options=options)
            ##tf.saved_model.save(model, temp_dir)

        elif "tensorflow.python.keras.engine.sequential.Sequential" in str(type(model)):
            if save_formats is not None and save_formats == 'tf':
                raise WMLClientError("Invalid save format value provided in tf_model_params to save Sequential model "
                                     "Please provide h5 as value for save_formats")

            temp_dir_name = '{}'.format('hdfs' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            model_file = temp_dir + "/sequential_model.h5"
            tf.keras.models.save_model(
                model, model_file, include_optimizer=include_optimizer, save_format='h5',
                signatures=None, options=options)
        elif isinstance(model, STR_TYPE) and os.path.splitext(os.path.basename(model))[-1] == '.h5':
            temp_dir_name = '{}'.format('hdfs' + gen_id)
            # temp_dir = os.path.join('.', temp_dir_name)
            temp_dir = temp_dir_name
            if not os.path.exists(temp_dir):
                import shutil
                os.makedirs(temp_dir)
                shutil.copy2(model, temp_dir)
        else:

            raise WMLClientError(
                'Saving the tensorflow model requires the model of either tf format or h5 format for Sequential model.'
            )

        path_to_archive = self._model_content_compress_artifact(temp_dir_name, temp_dir)
        return path_to_archive