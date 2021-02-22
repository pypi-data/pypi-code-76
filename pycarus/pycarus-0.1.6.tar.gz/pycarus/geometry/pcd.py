import math
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

import numpy as np  # type: ignore
import open3d as o3d  # type: ignore
import pytorch3d.transforms.transform3d as pt3d  # type: ignore
import torch


def batchify(inputs: List[torch.Tensor], required_dim: int) -> Tuple[bool, List[torch.Tensor]]:
    """Batchify input tensors if needed.

    All the input tensors with a number of dimensions smaller than
    required_dim will be expanded with a leading batch dimension.

    Args:
        inputs: The tensors to batchify.
        required_dim: The required number of dimensions.

    Returns:
        - A flag that indicates wether one of the inputs has been batchified.
        - The batchified tensors.
    """
    results: List[torch.Tensor] = []
    has_changed = False

    for t in inputs:
        has_changed = len(t.shape) < required_dim or has_changed
        batched_t = torch.unsqueeze(t, dim=0) if has_changed else t
        results.append(batched_t)

    return has_changed, results


def unbatchify(inputs: List[torch.Tensor]) -> List[torch.Tensor]:
    """Remove batch dimension from input tensors.

    Args:
        inputs: The tensors to unbatchify.

    Returns:
        The unbatchified tensors.
    """
    results: List[torch.Tensor] = []
    for t in inputs:
        unbatched_t = torch.squeeze(t, dim=0)
        results.append(unbatched_t)

    return results


def read_pcd(pcd_path: Union[str, Path], dtype: torch.dtype = torch.float) -> torch.Tensor:
    """Read a point cloud from a given file.

    The point cloud is returned as a torch tensor with shape (NUM_POINTS, D).
    D can be 3 (only XYZ coordinates), 6 (XYZ coordinates and
    normals) or 9 (XYZ coordinates, normals and colors).

    Args:
        pcd_path: The path of the point cloud file.
        dtype: The data type for the output tensor.

    Raises:
        ValueError: If the given file doesn't exist.

    Returns:
        A torch tensor with the loaded point cloud with shape (NUM_POINTS, D).
    """
    pcd_path = Path(pcd_path)
    if not pcd_path.exists():
        raise ValueError(f"The pcd file {str(pcd_path)} does not exists.")

    pcd_o3d = o3d.io.read_point_cloud(str(pcd_path))
    pcd_torch = torch.tensor(pcd_o3d.points, dtype=dtype)

    if len(pcd_o3d.normals) > 0:
        normals_torch = torch.tensor(pcd_o3d.normals, dtype=dtype)
        pcd_torch = torch.cat((pcd_torch, normals_torch), dim=-1)

    if len(pcd_o3d.colors) > 0:
        colors_torch = torch.tensor(pcd_o3d.colors, dtype=dtype)
        pcd_torch = torch.cat((pcd_torch, colors_torch), dim=-1)

    return pcd_torch


def get_o3d_from_tensor(pcd: Union[torch.Tensor, np.ndarray]) -> o3d.geometry.PointCloud:
    """Get open3d point cloud from either numpy array or torch tensor.

    The input point cloud must have shape (NUM_POINTS, D), where D can be 3
    (only XYZ coordinates), 6 (XYZ coordinates and normals) or 9
    (XYZ coordinates, normals and colors).

    Args:
        pcd: The numpy or torch point cloud with shape (NUM_POINTS, D).

    Returns:
        The open3d point cloud.
    """
    pcd_o3d = o3d.geometry.PointCloud()

    pcd_o3d.points = o3d.utility.Vector3dVector(pcd[:, :3])

    if pcd.shape[1] >= 6:
        pcd_o3d.normals = o3d.utility.Vector3dVector(pcd[:, 3:6])

    if pcd.shape[1] == 9:
        pcd_o3d.colors = o3d.utility.Vector3dVector(pcd[:, 6:])

    return pcd_o3d


def normalize_pcd(pcd: torch.Tensor) -> torch.Tensor:
    """Normalize the given point cloud(s) in the unit sphere.

    For each input point cloud, coordinates are first expressed
    wrt to the point cloud centroid. Then, they are normalized
    wrt the maximum distance from the centroid. If present,
    normals and colors are preserved.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).

    Returns:
        The normalized point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    pcd_copy = torch.clone(pcd)
    batched, [pcd_copy] = batchify([pcd_copy], 3)

    xyz = pcd_copy[:, :, :3]
    centroid = torch.mean(xyz, dim=1)
    xyz = xyz - centroid
    distances_from_centroid = torch.norm(xyz, p=2, dim=-1)  # type: ignore
    max_dist_from_centroid = torch.max(distances_from_centroid)
    xyz = xyz / max_dist_from_centroid

    normalized_pcd = torch.cat((xyz, pcd_copy[:, :, 3:]), dim=-1)

    if batched:
        [normalized_pcd] = unbatchify([normalized_pcd])

    return normalized_pcd


def farthest_point_sampling(pcd: torch.Tensor, num_points: int) -> torch.Tensor:
    """Sample the requested number of points from the given point cloud(s).

    Points are sampled using farthest point sampling.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        num_points: The number of points to sample.

    Returns:
        The sampled points with shape ([B,] NUM_SAMPLED_POINTS, D).
    """
    dev = pcd.device

    batched, [pcd] = batchify([pcd], 3)

    batch_size, original_num_points, point_dim = pcd.shape
    xyz = pcd[:, :, :3]

    distances = torch.full((batch_size, original_num_points), 1e10, device=dev)
    farthest = torch.randint(0, original_num_points, (batch_size,))

    output_shape = (batch_size, num_points, point_dim)
    sampled_points = torch.empty(output_shape, dtype=pcd.dtype, device=dev)
    batch_indices = torch.arange(batch_size, dtype=torch.long)

    for i in range(num_points):
        sampled_points[:, i] = pcd[batch_indices, farthest]
        current = xyz[batch_indices, farthest, :].view(batch_size, 1, 3)
        distances_from_current = torch.sum((xyz - current) ** 2, -1)
        mask = distances_from_current < distances
        distances[mask] = distances_from_current[mask]  # avoid picking previous point
        farthest = torch.argmax(distances, dim=-1)

    if batched:
        [sampled_points] = unbatchify([sampled_points])

    return sampled_points


def random_point_sampling(pcd: torch.Tensor, num_points: int) -> torch.Tensor:
    """Sample the requested number of points from the given point cloud(s).

    Points are sampled randomly.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        num_points: The number of points to sample.

    Returns:
        The sampled points with shape ([B,] NUM_SAMPLED_POINTS, D).
    """
    batched, [pcd] = batchify([pcd], 3)

    batch_size, original_num_points, _ = pcd.shape
    weights = torch.ones((batch_size, original_num_points), dtype=torch.float)
    indices_to_sample = torch.multinomial(weights, num_points, replacement=False)
    batch_indices = torch.arange(batch_size).view(batch_size, 1)
    sampled_points = pcd[batch_indices, indices_to_sample]

    if batched:
        [sampled_points] = unbatchify([sampled_points])

    return sampled_points


def get_distances_matrix(pcd_src: torch.Tensor, pcd_trg: torch.Tensor) -> torch.Tensor:
    """Get euclidean distances between two point clouds.

    This functions assumes that the first three element of each point are XYZ coordinates.
    It creates a matrix with shape (NUM_POINTS_SRC, NUM_POINTS_TRG), where the i-th row contains
    the euclidean distances between the i-th point of pcd_src and all the other points.

    Args:
        pcd_src: The input point cloud(s) with shape ([B,] NUM_POINTS_SRC, D).
        pcd_trg: The input point cloud(s) with shape ([B,] NUM_POINTS_TRG, D).

    Returns:
        The matrix with distances with shape (NUM_POINTS_SRC, NUM_POINTS_TRG).
    """
    batched, [pcd_src, pcd_trg] = batchify([pcd_src, pcd_trg], 3)

    pcd_src = pcd_src[:, :, :3]
    pcd_trg = pcd_trg[:, :, :3]

    size_batch, num_pts_src, _ = pcd_src.shape
    _, num_pts_trg, _ = pcd_trg.shape

    dot_src_trg = -2 * torch.matmul(pcd_src, pcd_trg.permute(0, 2, 1))
    src_square = torch.sum(pcd_src ** 2, -1).view(size_batch, num_pts_src, 1)
    trg_square = torch.sum(pcd_trg ** 2, -1).view(size_batch, 1, num_pts_trg)

    mat_dist_squared = dot_src_trg + src_square + trg_square
    mat_dist_squared[mat_dist_squared < 0.0] = 0.0
    mat_distances = torch.sqrt(mat_dist_squared)

    if batched:
        [mat_distances] = unbatchify([mat_distances])

    return mat_distances


def get_neighbours_distance(pcd: torch.Tensor, reduce_fn: str) -> torch.Tensor:
    """Compute distance between neighbouring points.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        reduce_fn: The reduce function to apply to neighbours distances.
            Available options are "min", "max", "mean", "median", "std".

    Raises:
        ValueError: If the given reduce function is unknown.

    Returns:
        The distance computed using the specified reduce_fn.
    """
    batched, [pcd] = batchify([pcd], 3)

    num_points = pcd.shape[1]
    distances = get_distances_matrix(pcd, pcd)
    distances[:, torch.eye(num_points).bool()] = float("inf")
    neighbours_distances = torch.min(distances, dim=-1)[0]

    rfns: Dict[str, Callable[[torch.Tensor], torch.Tensor]] = {
        "min": torch.min,
        "max": torch.max,
        "mean": torch.mean,
        "median": torch.median,
        "std": torch.std,
    }

    try:
        rfn = rfns[reduce_fn]
    except KeyError:
        raise ValueError("Unknown reduce function.")

    result = rfn(neighbours_distances)

    if batched:
        [result] = unbatchify([result])

    return result


def shuffle_pcd(pcd: torch.Tensor) -> torch.Tensor:
    """Shuffle the order of the point inside the give point cloud(s).

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).

    Returns:
        The shuffled point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    pcd_copy = torch.clone(pcd)

    batched, [pcd_copy] = batchify([pcd_copy], 3)

    _, num_points, _ = pcd_copy.shape
    rand_indices = torch.randperm(num_points)
    shuffled_pcd = pcd_copy[:, rand_indices]

    if batched:
        [shuffled_pcd] = unbatchify([shuffled_pcd])

    return shuffled_pcd


def jitter_pcd(pcd: torch.Tensor, sigma: float = 0.01, clip: float = 0.05) -> torch.Tensor:
    """Jitter point cloud(s) by adding random noise.

    Add a gaussian noise to each coordinates of each point
    in the input point cloud. The noise is sampled from a normal
    distribution with mean 0 and std 1 multiplied by sigma.
    Finally, the final amount of noise to add is clipped between -clip and clip.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        sigma: The sigma for the gaussian noise.
        clip: The clipping value.

    Returns:
        The jittered point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    pcd_copy = torch.clone(pcd)

    batched, [pcd_copy] = batchify([pcd_copy], 3)
    size_batch, num_points = pcd_copy.shape[0], pcd_copy.shape[1]

    noise = torch.clip(sigma * torch.randn((size_batch, num_points, 3)), min=-1 * clip, max=clip)
    jittered_pts = pcd_copy[:, :, 0:3] + noise.to(pcd_copy.device)
    jittered_pcd = pcd_copy
    jittered_pcd[:, :, 0:3] = jittered_pts

    if batched:
        [jittered_pcd] = unbatchify([jittered_pcd])

    return jittered_pcd


def random_drop_points(
    pcd: torch.Tensor,
    drop_percentage: float,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Random drop points in the given point cloud(s).

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        drop_percentage: The percentage of points to be removed.

    Returns:
        - The dropped point cloud(s) with shape ([B,] NUM_POINTS, D).
        - The indices of points that have been kept.
        - The indices of points that have been removed.
    """
    pcd_copy = torch.clone(pcd)
    batched, [pcd_copy] = batchify([pcd_copy], 3)
    batch_size, num_input_pts, point_dim = pcd_copy.shape
    num_pts_to_remove = math.ceil(num_input_pts * drop_percentage)

    if num_pts_to_remove > 0:
        weights = torch.ones((batch_size, num_input_pts), dtype=torch.float)
        indices_to_remove = torch.multinomial(weights, num_pts_to_remove, replacement=False)
        indices_to_remove = indices_to_remove.to(pcd_copy.device)

        output_shape = (batch_size, num_input_pts - num_pts_to_remove, point_dim)
        pcd_dropped = torch.empty(output_shape, dtype=pcd_copy.dtype)
        indices_to_keep = torch.empty(output_shape[:-1], dtype=torch.long)
        for i in range(batch_size):
            indices_pcd = torch.arange(num_input_pts)
            mask = torch.full((num_input_pts,), True)
            mask[indices_to_remove[i]] = False
            indices_to_keep[i] = indices_pcd[mask]

            pcd_dropped[i] = pcd_copy[i, indices_to_keep[i]]
    else:
        pcd_dropped = pcd_copy
        indices_to_keep = torch.arange(end=num_input_pts).repeat((batch_size,))
        indices_to_remove = torch.Tensor([])

    indices_to_keep = indices_to_keep.to(pcd_copy.device)
    pcd_dropped = pcd_dropped.to(pcd_copy.device)

    if batched:
        results = [pcd_dropped, indices_to_keep, indices_to_remove]
        [pcd_dropped, indices_to_keep, indices_to_remove] = unbatchify(results)

    return pcd_dropped, indices_to_keep, indices_to_remove


def _apply_pt3d_transform(
    pcd: torch.Tensor,
    transform: pt3d.Transform3d,
    transform_normals: bool,
) -> torch.Tensor:
    """Apply PyTorch 3D transform to the input point clouds.

    This method is a wrapper to the PyTorch3D Transform3D in order to avoid to call separate
    methods to transform points and normals. If transform_normals is True also the normals are
    transformed, for some rigid transformation such as scale and transation this is not
    necessary.

    Args:
        pcd: The input point clouds with shape (B, NUM_POINTS, D).
        transform: The transform to apply.

    Returns:
        The transformed point clouds.
    """
    batched, [pcd] = batchify([pcd], 3)

    point_dim = pcd.shape[-1]
    pcd_transformed = transform.transform_points(pcd[:, :, :3])

    if point_dim >= 6:
        if transform_normals:
            normals = transform.transform_normals(pcd[:, :, 3:6])
        else:
            normals = pcd[:, :, 3:6]
        pcd_transformed = torch.cat((pcd_transformed, normals), dim=-1)

    if point_dim == 9:
        colors = pcd[:, :, 6:9]
        pcd_transformed = torch.cat((pcd_transformed, colors), dim=-1)

    if batched:
        [pcd_transformed] = unbatchify([pcd_transformed])

    return pcd_transformed


def affine(pcd: torch.Tensor, affine_transform: torch.Tensor) -> torch.Tensor:
    """Apply an affine transformation, typically a rigid motion matrix.

    This method applies a rotation and a translation to the input point cloud. We rely on the same
    convention of PyTorch3D, hence an affine matrix is stored using a row-major order:
      M = [ [Rxx, Ryx, Rzx, 0],
            [Rxy, Ryy, Rzy, 0],
            [Rxz, Ryz, Rzz, 0],
            [Tx,  Ty,  Tz,  1],]
    the rows of the matrix represent the bases of a coordinate system and the last row stores
    the translation vector. If the point cloud contains also the normals, only the rotation
    will be applied. Despite operating in with affine matrix the coordinates of the input points
    don't need to be in the affine space.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        affine_transform: The transformation to appyly with shape (4, 4).

    Returns:
        The transformed point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    transform = pt3d.Transform3d(dtype=pcd.dtype, device=str(pcd.device), matrix=affine_transform)
    return _apply_pt3d_transform(pcd, transform=transform, transform_normals=True)


def rotate(pcd: torch.Tensor, rotation: torch.Tensor) -> torch.Tensor:
    """Rotate a point cloud give the input matrix.

    Rotate the cloud using the same convention as in PyTorch3D: a right-hand coordinate system,
    meaning that rotation about an axis with a positive angle results in a counter clockwise
    rotation, more info at (https://pytorch3d.readthedocs.io).
    The points are multiplied using post-multiplication: rotated_points = points * rotation.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        rotation: The rotation matrix with shape (3, 3).

    Returns:
        The rotated point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    transform = pt3d.Rotate(rotation, dtype=pcd.dtype, device=str(pcd.device))
    return _apply_pt3d_transform(pcd, transform, transform_normals=True)


def scale(pcd: torch.Tensor, scale_factor: torch.Tensor) -> torch.Tensor:
    """Scale a point cloud given the input scale factor.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        scale: The scale factor for the x, y, z, dimensions with shape (3,).

    Returns:
        The scaled point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    scale_x, scale_y, scale_z = scale_factor[0], scale_factor[1], scale_factor[2]
    transform = pt3d.Scale(x=scale_x, y=scale_y, z=scale_z, dtype=pcd.dtype, device=str(pcd.device))

    return _apply_pt3d_transform(pcd, transform, transform_normals=False)


def translate(pcd: torch.Tensor, translation: torch.Tensor) -> torch.Tensor:
    """Translate a point cloud given the input translation.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        translation: The translation offset with shape (3,).

    Returns:
        The translated point cloud(s) with shape ([B,] NUM_POINTS, D).
    """
    x, y, z = translation[0], translation[1], translation[2]
    transform = pt3d.Translate(x=x, y=y, z=z, dtype=pcd.dtype, device=str(pcd.device))

    return _apply_pt3d_transform(pcd, transform, transform_normals=False)


def get_neighbouring_points(
    pcd: torch.Tensor,
    query_points: torch.Tensor,
    radius: float,
    max_num_neighbors: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Compute neighbouring points using radius search or a nearest neighbor search.

    This function computes the nearest neighbors in a point cloud for each query point specified in
    query_points. In order to arrange the points in batch, a maximum number of neighbors
    (max_num_neighbors) should be specified. If the points within the radius are less then
    max_num_neighbors the index of the query point is used to pad the batch.

    Args:
        pcd: The input point cloud(s) with shape ([B,] NUM_POINTS, D).
        query_points: The input point cloud(s) with shape ([B,] NUM_QUERY_POINTS, D).
        radius: the radius to use for the search.
        max_num_neighbors: the maximum number of neighbors to return.

    Raises:
        ValueError: if max_num_neighbors is zero.

    Returns:
        - The neighbors for each query point, with shape ([B,] NUM_QUERY_POINTS, max_num_neighbors).
          The indices are sorted in ascending order according to the euclidean distance from the
         query points.
        - The points in the pcd indexed by the nearest neihgbors indices, with
          shape ([B,] NUM_QUERY_POINTS, max_num_neighbors, 3).
    """
    batched, [pcd, query_points] = batchify([pcd, query_points], 3)
    if max_num_neighbors == 0:
        raise ValueError("Max number of neighbors is zero.")

    size_batch, _, point_dim = pcd.shape
    _, num_pts_query, _ = query_points.shape

    distances = get_distances_matrix(query_points, pcd)
    indices_nn = torch.empty([])

    if radius is not None:
        distances[distances > radius] = float("inf")
        distances_sorted, indices_nn = torch.sort(distances, dim=-1)
        indices_first_kp = (
            indices_nn[:, :, 0].view(size_batch, num_pts_query, 1).repeat([1, 1, max_num_neighbors])
        )
        mask = distances_sorted == float("inf")
        mask = mask[:, :, :max_num_neighbors]
        indices_nn = indices_nn[:, :, :max_num_neighbors]
        indices_nn[mask] = indices_first_kp[mask]
    else:
        _, indices_nn = torch.sort(distances, dim=-1)
        indices_nn = indices_nn[:, :, :max_num_neighbors]

    out_shape = (size_batch, num_pts_query, max_num_neighbors, point_dim)
    points_nn = torch.empty(out_shape, dtype=pcd.dtype, device=pcd.device)
    kpts_indices = torch.arange(num_pts_query)

    for b in range(size_batch):
        points_nn[b, kpts_indices] = pcd[b, indices_nn[b, kpts_indices]]

    if batched:
        [indices_nn, points_nn] = unbatchify([indices_nn, points_nn])

    return indices_nn, points_nn


def color_point_cloud(pcd: torch.Tensor, colors: torch.Tensor) -> o3d.geometry.PointCloud:
    """Create a open 3d cloud assigning a color to each points.

    Args:
        pcd: The numpy or torch point cloud with shape (NUM_POINTS, D).
        colors: The labels with shape (NUM_POINTS, 3).

    Returns:
        The colored point cloud.
    """
    pcd_o3d = get_o3d_from_tensor(pcd)
    pcd_o3d.colors = o3d.utility.Vector3dVector(colors.numpy())

    return pcd_o3d
