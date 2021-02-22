"""
Base class for metric calculations
"""
from abc import ABC


class Calculator(ABC):
    """
    Base class for metric calculations
    """

    @classmethod
    def can_calculate_metric(cls, metric):
        """
        Decide whether the input metric can be calculated or not

        Parameters
        ----------
        metric : str
            Metric to check

        Returns
        -------
        bool
            If ``True``, the metric can be calculated. Otherwise, it cannot.
        """
        return cls._can_calculate_metric(metric)

    @classmethod
    def _can_calculate_metric(cls, metric):  # noqa: D401
        """
        Internal handling of whether a metric can be calculated or not, to be implemented in sub-classes of :obj:`Calculator`
        """
        raise NotImplementedError

    @classmethod
    def calculate_metric(
        cls, assessed_ranges, res_calc, norm_period, evaluation_period, unit
    ):
        """
        Calculate metric

        Parameters
        ----------
        assessed_ranges : :obj:`pyrcmip.assessed_ranges.AssessedRanges`
            Assessed ranges instance

        res_calc : :obj:`scmdata.ScmRun`
            Results from which the metric is to be derived

        norm_period : list
            Years to use for normalising the data before calculating the metric

        evaluation_period : list
            Years to use when evaluating the metric

        unit : str
            Unit in which the metric should be returned

        Returns
        -------
        :obj:`pd.DataFrame`
            Metric values with other relevant model metadata

        Raises
        ------
        NoDataForMetricError
            No data is available to calculate the given metric

        DimensionalityError
            The units of the data cannot be converted to the desired units or
            the units of the data are incompatible with the metric calculation
        """
        return cls._calculate(
            assessed_ranges, res_calc, norm_period, evaluation_period, unit
        )

    @classmethod
    def _calculate(
        cls, assessed_ranges, res_calc, norm_period, evaluation_period, unit
    ):  # noqa: D401
        """
        Internal handling of calculations, to be implemented in sub-classes of :obj:`Calculator`
        """
        raise NotImplementedError
