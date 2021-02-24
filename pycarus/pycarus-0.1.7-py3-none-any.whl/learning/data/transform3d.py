import pytorch3d.transforms.transform3d as pt3d  # type: ignore
import torch
from pytorch3d.transforms.rotation_conversions import _axis_angle_rotation  # type: ignore

from pycarus.geometry.pcd import affine, farthest_point_sampling, jitter_pcd, normalize_pcd
from pycarus.geometry.pcd import random_drop_points, random_point_sampling, rotate, scale
from pycarus.geometry.pcd import shuffle_pcd, translate


class PointSampler:
    """Perform uniform sampling on point cloud using farthest point sampling.

    Args:
        num_points: Number of point to sample.
        algorithm: the algorithm to use for the subsampling one in ["fps", "random"].
    """

    def __init__(self, num_points: int, algorithm: str) -> None:
        self.num_points = num_points
        self.algorithm = algorithm

        if self.algorithm not in ["fps", "random"]:
            raise ValueError(f"Expected type to be one of [fps, random], got {algorithm}")

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        """Sample point cloud.

        Args:
            pcd: The input point cloud with shape (NUM_POINTS, D).

        Returns:
            The sampled point cloud.
        """
        pcd_ss = torch.tensor([])
        if self.algorithm == "fps":
            pcd_ss = farthest_point_sampling(pcd, self.num_points)

        if self.algorithm == "random":
            pcd_ss = random_point_sampling(pcd, self.num_points)

        return pcd_ss

    def __repr__(self) -> str:
        format_string = f"{self.__class__.__name__}: num_points: {self.num_points}"
        format_string += f" - algorithm: {self.algorithm}."
        return format_string


class Normalize:
    """Normalize a given point cloud into the unit cube."""

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        """Normalize a point cloud.

        Args:
            pcd: The input point cloud with shape (NUM_POINTS, D).

        Returns:
            The normalized point cloud.
        """
        return normalize_pcd(pcd)


class Affine(pt3d.Transform3d):
    """Transform to apply an affine transformation, i.e. rotation plus a translation."""

    def __init__(self, matrix: torch.Tensor) -> None:
        """Transform to apply an affine transformation, i.e. rotation plus a translation.

        Args:
            matrix: The motion matrix with shape (4, 4).
        """
        self.matrix = matrix
        super().__init__(matrix=self.matrix)

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        return affine(pcd, self.matrix)


class Rotate(pt3d.Rotate):
    """Transform to rotate a point cloud."""

    def __init__(self, rotation: torch.Tensor) -> None:
        """Transform to rotate a point cloud.

        Args:
            rotation: The rotation matrix with shape (3, 3).
        """
        self.rotation = rotation
        super().__init__(self.rotation)

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        return rotate(pcd, self.rotation)


class RandomRotateAxisAngle:
    """Rotate a point cloud around one axis by a random angle sampled within a range. """

    def __init__(self, min_angle: float, max_angle: float, axis: str):
        """Rotate a point cloud around one axis by a random angle sampled within a range.

        Args:
            min_angle: the lower bound for the angle in radians.
            max_angle: the upper bound for the angle in radians.
            axis: the axis of rotation.

        Raises:
            ValueError: if the required axis is different from [X, Y, Z].
        """
        self.axis = axis.upper()

        if axis not in ["X", "Y", "Z"]:
            raise ValueError(f"Expected axis to be one of [X, Y, Z], not got {axis}")

        self.min_angle = min_angle
        self.max_angle = max_angle
        self.last_matrix = torch.eye(3)

    @staticmethod
    def _get_params(min_angle: float, max_angle: float, axis: str) -> torch.Tensor:
        """Get random rotation matrix with an angle in the range min_angle - max_angle.

        Args:
            min_angle: the lower bound for the angle in radians.
            max_angle: the upper bound for the angle in radians.
            axis: the axis of rotation.

        Returns:
            The rotation matrix with shape (3, 3).
        """
        theta = torch.FloatTensor(1).uniform_(min_angle, max_angle)
        matrix_col_major = _axis_angle_rotation(axis, theta)
        # The convention used in this framework is to operate on points as row vectors.
        # The rotation matrix returned from _axis_angle_rotation is for transforming column vectors.
        # Therefore we transpose this matrix.
        matrix_row_major = matrix_col_major.transpose(1, 2)[0]
        return matrix_row_major

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        self.last_matrix = self._get_params(self.min_angle, self.max_angle, self.axis)
        return rotate(pcd, self.last_matrix)

    def __repr__(self) -> str:
        format_string = f"{self.__class__.__name__}: min_angle: {self.min_angle}"
        format_string += f" - max_angle: {self.max_angle} - axis: {self.axis}."

        return format_string


class Translate(pt3d.Translate):
    """Transform to translate a point cloud."""

    def __init__(self, translation: torch.Tensor) -> None:
        """Transform to translate a point cloud.

        Args:
            translation: The translation offset with shape (3,).
        """
        self.translation = translation
        x, y, z = translation[0], translation[1], translation[2]
        super().__init__(x=x, y=y, z=z)

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        return translate(pcd, self.translation)


class Scale(pt3d.Scale):
    """Transform to scale a point cloud."""

    def __init__(self, scale_factor: torch.Tensor) -> None:
        """Transform to scale a point cloud.

        Args:
            scale_factor: The scale factor for the x, y, z, dimensions with shape (3,).
        """
        self.scale_factor = scale_factor
        x, y, z = scale_factor[0], scale_factor[1], scale_factor[2]
        super().__init__(x=x, y=y, z=z)

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        return scale(pcd, self.scale_factor)


class JitterPointCloud:
    """Jitter point cloud by adding random noise"""

    def __init__(self, sigma: float, clip: float) -> None:
        """Jitter point cloud by adding random noise.

        Args:
            sigma: The sigma for the gaussian noise.
            clip: The clipping value.
        """
        self.sigma = sigma
        self.clip = clip

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        return jitter_pcd(pcd, self.sigma, self.clip)


class RandomDropPoints:
    """Randomly remove points from a point cloud."""

    def __init__(self, min_percentage: float, max_percentage: float) -> None:
        """Remove random percentage of points from a point cloud. The number of points is uniformly
        sampled in the range min_percentage - max_percentage.

        Args:
            min_percentage: The lower bound for the percentage of points to remove.
            max_percentage: The upper bound for the percentage of points to remove.
        """
        self.min_percentage = min_percentage
        self.max_percentage = max_percentage
        self.drop_percentage = 0.0
        self.last_kept = torch.Tensor([])
        self.last_removed = torch.Tensor([])

    @staticmethod
    def _get_params(min_percentage: float, max_percentage: float) -> float:
        """Get random number in the range min_percentage - max_percentage.

        Args:
            min_percentage: the lower bound for the percentage.
            max_percentage: the upper bound for the percentage.

        Returns:
            A random number in the specified range.
        """
        random_percentage = torch.FloatTensor(1).uniform_(min_percentage, max_percentage)[0].item()
        return float(random_percentage)

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        self.last_drop_percentage = self._get_params(self.min_percentage, self.max_percentage)
        points, indices_kept, indices_removed = random_drop_points(pcd, self.last_drop_percentage)
        self.last_kept = indices_kept
        self.last_removed = indices_removed

        return points

    def __repr__(self) -> str:
        format_string = f"{self.__class__.__name__}: min_percentage: {self.min_percentage}"
        format_string += f" - max_percentage: {self.max_percentage}."

        return format_string


class ShufflePoints:
    """Shuffle the order of the points inside the point cloud."""

    def __call__(self, pcd: torch.Tensor) -> torch.Tensor:
        return shuffle_pcd(pcd)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
