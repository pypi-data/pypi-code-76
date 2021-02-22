# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

CLOUDML_MEMORY_UNITS = ["K", "M", "G"]
QUOTA_ACCURACY_PLACE = 2
ENABLE_GPU_TYPE_SELECT = False
GPULIST = ["m40", "p40", "k40", "p4", "v100"]
DEV_PROXY_PROTOCOL = {8888: "JUPYTER", 22: "TCP"}
DEV_PROXY_MIN_CONTAINER_PORT = 1
DEV_PROXY_MAX_CONTAINER_PORT = 65535
PRI_RANK = ["1", "2", "3"]
CLOUDML_SHARED_BUCKET = "cloudmlusers"

