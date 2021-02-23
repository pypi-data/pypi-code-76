# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Collection of kernel functions to be used by the
hyperparameter optimizations.
"""

exp = "exp"
"""
An exponential kernel yielding non-differentiable
sample paths.
"""

gauss = "gauss"
"""
A Gaussian kernel yielding analytic
(infinitely--differentiable) sample paths.
"""

matern32 = "matern32"
"""
A Matérn 3/2 kernel yielding once-differentiable
sample paths.
"""

matern52 = "matern52"
"""
A Matérn 5/2 kernel yielding twice-differentiable
sample paths.
"""


_all_kernels = [matern32, matern52, exp, gauss]
