"""
Load preprocessed datasets
"""

import json
import warnings
from pathlib import Path
from urllib.request import HTTPError, urlopen

import pandas as pd

from getml.data import DataFrame
from getml.log import logger

BUCKET = "https://static.getml.com/datasets/"
"""S3 bucket containing the CSV files"""


def _load_dataset(ds_name, assets, roles, units, as_pandas):
    """Helper function to load a dataset

    Args:
        ds_name (str): name of the dataset
        assets (list): CSV files to be loaded from the S3 bucket
        roles (bool): Return getml.DataFrame with roles set
        units (bool): Return getml.DataFrame with units set
        as_pandas (bool): Return data as `pandas.DataFrame` s

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True).
    """
    base = BUCKET + ds_name
    base += "/preprocessed"

    df_pandas = dict()
    for ass_ in assets:
        filename = base + "/" + ds_name + "_" + ass_ + ".csv"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df_pandas[ass_] = pd.read_csv(filename)

    if as_pandas:
        return df_pandas

    if roles:
        filename = base + "/" + ds_name + "_" + "roles.json"
        try:
            json_url = urlopen(filename)
            roles = json.loads(json_url.read())
        except HTTPError:
            raise Exception("Information on roles could not be retrieved.")
    else:
        roles = None

    if units:
        filename = base + "/" + ds_name + "_" + "units.json"
        try:
            json_url = urlopen(filename)
            units = json.loads(json_url.read())
        except HTTPError:
            raise Exception("Information on units could not be retrieved.")
    else:
        units = None

    df_getml = dict()
    for key, value in df_pandas.items():
        r_ = None if roles is None else roles.get(key)
        u_ = None if units is None else units.get(key)

        # Parse pd.Timestamps
        if r_ is not None and "time_stamp" in r_.keys():
            for t_ in r_["time_stamp"]:
                value[t_] = pd.to_datetime(value[t_])

        df_getml[key] = DataFrame.from_pandas(value, name=key, roles=r_)

        # Set units
        if u_ is not None:
            for unit, columns in u_.items():
                df_getml[key].set_unit(columns, unit)

    return df_getml


def load_air_pollution(roles=False, as_pandas=False):
    """Regression dataset on air pollution in Beijing, China

    The dataset consits of a single table split into train and test sets
    arround 2014-01-01.

    The orgininal publication is:
    Liang, X., Zou, T., Guo, B., Li, S., Zhang, H., Zhang, S., Huang, H. and
    Chen, S. X. (2015). Assessing Beijing's PM2.5 pollution: severity, weather
    impact, APEC and winter heating. Proceedings of the Royal Society A, 471,
    20150257.

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * train
            * test

    Examples:

        >>> df_getml = getml.datasets.load_air_pollution()
        >>> type(df_getml["test"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the atherosclerosis dataset including all necessary
        preprocessing steps please refer to `getml-examples
        <https://github.com/getml/getml-examples/tree/master/atherosclerosis>`_.


    Note:

        Roles can be set ad-hoc by supplying the respective flag. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`. This dataset contains no units.
        Before using them in an analysis, a data model needs to be constructed
        using :class:`~getml.data.Placeholder` s.
    """

    ds_name = "air_pollution"
    assets = ["train", "test"]

    units = False

    return _load_dataset(ds_name, assets, roles, units, as_pandas)


def load_atherosclerosis(roles=False, as_pandas=False):
    """Binary classification dataset on the lethality of atherosclerosis

    The atherosclerosis dataset is a medical dataset from the the `CTU Prague
    Relational Learning Repository
    <https://relational.fit.cvut.cz/dataset/Atherosclerosis>`_. It contains
    information from an longitudal study on 1417 middle-aged men obeserved over
    the course of 20 years. After preprocessing, it consists of 2 tables with 76
    and 66 columns:

    * `population`: Data on the study's participants

    * `contr`: Data on control dates

    The population table is split into a training (70%), a testing (15%) set and a
    validation (15%) set.

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * population_train
            * population_test
            * population_validation
            * contr

    Examples:

        >>> df_getml = getml.datasets.load_atherosclerosis()
        >>> type(df_getml["population_train"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the atherosclerosis dataset including all necessary
        preprocessing steps please refer to `getml-examples
        <https://github.com/getml/getml-examples/tree/master/atherosclerosis>`_.


    Note:

        Roles can be set ad-hoc by supplying the respective flag. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`. This dataset contains no units.
        Before using them in an analysis, a data model needs to be constructed
        using :class:`~getml.data.Placeholder` s.
    """

    ds_name = "atherosclerosis"
    assets = ["population_train", "population_test", "population_validation", "contr"]

    units = False

    return _load_dataset(ds_name, assets, roles, units, as_pandas)


def load_biodegradability(roles=False, as_pandas=False):
    """Regression dataset on molecule weight prediction

    The QSAR biodegradation dataset was built in the Milano Chemometrics and
    QSAR Research Group (Universita degli Studi Milano-Bicocca, Milano, Italy).
    The data have been used to develop QSAR (Quantitative Structure Activity
    Relationships) models for the study of the relationships between chemical
    structure and biodegradation of molecules. Biodegradation experimental
    values of 1055 chemicals were collected from the webpage of the National
    Institute of Technology and Evaluation of Japan (NITE).

    The orgininal publication is:
    Mansouri, K., Ringsted, T., Ballabio, D., Todeschini, R., Consonni, V.
    (2013). Quantitative Structure - Activity Relationship models for ready
    biodegradability of chemicals. Journal of Chemical Information and Modeling,
    53, 867-878

    The dataset was collected through the `UCI Machine Learning Repository`
    <https://archive.ics.uci.edu/ml/datasets/QSAR+biodegradation>

    It contains information on 1309 molecules with 6166 bonds. It consists of 5
    tables.

    The population table is split into a training (50 %) and a testing (25%) and
    validition (25%) sets.

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * molecule_train
            * molecule_test
            * molecule_validation
            * atom
            * bond
            * gmember
            * group

    Examples:

        >>> df_getml = getml.datasets.load_biodegradability()
        >>> type(df_getml["molecule_train"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the biodegradability dataset including all necessary
        preprocessing steps please refer to getml-examples (forthcoming).

    Note:

        Roles can be set ad-hoc by supplying the respective flag. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`. This dataset contains no units.
        Before using them in an analysis, a data model needs to be constructed
        using :class:`~getml.data.Placeholder` s.
    """

    ds_name = "biodegradability"
    assets = [
        "molecule_train",
        "molecule_test",
        "molecule_validation",
        "atom",
        "bond",
        "gmember",
        "group",
    ]

    units = False

    return _load_dataset(ds_name, assets, roles, units, as_pandas)


def load_consumer_expenditures(roles=False, units=False, as_pandas=False):
    """Binary classification dataset on consumer expenditures

    The Consumer Expenditure Data Set is a public domain data set provided by
    the American Bureau of Labor Statistics (https://www.bls.gov/cex/pumd.htm).
    It includes the diary entries, where American consumers are asked to keep
    diaries of the products they have purchased each month,

    We use this dataset to classify wether an item was pruchased as a gift.

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

        units (bool):

            Return data with units set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * population_testing
            * population_training,
            * population_validation
            * expd
            * fmld
            * memd

    Examples:

        >>> df_getml = getml.datasets.load_consumer_expenditures()
        >>> type(df_getml["expd"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the occupancy dataset including all necessary
        preprocessing steps please refer to `getml-examples
        <https://github.com/getml/getml-examples/tree/master/consumer_expenditures>`_.


    Note:

        Roles and units can be set ad-hoc by supplying the respective flag. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`.`
        Before using them in an analysis, a data model needs to be constructed
        using :class:`~getml.data.Placeholder` s.
    """

    ds_name = "consumer_expenditures"
    assets = [
        "population_testing",
        "population_training",
        "population_validation",
        "expd",
        "fmld",
        "memd",
    ]
    return _load_dataset(ds_name, assets, roles, units, as_pandas)


def load_interstate94(roles=False, units=False, as_pandas=False):
    """Regression dataset on traffic volume predicition

    The interstate94 dataset is a multivariate time series containing the
    hourly traffic volume on I-94 westbound from Minneapolis-St Paul. It is
    based on data provided by the `MN Department of Transportation
    <https://www.dot.state.mn.us/>`_. Some additional data preparation done by
    `John Hogue <https://github.com/dreyco676/Anomaly_Detection_A_to_Z/>`_. The
    dataset features some particular interesting characteristics common for
    time series, which classical models may struggle to appropriately deal
    with. Such characteristics are:

    * High frequency (hourly)
    * Dependence on irregular events (holidays)
    * Strong and overlapping cycles (daily, weekly)
    * Annomalies
    * Multiple seasonalities

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

        units (bool):

            Return data with units set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * train
            * test
            * weather

    Examples:

        >>> df_getml = getml.datasets.load_interstate94()
        >>> type(df_getml["traffic_train"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the interstate94 dataset including all necessary
        preprocessing steps please refer to `getml-examples
        <https://github.com/getml/getml-examples/tree/master/interstate94>`_.

    Note:

        Roles and units can be set ad-hoc by supplying the respective flags. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`. Before using them in an
        analysis, a data model needs to be constructed using
        :class:`~getml.data.Placeholder` s.
    """

    ds_name = "interstate94"
    assets = ["traffic_test", "traffic_train", "weather"]

    return _load_dataset(ds_name, assets, roles, units, as_pandas)


def load_loans(roles=False, units=False, as_pandas=False):
    """Binary classification dataset on loan default

    The loans dataset is based on financial dataset from the the `CTU Prague
    Relational Learning Repository
    <https://relational.fit.cvut.cz/dataset/Financial>`_.

    The original publication is:
    Berka, Petr (1999). Workshop notes on Discovery Challange PKDD'99.

    The dataset contains information on 606 successful and 76 unsuccessful
    loans. After some preprocessing it contains 4 tables

    * `population`: Information about the loans themselves, such as the date of creation, the amount, and the planned duration of the loan. The target variable is the status of the loan (default/no default)

    * `order`: Information about permanent orders, debited payments and account balances.

    * `trans`: Information about transactions and accounts balances.

    * `meta`: Meta information about the obligor, such as gender and geo-information

    The population table is split into a training and a testing set at 80% of the main population.

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

        units (bool):

            Return data with units set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * population_train
            * population_test
            * order
            * trans
            * meta

    Examples:

        >>> df_getml = getml.datasets.load_loans()
        >>> type(df_getml["population_train"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the loans dataset including all necessary
        preprocessing steps please refer to `getml-examples
        <https://github.com/getml/getml-examples/tree/master/loans>`_.

    Note:

        Roles and units can be set ad-hoc by supplying the respective flags. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`. Before using them in an
        analysis, a data model needs to be constructed using
        :class:`~getml.data.Placeholder` s.
    """

    ds_name = "loans"
    assets = ["population_train", "population_test", "order", "trans", "meta"]

    return _load_dataset(ds_name, assets, roles, units, as_pandas)


def load_occupancy(roles=False, as_pandas=False):
    """Binary classification dataset on occupancy detection

    The occupancy detection data set is a very simple multivariate time series
    from the `UCI Machine Learning Repository
    <https://archive.ics.uci.edu/ml/datasets/Occupancy+Detection+>`_. It is a
    binary classification problem. The task is to predict room occupancy
    from Temperature, Humidity, Light and CO2.

    The original publication is:
    Candanedo, L. M., & Feldheim, V. (2016). Accurate occupancy detection of an
    office room from light, temperature, humidity and CO2 measurements using
    statistical learning models. Energy and Buildings, 112, 28-39.

    Args:
        as_pandas (bool):

            Return data as `pandas.DataFrame` s

        roles (bool):

            Return data with roles set

    Returns:
        dict:

            Dictionary containing the data as :class:`~getml.data.DataFrame` s or
            :class:`pandas.DataFrame` s (if `as_pandas` is True). The keys correspond
            to the name of the DataFrame on the :mod:`~getml.engine`. The following
            DataFrames are contained in the dictionary

            * train
            * validate
            * test

    Examples:

        >>> df_getml = getml.datasets.load_occupancy()
        >>> type(df_getml["train"])
        ... getml.data.data_frame.DataFrame

        For an full analysis of the occupancy dataset including all necessary
        preprocessing steps please refer to `getml-examples
        <https://github.com/getml/getml-examples/tree/master/occupancy>`_.


    Note:

        Roles can be set ad-hoc by supplying the respective flag. If
        `roles` is `False`, all columns in the returned
        :class:`~getml.data.DataFrames` s have roles
        :const:`~getml.data.roles.unused_string` or
        :const:`~getml.data.roles.unused_float`. This dataset contains no units.
        Before using them in an analysis, a data model needs to be constructed
        using :class:`~getml.data.Placeholder` s.
    """

    ds_name = "occupancy"
    assets = ["test", "train", "validate"]

    units = False

    return _load_dataset(ds_name, assets, roles, units, as_pandas)
