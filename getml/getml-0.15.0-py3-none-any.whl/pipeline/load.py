# Copyright 2020 The SQLNet Company GmbH

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

from getml.data import Placeholder

from .pipeline import Pipeline

def load(name):
    """Loads a pipeline from the getML engine into Python.

    Args:
        name: The name of the pipeline to be loaded.

    Returns:
        A :meth:`~getml.pipeline.Pipeline` that is a handler
        for the pipeline signified by name.
    """
    # This will be overwritten by .refresh(...) anyway
    dummy = Placeholder(name="dummy")
    dummy2 = Placeholder(name="dummy2")
    dummy.join(dummy2, join_key="join_key")

    pipeline = Pipeline(
        population=dummy,
        peripheral=dummy2
    )
    pipeline._name = name

    return pipeline.refresh()

