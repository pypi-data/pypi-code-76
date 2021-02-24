"""
Base class for normalisation operations
"""
import copy
from abc import ABC, abstractmethod

from scmdata import ScmRun


class Normaliser(ABC):
    """
    Base class for normalising operations
    """

    @property
    def method_name(self):
        """
        str: Name of the method used for normalisation

        This string is included in the metadata of normalised data/files.
        """
        return self._method_name

    @staticmethod
    def _take_anomaly_from(inscmdf, ref_df):
        in_ts = inscmdf.timeseries()

        anomalies = in_ts - ref_df
        if anomalies.isnull().any().any():  # pragma: no cover
            raise ValueError("`inscmdf` and `ref_df` don't have the same index")

        anomalies = ScmRun(anomalies)

        return anomalies

    @staticmethod
    def _raise_branching_time_unavailable_error(branch_time, parent):
        error_msg = "Branching time `{:04d}{:02d}` not available in {} data in {}".format(
            branch_time.year,
            branch_time.month,
            parent.metadata["experiment_id"],
            parent.metadata["netcdf-scm crunched file"],
        )
        raise ValueError(error_msg)

    def get_reference_values(self, indata, picontrol, picontrol_branching_time):
        """
        Get reference values for an experiment from its equivalent piControl experiment

        Parameters
        ----------
        indata : :obj:`scmdata.ScmRun`
            Experiment to calculate reference values for

        picontrol : :obj:`scmdata.ScmRun`
            Pre-industrial control run data

        picontrol_branching_time : :obj:`datetime.datetime`
            The branching time in the pre-industrial experiment. It is assumed
            that the first timepoint in ``input`` follows immediately from this
            branching time.

        Returns
        -------
        :obj:`pd.DataFrame`
            Reference values with the same index and columns as ``indata``

        Raises
        ------
        ValueError
            The branching time data is not in ``picontrol`` data

        NotImplementedError
            The normalisation method is not recognised
        """
        if picontrol_branching_time.year not in picontrol["year"].unique().tolist():
            self._raise_branching_time_unavailable_error(
                picontrol_branching_time, picontrol
            )

        raw = self._get_reference_values(indata, picontrol, picontrol_branching_time)

        idx_cols = indata.meta.columns
        cols_to_unify = [
            c
            for c in idx_cols
            if c not in ["climate_model", "region", "variable", "unit"]
        ]
        out = raw.reset_index(cols_to_unify)
        for unify_col in cols_to_unify:
            out[unify_col] = indata.get_unique_meta(unify_col, no_duplicates=True)

        out = out.set_index(cols_to_unify, append=True)
        out = out.reorder_levels(idx_cols)

        return out

    @abstractmethod
    def _get_reference_values(self, indata, picontrol, picontrol_branching_time):
        """
        Calculate reference values from pre-industrial control run data
        """

    def normalise_against_picontrol(self, indata, picontrol, picontrol_branching_time):
        """
        Normalise data against picontrol

        Parameters
        ----------
        indata : :obj:`scmdata.ScmRun`
            Data to normalise

        picontrol : :obj:`scmdata.ScmRun`
            Pre-industrial control run data

        picontrol_branching_time : :obj:`datetime.datetime`
            The branching time in the pre-industrial experiment. It is assumed
            that the first timepoint in ``input`` follows immediately from this
            branching time.

        Returns
        -------
        :obj:`scmdata.ScmRun`
            Normalised data including metadata about the file which was used for
            normalisation and the normalisation method

        Raises
        ------
        NotImplementedError
            Normalisation is being done against a timeseries other than piControl

        ValueError
            The branching time data is not in ``picontrol`` data

        NotImplementedError
            The normalisation method is not recognised
        """
        norm_method_key = "normalisation method"

        if not picontrol.metadata["experiment_id"].endswith(  # pragma: no cover
            "piControl"
        ):
            # emergency valve, can't think of how this path should work
            raise NotImplementedError(
                "If you would like to normalise against an experiment other than "
                "piControl, please raise an issue at "
                "https://gitlab.com/netcdf-scm/netcdf-scm/-/issues"
            )

        reference_values = self.get_reference_values(
            indata, picontrol, picontrol_branching_time
        )
        out = self._take_anomaly_from(indata, reference_values)

        metadata = copy.deepcopy(indata.metadata)
        if not any(["(child)" in k for k in metadata]):
            metadata = {"(child) {}".format(k): v for k, v in metadata.items()}

        metadata = {
            **metadata,
            **{
                "(normalisation) {}".format(k): v for k, v in picontrol.metadata.items()
            },
        }
        metadata[norm_method_key] = self.method_name
        out.metadata = metadata

        return out
