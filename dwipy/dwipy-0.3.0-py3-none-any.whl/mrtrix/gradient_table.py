import numpy as np
import dwipy.constants
import os


class GradientTable:
    def __init__(self, gradient_matrix: np.ndarray) -> None:
        # Round the bvals, they should be int
        # But in some cases, there are small floats
        gradient_matrix[:, 3] = np.around(gradient_matrix[:, 3])
        self._gradients = gradient_matrix

    @classmethod
    def from_matrix(cls, gradient_table: np.ndarray):
        if gradient_table.shape[1] != 4:
            raise ValueError("Invalid gradient table format")

        return cls(gradient_table)

    @classmethod
    def from_file(cls, gradient_file: str):
        """
        Load a gradient file from the mrtrix3 format.

        Args:
            gradient_file (str): File location

        Returns:
            np.ndarray: Gradients, [Nx4] matrix with N the number of entries
        """
        # Load the array with minimum of 2 dimension
        # Otherwise in case of a single line we get 1 dimensional array
        # Which is confusing for index
        if os.path.exists(gradient_file):
            grad_matrix = np.loadtxt(
                gradient_file, delimiter=" ", comments="#", dtype=float, ndmin=2
            )
        else:
            raise IOError("Gradient file {grad_file} not found!".format(grad_file=gradient_file))

        return cls(grad_matrix)

    @property
    def gradients(self) -> np.ndarray:
        """
        Get the full gradient table.

        Returns:
            np.ndarray: The gradient table
        """
        return self._gradients

    @property
    def n_entries(self) -> int:
        """
        Get number of entries in gradient table.

        Returns:
            int: Number of entries
        """
        return self._gradients.shape[0]

    @property
    def n_unique_bvals(self) -> int:
        return self.unique_bvals.shape[0]

    @property
    def bvals(self) -> np.ndarray:
        """
        Get the b-values from the gradient matrix.

        Returns:
            np.ndarray: The b-values
        """
        # Bvals are last column
        return self._gradients[:, 3]

    @property
    def unique_bvals(self) -> np.ndarray:
        return np.unique(self.bvals)

    @bvals.setter
    def bvals(self, bvals_value: np.ndarray) -> None:
        if bvals_value.shape[0] != self.n_entries:
            raise ValueError(
                "Number of b-values does not match number of entries. Currently gradient table has {n_entries} entries, you provided {bval_length} entries.".format(
                    n_entries=self.n_entries, bval_length=bvals_value.shape[0]
                )
            )
        # Round the bvals to make sure they are ints
        bvals_value = np.around(bvals_value)
        self._gradients[:, 3] = bvals_value

    @property
    def bvecs(self) -> np.ndarray:
        """
        Get the gradient vectors from the gradient matrix.

        Returns:
            np.ndarray: The gradient vectors
        """
        # Bvecs are everything up to last column
        return self._gradients[:, 0:3]

    @bvecs.setter
    def bvecs(self, bvecs_values: np.ndarray) -> None:
        if bvecs_values.shape[0] != self.n_entries:
            raise ValueError(
                "Number of b-values does not match number of entries. Currently gradient table has {n_entries} entries, you provided {bvec_length} entries.".format(
                    n_entries=self.n_entries, bvec_length=bvecs_values.shape[0]
                )
            )

        self._gradients[:, 0:3] = bvecs_values

    @property
    def bvecs_non_zero_bvals(self) -> np.ndarray:
        return self.bvecs[self.bvals != 0, 0:3]

    def write_to_file(self, gradient_file: str) -> None:
        """
        Write the gradient table to a mrtrix3 file.

        Args:
            gradient_file (str): Path to the gradient file
        """
        np.savetxt(
            gradient_file, self._gradients, delimiter=" ", fmt=["%2.5f", "%2.5f", "%2.5f", "%d"]
        )

    @property
    def bvalue_status(self) -> dwipy.constants.GRADSTATUS:
        if any(np.isnan(self.bvals)):
            return dwipy.constants.GRADSTATUS.BVALS_HAS_NAN
        if self.n_unique_bvals < 2:
            return dwipy.constants.GRADSTATUS.ONE_BVAL
        if any(self.unique_bvals > dwipy.constants.MAX_B_VALUE):
            return dwipy.constants.GRADSTATUS.BVALS_TOO_HIGH

        total_bvec_per_direction = np.sum(np.abs(self.bvecs_non_zero_bvals), axis=0)

        if any(total_bvec_per_direction == 0) and any(total_bvec_per_direction > 0):
            return dwipy.constants.GRADSTATUS.DTI_ONE_DIRECTION

        return dwipy.constants.GRADSTATUS.VALID_GRADS

    def is_valid(self) -> bool:
        return self.bvalue_status is dwipy.constants.GRADSTATUS.VALID_GRADS

    @property
    def dwi_type(self) -> dwipy.constants.DWITYPE:
        if not self.is_valid():
            raise ValueError("The gradient table is not a valid DWI table, cannot determine type")

        bvec_total_value = np.sum(np.power(self.bvecs, 2), axis=1)
        if self.n_unique_bvals == 2 and np.count_nonzero(self.bvecs) == 0:
            # WE only have two entries, and all b-vectors are zero
            # So it is a trace
            return dwipy.constants.DWITYPE.DWI_SINGLE_TRACE
        elif self.n_unique_bvals > 2 and np.count_nonzero(self.bvecs) == 0:
            # We have mutiple b-values, but all are still trace
            return dwipy.constants.DWITYPE.DWI_MULTI_TRACE
        # Not sure what thise one represents
        # elif np.count_nonzero(np.unique(bvals)) == np.count_nonzero(bvec_total_value):
        #     # We have bvecs but with just one corresonding bval for each
        #     # Not really a DTI, probably error in extraction
        #     return dwipy.constants.DWITYPE.DWI_TRACE_NONZERO_BVAL
        # elif np.count_nonzero(bvecs) == 0:
        #     return dwipy.constants.DWITYPE.UNKNOWN
        else:
            # Bvec values for non-zero b values
            max_bvec = np.amax(np.abs(self.bvecs[self.bvals != 0, :]), axis=1)
            is_zero = np.isclose(bvec_total_value[self.bvals != 0], 0)

            if len(np.unique(self.bvals[self.bvals != 0])) * 3 == np.count_nonzero(max_bvec):
                # We can have multiple bvals that each a single x/y/z bvec
                # We do not consider this DTI
                return dwipy.constants.DWITYPE.DWI_MULTI_B_VECS
            elif np.sum(is_zero) != 0:
                # Some non-zero bvals are actually trace images
                return dwipy.constants.DWITYPE.DWI_MULTI_B_VECS_AND_TRACE
            else:
                return dwipy.constants.DWITYPE.DTI
