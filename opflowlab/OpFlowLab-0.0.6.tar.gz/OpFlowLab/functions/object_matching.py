import cv2
import numpy as np
from numba import njit, prange
from numba.typed import List


def remove_objects(ar, min_object_size=None, max_object_size=None):
    if min_object_size is not None or max_object_size is not None:
        if min_object_size is None:
            min_object_size = 0
        if max_object_size is None:
            max_object_size = np.inf

        out = ar.copy()
        ccs = out

        component_sizes = np.bincount(ccs.ravel())
        if min_object_size is not None:
            too_small = component_sizes < min_object_size
            too_small_mask = too_small[ccs]
            out[too_small_mask] = 0

        if max_object_size is not None:
            too_large = component_sizes > max_object_size
            too_large_mask = too_large[ccs]
            out[too_large_mask] = 0

        return out
    else:
        return ar


@njit(parallel=True)
def fast_distance_function(centroids, pos):
    n = centroids.shape[0]
    m = pos.shape[0]
    d = np.empty((m, n), dtype=centroids.dtype)

    for i in prange(m):
        for j in range(n):
            d[i, j] = ((centroids[j, 0] - pos[i, 0]) ** 2 + (centroids[j, 1] - pos[i, 1]) ** 2) ** 0.5
    return d


@njit
def calculate_distance(x, z, circular=True):
    dist = np.sqrt((x[1:] - x[:-1]) ** 2 + (z[1:] - z[:-1]) ** 2)

    if circular is True:
        np.append(dist, np.sqrt((x[-1] - x[0]) ** 2 + (z[-1] - z[0]) ** 2))
    return dist


@njit
def reslice_positions(x, y, num_points=21):
    output_x = np.empty(num_points, np.float32)
    output_y = np.empty(num_points, np.float32)

    profile_length = np.sum(calculate_distance(x, y))
    spacing = profile_length / num_points
    pos = 0

    for pt in range(num_points):
        if pt == 0:
            current_x = x[0]
            current_y = y[0]
        else:
            residual_spacing = spacing
            while True:
                pos += 1
                if pos >= x.shape[0]:
                    break
                distance = np.sqrt((x[pos] - current_x) ** 2 + (y[pos] - current_y) ** 2)

                if distance >= residual_spacing:
                    current_x = current_x + (x[pos] - current_x) / distance * residual_spacing
                    current_y = current_y + (y[pos] - current_y) / distance * residual_spacing
                    break
                else:
                    residual_spacing = residual_spacing - distance
                    current_x = x[pos]
                    current_y = y[pos]

        output_x[pt] = current_x
        output_y[pt] = current_y

    return output_x, output_y


@njit(parallel=True)
def get_pairs(properties, remapped_target_image, coord_pos=5):
    length = len(properties)
    forward_pair_list = np.full(length, np.nan)
    for i in range(length):
        obj = properties[i][coord_pos]
        lst = []
        for j in range(len(obj)):
            lst.append(remapped_target_image[obj[j, 0], obj[j, 1]])
        counts = np.bincount(lst)
        counts = counts / len(lst)

        forward_pair_list[i] = np.argmax(counts)

    return forward_pair_list


@njit(parallel=True)
def calculate_matched_velocities(initial_properties, target_properties, reverse_pair_list,
                                 forward_index, forward_unique, forward_bincount,
                                 reverse_unique, reverse_bincount, diff_search,
                                 matched_flow_x, matched_flow_y,
                                 selected_initial_mask, selected_target_mask,
                                 label_pos=0,
                                 ):
    for i in prange(len(forward_index)):
        initial_index = forward_index[i]
        target_value = forward_unique[i]
        forward_count = forward_bincount[i]

        search_start = np.maximum(target_value - diff_search - 1, 0)
        search_end = np.minimum(len(target_properties) + 1, target_value + 1)
        search_field = target_properties[search_start: search_end]

        for k in range(len(search_field)):
            if search_field[k][label_pos] == target_value:
                target_index = search_start + k

        initial_label = initial_properties[initial_index][label_pos]
        reverse_counts = reverse_bincount[np.where(reverse_unique == initial_label)[0]]
        if len(reverse_counts) > 0:
            reverse_count = reverse_counts[0]

            if reverse_pair_list[target_index] == initial_label:
                if forward_count == 1 and reverse_count == 1:
                    coords, output_velocity = single_object_velocity(initial_properties[initial_index],
                                                                     target_properties[target_index])

                    if coords is not None:
                        for ind in range(len(coords)):
                            matched_flow_x[np.int(coords[ind, 0]), np.int(coords[ind, 1])] = output_velocity[ind, 1]
                            matched_flow_y[np.int(coords[ind, 0]), np.int(coords[ind, 1])] = output_velocity[ind, 0]

                        selected_initial_mask[initial_index] = 0
                        selected_target_mask[target_index] = 0

    return matched_flow_x, matched_flow_y, selected_initial_mask, selected_target_mask


@njit
def single_object_velocity(object1_properties, object2_properties,
                           local_centroid_pos=1, centroid_pos=2,
                           orientation_pos=3, major_axis_pos=4,
                           coords_pos=5, contour_pos=6):
    pt1_local_centroid = np.array(object1_properties[local_centroid_pos])
    pt1_centroid = np.array(object1_properties[centroid_pos])
    pt1_orientation = object1_properties[orientation_pos]
    pt1_major_axis = object1_properties[major_axis_pos]
    pt1_coords = object1_properties[coords_pos]
    pt1_contour = object1_properties[contour_pos]

    pt1_perimeter = obtain_perimeter_points(pt1_local_centroid, pt1_orientation, pt1_major_axis, pt1_contour)

    pt2_local_centroid = np.array(object2_properties[local_centroid_pos])
    pt2_centroid = np.array(object2_properties[centroid_pos])
    pt2_orientation = object2_properties[orientation_pos]
    if np.abs(pt2_orientation - pt1_orientation) > np.pi / 2:
        pt2_orientation = np.pi + pt2_orientation
    pt2_major_axis = object2_properties[major_axis_pos]
    pt2_contour = object2_properties[contour_pos]

    pt2_perimeter = obtain_perimeter_points(pt2_local_centroid, pt2_orientation, pt2_major_axis, pt2_contour)

    # affine = ransac(pt1_perimeter, pt2_perimeter, num_pts=4, distance_threshold=1, iters=100)
    affine = estimate_affine(pt1_perimeter, pt2_perimeter)

    if affine is not None:
        temp_coords = pt1_coords - pt1_centroid + pt1_local_centroid

        temp_coords = np.ascontiguousarray(temp_coords.astype(np.float32).T)
        new_coords = (np.ascontiguousarray(affine[:, :2]) @ temp_coords).T + affine[:, 2]

        velocity = new_coords - temp_coords.T

        distance = np.sqrt((pt1_coords[:, 1] - pt1_centroid[1]) ** 2 + (pt1_coords[:, 0] - pt1_centroid[0]) ** 2)
        centroid_index = np.argmin(distance)
        local_velocity = velocity - velocity[centroid_index, :]

        output_velocity = local_velocity + pt2_centroid - pt1_centroid
        return pt1_coords, output_velocity
    else:
        return None, None


@njit
def obtain_perimeter_points(local_centroid, orientation, major_axis, contour):
    top_pt = local_centroid + np.array((np.cos(orientation) * major_axis / 2, np.sin(orientation) * major_axis / 2))

    distance = np.sqrt((contour[:, 0] - top_pt[1]) ** 2 + (contour[:, 1] - top_pt[0]) ** 2)
    start_point = np.argmin(distance)
    contour = np.vstack((contour[start_point:, ...], contour[:start_point, ...]))

    pt_x, pt_y = reslice_positions(contour[:, 0], contour[:, 1])

    pt_y = np.append(pt_y, local_centroid[0])
    pt_x = np.append(pt_x, local_centroid[1])
    pt_list = np.vstack((pt_y, pt_x)).T
    pt_list = pt_list.astype(np.float32)

    return pt_list


@njit
def estimate_affine(pt1_perimeter, pt2_perimeter):
    coefficient = np.empty((len(pt1_perimeter) * 2, 6))
    ordinate = np.empty((len(pt1_perimeter) * 2))
    for i in range(len(pt1_perimeter)):
        coefficient[2 * i] = [pt1_perimeter[i, 0], pt1_perimeter[i, 1], 1, 0, 0, 0]
        ordinate[2 * i] = pt2_perimeter[i, 0]
        coefficient[2 * i + 1] = [0, 0, 0, pt1_perimeter[i, 0], pt1_perimeter[i, 1], 1]
        ordinate[2 * i + 1] = pt2_perimeter[i, 1]

    solution = np.linalg.lstsq(coefficient, ordinate)[0]
    solution = np.reshape(solution, (2, 3))
    solution = solution.astype(np.float32)

    return solution


@njit
def ransac(pt1_perimeter, pt2_perimeter, num_pts=3, distance_threshold=2, model_threshold=0.5, iters=50):
    assert len(pt1_perimeter) == len(pt2_perimeter)
    output_matrix = None
    error = np.inf
    for _ in range(iters):
        sample_id = np.random.randint(0, len(pt1_perimeter), num_pts)
        pt1_sample = pt1_perimeter[sample_id, :]
        pt2_sample = pt2_perimeter[sample_id, :]

        affine_matrix = estimate_affine(pt1_sample, pt2_sample)

        pt1_temp = np.ascontiguousarray(pt1_perimeter.astype(np.float32).T)
        pt1_affine = (np.ascontiguousarray(affine_matrix[:, :2]) @ pt1_temp).T + affine_matrix[:, 2]

        distance = np.sqrt((pt2_perimeter[:, 1] - pt1_affine[:, 1])**2 + (pt2_perimeter[:, 0] - pt1_affine[:, 0])**2)

        if np.sum(distance < distance_threshold) > np.int(len(pt1_perimeter)*model_threshold):
            if np.sum(distance) < error:
                error = np.sum(distance)
                output_matrix = affine_matrix
    return output_matrix


def calculate_contour(label_image):
    contour, _ = cv2.findContours(np.array(label_image, dtype=np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contour) > 1:
        lengths = np.array([x.shape[0] for x in contour])
        index = np.argmax(lengths)
        contour = contour[index].squeeze()
    else:
        contour = contour[0].squeeze()

    return contour


@njit
def remove_items(properties, mask):
    output = List()
    for i in range(len(properties)):
        if mask[i] == 1:
            output.append(properties[i])

    return output
