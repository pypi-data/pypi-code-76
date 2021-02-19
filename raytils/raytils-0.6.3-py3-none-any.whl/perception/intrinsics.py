import numpy as np

__all__ = ["Intrinsics", "deproject_depth_image", "get_all_xy_pixel_coords", "get_all_yx_pixel_coords"]


class Intrinsics:
    """ Creates a projection matrix from fx, fy, cx, cy parameters

    Attributes:
        fx: Focal length of the x axis in pixels
        fy: Focal length of the y axis in pixels
        cx: Principal point of the x axis in pixels
        cy: Principal point of the y axis in pixels
        skew: The image skew in pixels
    """
    def __init__(self, fx: float, fy: float, cx: float, cy: float, skew: float = 0):
        self._fx = fx
        self._fy = fy
        self._cx = cx
        self._cy = cy
        self._skew = skew
        self.K = np.array([[fx, skew, cx], [0, fy, cy], [0, 0, 1]])

    @property
    def projection_matrix(self) -> np.array:
        """Returns the projection matrix K (3, 3) from [[fx, skew, cx], [0, fy, cy], [0, 0, 1]]"""
        return self.K


def get_all_xy_pixel_coords(height: int, width: int) -> np.array:
    """ Get pixel co-ordinates in x, y format (col major)

    Args:
        height: The height of the image
        width: The width of the image

    Returns:
        Numpy array of (height*width, 2) x, y coordinates for an image of size (height, width)
    """
    row_indices = np.arange(height)
    col_indices = np.arange(width)
    # Mesh grid col-row to get x, y not y, x
    pixel_grid = np.meshgrid(col_indices, row_indices)
    pixels_coords = np.c_[pixel_grid[0].flatten(), pixel_grid[1].flatten()].T
    return pixels_coords


def get_all_yx_pixel_coords(height: int, width: int) -> np.array:
    """ Get pixel co-ordinates in y, x format (row major)

    Args:
        height: The height of the image
        width: The width of the image

    Returns:
        Numpy array of (height*width, 2) y, x coordinates for an image of size (height, width)
    """
    row_indices = np.arange(height)
    col_indices = np.arange(width)
    # Mesh grid col-row to get x, y not y, x
    pixel_grid = np.meshgrid(row_indices, col_indices)
    pixels_coords = np.c_[pixel_grid[0].flatten(), pixel_grid[1].flatten()].T
    return pixels_coords


def deproject_depth_image_exp(depth_image: np.array, fx: float, fy: float, cx: float, cy: float):
    """ Deproject depth image into a point cloud image of shape [height, width, 3(x, y, z)]

    Args:
        depth_image: Numpy image of depth values in pixel format (int) of shape (height, width)
        fx: Focal length of the x axis in pixels
        fy: Focal length of the y axis in pixels
        cx: Principal point of the x axis in pixels
        cy: Principal point of the y axis in pixels

    Returns:
        Point cloud image of shape [height, width, 3(x, y, z)]
    """
    # Reformat intrinsics to 3x3 projection matrix
    intrinsics = Intrinsics(fx, fy, cx, cy)
    K = intrinsics.projection_matrix

    height, width = depth_image.shape[:2]
    pixels_coords = get_all_xy_pixel_coords(height, width)

    # Reshape pixels_coords from (height*width, 2) to (3, height*width) where [3] is a height*width array of 1.0
    pixels_homogeneous = np.r_[pixels_coords, np.ones([1, pixels_coords.shape[1]])]
    depth_array = np.tile(depth_image.data.flatten(), [3, 1])

    # Deproject to depth image
    points_3d = depth_array * np.linalg.inv(K).dot(pixels_homogeneous)
    point_cloud_image = points_3d.reshape(depth_image.height, depth_image.width, 3)
    return point_cloud_image


def deproject_depth_image(depth: np.ndarray, fx: float, fy: float, cx: float, cy: float, scale=10000.0):
    """ Deproject depth image into a point cloud image of shape [height, width, 3(x, y, z)]

    Args:
        depth: Numpy image of depth values in pixel format (int) of shape (height, width)
        fx: Focal length of the x axis in pixels
        fy: Focal length of the y axis in pixels
        cx: Principal point of the x axis in pixels
        cy: Principal point of the y axis in pixels
        scale: Scale of the point cloud (mm, cm, m etc)

    Returns:
        Points image of shape [height, width, 3(x, y, z)]
    """
    z_pos = (depth / scale).flatten()
    yx_pos = np.where(np.ones(depth.shape))

    points = np.ndarray((len(z_pos), 3))
    points[:, 0] = (yx_pos[1] - cx) * z_pos / fx
    points[:, 1] = ((yx_pos[0] - cy) * z_pos / fy) * -1
    points[:, 2] = z_pos * -1

    return points
