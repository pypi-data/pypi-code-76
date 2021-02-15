# Copyright 2020 The TensorFlow Probability Authors.
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
# ============================================================================
"""Sinh bijector."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_probability.python.internal.backend.numpy.compat import v2 as tf
from tensorflow_probability.substrates.numpy import math as tfp_math
from tensorflow_probability.substrates.numpy.bijectors import bijector


__all__ = [
    "Sinh",
]


class Sinh(bijector.Bijector):
  """Bijector that computes `Y = sinh(X)`.

  #### Examples

  ```python
  bijector.Sinh().forward(x=[[1., 0], [3, 2]])
  # Result: [[1.1752012, 0.], [10.017875, 3.6268604]], i.e., sinh(x)

  bijector.Sinh().inverse(y=[[1., 0], [3, 2]])
  # Result: [[0.8813736, 0.], [1.8184465, 1.4436355]], i.e., asinh(y).
  ```
  """

  def __init__(self, validate_args=False, name="sinh"):
    parameters = dict(locals())
    with tf.name_scope(name) as name:
      super(Sinh, self).__init__(
          forward_min_event_ndims=0,
          validate_args=validate_args,
          parameters=parameters,
          name=name)

  @classmethod
  def _is_increasing(cls):
    return True

  @classmethod
  def _parameter_properties(cls, dtype):
    return dict()

  def _forward(self, x):
    return tf.sinh(x)

  def _inverse(self, y):
    return tf.asinh(y)

  # We implicitly rely on _forward_log_det_jacobian rather than explicitly
  # implement _inverse_log_det_jacobian because directly using
  # `-0.5 * math.log1psquare(y)` has lower numerical precision.
  def _forward_log_det_jacobian(self, x):
    return tfp_math.log_cosh(x)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# This file is auto-generated by substrates/meta/rewrite.py
# It will be surfaced by the build system as a symlink at:
#   `tensorflow_probability/substrates/numpy/bijectors/sinh.py`
# For more info, see substrate_runfiles_symlinks in build_defs.bzl
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# (This notice adds 10 to line numbering.)


