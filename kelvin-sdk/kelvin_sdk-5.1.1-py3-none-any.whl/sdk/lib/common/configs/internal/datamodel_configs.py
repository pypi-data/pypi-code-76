"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""


class DatamodelConfigs:
    datamodel_default_icd_extension: str = ".yml"
    datamodel_default_version: str = "0.0.1"
    datamodel_name_acceptance_regex: str = r"^([a-z][a-z0-9_]+\.)+[a-z][a-z0-9_]+$"
    datamodel_class_name_acceptance_regex: str = r"^[a-zA-Z][a-zA-Z0-9_]+$"
