# Copyright 2020 Tobias Höfer
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
# =============================================================================
"""GPU-Utils to show all available GPUs and explicitly select a given GPU.
"""
import tensorflow as tf


def info():
    """Lists all GPUs.
    """
    print("Num GPUs Available: ",
          len(tf.config.experimental.list_physical_devices('GPU')))


def only_use_gpu(gpu_id, memory_growth=True):
    """Select a GPU by its ID to selectively use a specific GPU for training.
    Args:
        gpu_id (int): GPU by its numeric ID.
    """
    device = tf.config.list_physical_devices('GPU')[gpu_id]
    tf.config.experimental.set_visible_devices(device, 'GPU')
    if memory_growth:
        tf.config.experimental.set_memory_growth(device, True)
