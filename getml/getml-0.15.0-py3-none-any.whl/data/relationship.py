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
Marks the relationship between joins in :class:`~getml.data.Placeholder`
"""


many_to_many = "many-to-many"
"""Used for one-to-many or many-to-many relationships.

When there is such a relationship, feature learning
is necessary and meaningful. If you mark a join as
a default relationship, but that assumption is violated
for the training data, the pipeline will raise a
warning.
"""

many_to_one = "many-to-one"
"""Used for many-to-one relationships.

If two tables are guaranteed to be in a
many-to-one relationship, then feature
learning is not necessary as they can
simply be joined. If a relationship is
marked many-to-one, but the assumption is
violated, the pipeline will raise
an exception.
"""

one_to_many = "one-to-many"
"""Used for one-to-many or many-to-many relationships.

When there is such a relationship, feature learning
is necessary and meaningful. If you mark a join as
a default relationship, but that assumption is violated
for the training data, the pipeline will raise a
warning.
"""

one_to_one = "one-to-one"
"""Used for many-to-one relationships.

If two tables are guaranteed to be in a
one-to-one relationship, then feature
learning is not necessary as they can
simply be joined. If a relationship is
marked one-to-one, but the assumption is
violated, the pipeline will raise
an exception. If you are unsure whether
you want to use many_to_one or one_to_one,
user many_to_one.
"""

_all_relationships = [many_to_many, many_to_one, one_to_many, one_to_one]
