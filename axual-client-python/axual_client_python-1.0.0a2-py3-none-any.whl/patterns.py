# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
GROUP_PLACEHOLDER = '{group}'
ENVIRONMENT_PLACEHOLDER = '{environment}'
INSTANCE_PLACEHOLDER = '{instance}'
TENANT_PLACEHOLDER = '{tenant}'
TOPIC_PLACEHOLDER = '{topic}'

# Move those on another class maybe
GROUP_KEY = 'group'
ENVIRONMENT_KEY = 'environment'
INSTANCE_KEY = 'instance'
TENANT_KEY = 'tenant'
TOPIC_KEY = 'topic'
TOPIC_PATTERN_KEY = 'topic.pattern'
GROUP_PATTERN_KEY = 'group.id.pattern'


def resolve_topic(discovery_result: dict, topic: str) -> str:
    return discovery_result[TOPIC_PATTERN_KEY] \
        .replace(TENANT_PLACEHOLDER, discovery_result[TENANT_KEY]) \
        .replace(INSTANCE_PLACEHOLDER, discovery_result[INSTANCE_KEY]) \
        .replace(ENVIRONMENT_PLACEHOLDER, discovery_result[ENVIRONMENT_KEY]) \
        .replace(TOPIC_PLACEHOLDER, topic)


def resolve_group(discovery_result: dict, group: str) -> str:
    return discovery_result[GROUP_PATTERN_KEY] \
            .replace(TENANT_PLACEHOLDER, discovery_result[TENANT_KEY]) \
            .replace(INSTANCE_PLACEHOLDER, discovery_result[INSTANCE_KEY]) \
            .replace(ENVIRONMENT_PLACEHOLDER, discovery_result[ENVIRONMENT_KEY]) \
            .replace(GROUP_PLACEHOLDER, group)
