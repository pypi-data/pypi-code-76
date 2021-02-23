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

"""Contains functionalities for importing, handling, and retrieving
data from the getML engine.

All data relevant for the getML suite has to be present in the getML
engine. Its Python API itself does not store any of the data used for
training or prediction. Instead, it provides a handler class for the
data frame objects in the getML engine, the
:class:`~getml.data.DataFrame`. Either using this overall handler for
the underlying data set or the individual :mod:`~getml.data.columns`
its composed of, one can both import and retrieve data from the engine
as well as performing operations on them. In addition to the data
frame objects, the engine also uses an abstract and light weight
version of the underlying data model, which is represented by the
:class:`~getml.data.Placeholder`.

In general, working with data within the getML suite is organized in
three different steps.

* :ref:`Importing the data<importing_data>` into the getML engine .
* :ref:`Annotating the data<annotating>` by assign
  :mod:`~getml.data.roles` to the individual :mod:`~getml.data.columns`
* :ref:`Constructing the data model<data_model>` by deriving
  :class:`~getml.data.Placeholder` from the data and joining them to
  represent the data schema.

Examples:

    Creating a new data frame object in the getML engine and importing
    data is done by one the class methods
    :func:`~getml.data.DataFrame.from_csv`,
    :func:`~getml.data.DataFrame.from_db`,
    :func:`~getml.data.DataFrame.from_json`, or
    :func:`~getml.data.DataFrame.from_pandas`.

    In this example we chose to directly load data from a public
    database in the internet. But, firstly, we have to connect the
    getML engine to the database (see :ref:`mysql_interface` in the user
    guide for further details).

    .. code-block:: python

        getml.database.connect_mysql(
            host="relational.fit.cvut.cz",
            port=3306,
            dbname="financial",
            user="guest",
            password="relational",
            time_formats=['%Y/%m/%d']
        )

    Using the established connection, we can tell the engine to
    construct a new data frame object called 'df_loan', fill it with
    the data of 'loan' table contained in the MySQL database, and
    return a :class:`~getml.data.DataFrame` handler associated with
    it.

    .. code-block:: python

        loan = getml.data.DataFrame.from_db('loan', 'df_loan')

        print(loan)

    .. code-block:: pycon

        ...
        | loan_id      | account_id   | amount       | duration     | date          | payments      | status        |
        | unused float | unused float | unused float | unused float | unused string | unused string | unused string |
        -------------------------------------------------------------------------------------------------------------
        | 4959         | 2            | 80952        | 24           | 1994-01-05    | 3373.00       | A             |
        | 4961         | 19           | 30276        | 12           | 1996-04-29    | 2523.00       | B             |
        | 4962         | 25           | 30276        | 12           | 1997-12-08    | 2523.00       | A             |
        | 4967         | 37           | 318480       | 60           | 1998-10-14    | 5308.00       | D             |
        | 4968         | 38           | 110736       | 48           | 1998-04-19    | 2307.00       | C             |
        ...

    In order to construct the data model and for the feature
    learning algorithm to get the most out of your data, you have
    to assign roles to columns using the
    :meth:`~getml.data.DataFrame.set_role` method (see
    :ref:`annotating` for details).

    .. code-block:: python

        loan.set_role(["duration", "amount"], getml.data.roles.numerical)
        loan.set_role(["loan_id", "account_id"], getml.data.roles.join_key)
        loan.set_role("date", getml.data.roles.time_stamp)
        loan.set_role(["payments"], getml.data.roles.target)

        print(loan)

    .. code-block:: pycon

        | date                        | loan_id  | account_id | default | payments  | duration  | amount    | status        |
        | time stamp                  | join key | join key   | target  | numerical | numerical | numerical | unused string |
        ---------------------------------------------------------------------------------------------------------------------
        | 1994-01-05T00:00:00.000000Z | 4959     | 2          | 0       | 3373      | 24        | 80952     | A             |
        | 1996-04-29T00:00:00.000000Z | 4961     | 19         | 1       | 2523      | 12        | 30276     | B             |
        | 1997-12-08T00:00:00.000000Z | 4962     | 25         | 0       | 2523      | 12        | 30276     | A             |
        | 1998-10-14T00:00:00.000000Z | 4967     | 37         | 1       | 5308      | 60        | 318480    | D             |
        | 1998-04-19T00:00:00.000000Z | 4968     | 38         | 0       | 2307      | 48        | 110736    | C             |
        ...

    Finally, we are able to construct the data model by deriving
    :class:`~getml.data.Placeholder` from each
    :class:`~getml.data.DataFrame` and establishing relations between
    them using the :meth:`~getml.data.Placeholder.join` method.

    .. code-block:: python

        # But, first, we need second data set to build a data model.
        trans = getml.data.DataFrame.from_db(
            'trans', 'df_trans',
            roles = {getml.data.roles.numerical: ["amount", "balance"],
                     getml.data.roles.categorical: ["type", "bank", "k_symbol",
                                                    "account", "operation"],
                     getml.data.roles.join_key: ["account_id"],
                     getml.data.roles.time_stamp: ["date"]
            }
        )

        ph_loan = loan.to_placeholder()
        ph_trans = trans.to_placeholder()

        ph_loan.join(ph_trans, join_key="account_id",
                    time_stamp="date")

    The data model contained in `ph_loan` can now be used to
    construct a :class:`~getml.pipeline.Pipeline`.
"""

from . import relationship, roles, time
from .concat import concat
from .data_frame import DataFrame
from .data_frames import DataFrames
from .helpers import list_data_frames
from .helpers2 import delete, exists, load_data_frame
from .placeholder import Placeholder, _decode_joined_tables, _decode_placeholder

__all__ = (
    "DataFrame",
    "DataFrames" "Placeholder",
    "concat",
    "delete",
    "exists",
    "load_data_frame",
    "list_data_frames",
    "relationship",
    "roles",
    "time",
)
