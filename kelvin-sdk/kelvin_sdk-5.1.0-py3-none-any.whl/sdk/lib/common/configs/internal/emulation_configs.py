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
from dataclasses import dataclass
from typing import List


@dataclass
class StudioConfigs:
    host: str = "localhost"
    port: int = 8000
    default_port: int = 8000
    studio_schema_file_bind: str = "{schema_file_path}:/opt/kelvin/app/server/data/{schema_file_name}:Z"
    studio_input_file_bind: str = "{input_file_path}:/opt/kelvin/app/server/data/{input_file_name}:Z"

    def get_port_mapping(self) -> List[str]:
        return [f"{self.port}:{self.port}"]

    def get_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def is_port_open(self) -> bool:
        from kelvin.sdk.lib.common.utils.general_utils import is_port_open

        return is_port_open(host=self.host, port=self.port)
