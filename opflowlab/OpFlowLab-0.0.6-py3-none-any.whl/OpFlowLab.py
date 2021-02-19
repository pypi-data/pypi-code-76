#!/usr/bin/env python3
import glob
import os
import sys
import warnings

import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage.color
import skimage.filters
import skimage.io
import skimage.measure
import skimage.metrics
import skimage.morphology
import skimage.transform
from numba.typed import List
from pykdtree.kdtree import KDTree
from tqdm import tqdm

from .functions import utils, object_matching, tracer_functions, interpolation, colormap_functions


class OpFlowLab:
    def __init__(self,
                 main_folder, image_file,
                 forward_velocity_folder=None, reverse_velocity_folder=None,
                 object_segmentation_folder=None,
                 velocity_type="dense", velocity_ext_type="*.bin", image_ext_type="*.tif",
                 velocity_dtype="float16", kernel_size=5):
        self.main_folder = main_folder
        self.velocity_type = velocity_type
        self.velocity_ext_type = velocity_ext_type
        self.image_ext_type = image_ext_type

        self.image = skimage.io.imread(image_file)
        self.image_shape = self.image.shape[1:]

        self.velocity_dtype = velocity_dtype
        self.kernel_size = kernel_size

        self.forward_velocity_filelist = None
        self.forward_velocity_folder = forward_velocity_folder
        self.reverse_velocity_filelist = None
        self.reverse_velocity_folder = reverse_velocity_folder
        self.object_segmentation_filelist = None
        self.object_segmentation_folder = object_segmentation_folder

        self.length = self.image.shape[0]

        if forward_velocity_folder is not None:
            self.initialize_forward_velocities(forward_velocity_folder)

        if reverse_velocity_folder is not None:
            self.initialize_reverse_velocities(self.reverse_velocity_folder)

        if object_segmentation_folder is not None:
            self.initialize_segmentation_folder(self.object_segmentation_folder)

        # TODO: Perform checks to ensure that all the filelists are of the correct length

    def parse_folder(self, folder):
        if os.path.isdir(folder):
            pass
        else:
            folder = os.path.join(self.main_folder, folder)
        return folder

    def initialize_forward_velocities(self, folder, velocity_type=None, velocity_ext_type=None):
        if velocity_type is None:
            velocity_type = self.velocity_type
        if velocity_ext_type is None:
            velocity_ext_type = self.velocity_ext_type
        self.forward_velocity_folder = self.parse_folder(folder)
        self.forward_velocity_filelist = utils.load_velocity_filelist(self.forward_velocity_folder,
                                                                      velocity_type=velocity_type,
                                                                      file_ext=velocity_ext_type,
                                                                      reverse_sort=False)

    def initialize_reverse_velocities(self, folder, velocity_type=None, velocity_ext_type=None):
        if velocity_type is None:
            velocity_type = self.velocity_type
        if velocity_ext_type is None:
            velocity_ext_type = self.velocity_ext_type
        self.reverse_velocity_folder = self.parse_folder(folder)
        self.reverse_velocity_filelist = utils.load_velocity_filelist(self.reverse_velocity_folder,
                                                                      velocity_type=velocity_type,
                                                                      file_ext=velocity_ext_type,
                                                                      reverse_sort=True)

    def initialize_segmentation_folder(self, folder, img_ext_type=None):
        if img_ext_type is None:
            img_ext_type = self.image_ext_type
        self.object_segmentation_folder = self.parse_folder(folder)
        self.object_segmentation_filelist = glob.glob(os.path.join(self.object_segmentation_folder, img_ext_type))
        self.object_segmentation_filelist.sort()

    def load_velocities(self, filelist, img_no):
        """
        Helper function to call the correct loading function based on the type of vectors as specified in
        self._vector_type

        Parameters
        ----------
        filelist : (list, list) or (list,)
            List
        img_no : int
            Index to indicate which file number to load

        Returns
        -------
        velocity_y : 2D numpy array
            Array containing the y component of the vectors from motion estimation analysis
        velocity_x : 2D numpy array
            Array containing the x component of the vectors from motion estimation analysis

        See Also
        --------
        utils.load_vectors_bin: Function to load vector information from optical flow generated *.bin files
        utils.load_vectors_piv: Function to load vector information from PIV generated *.mat files
        """
        velocity_x = None
        velocity_y = None
        if self.velocity_type == 'dense':
            velocity_x = utils.load_velocity_bin(filelist[0][img_no], self.image_shape,
                                                 bin_dtype=self.velocity_dtype, kernel_size=self.kernel_size)
            velocity_y = utils.load_velocity_bin(filelist[1][img_no], self.image_shape,
                                                 bin_dtype=self.velocity_dtype, kernel_size=self.kernel_size)

        elif self.velocity_type == 'sparse':
            velocity_x, velocity_y, x_array, y_array = utils.load_velocity_piv(filelist[0][0], img_no)

            data = np.c_[y_array.ravel(), x_array.ravel()]
            tree = KDTree(data, leafsize=16)

            x_pos, y_pos = np.meshgrid(np.arange(self.image_shape[1]), np.arange(self.image_shape[0]))
            pts = np.array(np.c_[y_pos.ravel(), x_pos.ravel()], dtype=np.float32)
            distances, indices = tree.query(pts, k=5, distance_upper_bound=32.0)
            pts = np.rint(pts).astype(np.int)

            coords = np.c_[velocity_y.ravel(), velocity_x.ravel()]
            piv_x_interpolate = np.zeros(self.image_shape)
            piv_y_interpolate = np.zeros(self.image_shape)

            velocity_x, velocity_y = interpolation.inverse_distance_weighting(pts, distances, indices, coords,
                                                                              piv_x_interpolate, piv_y_interpolate)
        return velocity_x, velocity_y

    def flowMatch_function(self,
                           output_folder="FlowMatch",
                           pairwise_threshold_distance=10,
                           min_object_size=None, max_object_size=None,
                           ):
        """
        Wrapper function that calls :func:`~object_matching_iteration` for each individual pair of frames in the
        image stack.

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store the interpolated vector fields
        pairwise_threshold_distance : int
            Distance between the propagated centroid location and the actual centroid location that is used as a cutoff for object matching
        min_object_size : int or None
            Minimum object size for it to be included in the matching process. Set to None to ignore this cutoff
        max_object_size : int or None
            Maximum object size for it to be included in the matching process. Set to None to ignore this cutoff

        Returns
        -------
        total_number_list : list
            List containing the total number of objects that are eligible for object matching for each frame
        matched_number_list : list
            List containing the total number of matched object for each frame

        See Also
        --------
        object_matching_iteration: function used to perform object matching and interpolation for a single frame
        """
        # create output folders
        flowx_output_directory = os.path.join(self.main_folder, output_folder, 'flowx')
        os.makedirs(flowx_output_directory, exist_ok=True)

        flowy_output_directory = os.path.join(self.main_folder, output_folder, 'flowy')
        os.makedirs(flowy_output_directory, exist_ok=True)

        total_number_list = []
        matched_number_list = []

        for img_no in tqdm(range(self.length - 1), file=sys.stdout):
            total_number, matched_number = self.flowMatch_iteration(img_no,
                                                                    flowx_output_directory,
                                                                    flowy_output_directory,
                                                                    pairwise_threshold_distance=pairwise_threshold_distance,
                                                                    min_object_size=min_object_size,
                                                                    max_object_size=max_object_size,
                                                                    )
            total_number_list.append(total_number)
            matched_number_list.append(matched_number)

        return total_number_list, matched_number_list

    def flowMatch_iteration(self,
                            frame_no,
                            flowx_output_directory, flowy_output_directory,
                            pairwise_threshold_distance=10,
                            min_object_size=None, max_object_size=None,
                            save_dtype="float16",
                            save_velocity_as_tif=False,
                            ):
        """
        Perform object matching of segmented objects using the provided motion estimation vector information for a
        single iteration and outputs an interpolated vector field using the velocity obtained from the matched objects.

        Parameters
        ----------
        frame_no : int
            Frame number with which to load vector
        flowx_output_directory : str
            Path to folder that will be used to store the x component of the interpolated vector field
        flowy_output_directory : str
            Path to folder that will be used to store the y component of the interpolated vector field
        pairwise_threshold_distance : int
            Distance between the propagated centroid location and the actual centroid location that is used as a cutoff for object matching
        min_object_size : int or None
            Minimum object size for it to be included in the matching process. Set to None to ignore this cutoff
        max_object_size : int or None
            Maximum object size for it to be included in the matching process. Set to None to ignore this cutoff
        save_dtype : str
            Save vectors as either float16 or float32 file
        save_velocity_as_tif : bool
            Save as float32 tif file instead of a float16 binary file


        Returns
        -------
        total_number : int
            Total number of objects that are eligible for object matching for each frame
        matched_number : int
            Total number of matched object for each frame

        See Also
        --------
        object_matching_function : wrapper function to perform object matching and interpolation on all frames
        """
        # obtain initial centroids
        initial_image = skimage.io.imread(self.object_segmentation_filelist[frame_no])
        if initial_image.shape != self.image_shape:
            print("Label image is not the same size as the input image. Resizing label image.")
            initial_image = cv2.resize(initial_image, (self.image_shape[1], self.image_shape[0]),
                                       interpolation=cv2.INTER_NEAREST)
        initial_object_properties = skimage.measure.regionprops(initial_image)
        initial_object_properties = np.array(initial_object_properties, dtype=object)
        initial_object_area = np.array([x['Area'] for x in initial_object_properties])
        area_mask = np.ones_like(initial_object_area)
        if min_object_size is not None:
            area_mask = np.logical_and(area_mask, initial_object_area > min_object_size)
        if max_object_size is not None:
            area_mask = np.logical_and(area_mask, initial_object_area < max_object_size)
        initial_object_properties = initial_object_properties[area_mask]

        initial_properties = List([(prop["label"], prop["local_centroid"], prop["centroid"], prop["orientation"],
                                    prop["major_axis_length"], prop["coords"],
                                    object_matching.calculate_contour(prop["image"]))
                                   for prop in initial_object_properties])

        counter = 0
        total_number = initial_object_properties.shape[0]
        matched_flow_x = np.full(self.image_shape, np.nan)
        matched_flow_y = np.full(self.image_shape, np.nan)
        centroid_list = [x[2] for x in initial_properties]

        # obtain target centroids
        target_image = skimage.io.imread(self.object_segmentation_filelist[frame_no + 1])
        if target_image.shape != self.image_shape:
            target_image = cv2.resize(target_image, (self.image_shape[1], self.image_shape[0]),
                                      interpolation=cv2.INTER_NEAREST)

        target_object_properties = skimage.measure.regionprops(target_image)
        target_object_properties = np.array(target_object_properties, dtype=object)

        target_object_area = np.array([x['Area'] for x in target_object_properties])
        area_mask = np.ones_like(target_object_area)
        if min_object_size is not None:
            area_mask = np.logical_and(area_mask, target_object_area > min_object_size)
        if max_object_size is not None:
            area_mask = np.logical_and(area_mask, target_object_area < max_object_size)
        target_object_properties = target_object_properties[area_mask]

        target_properties = List([(prop["label"], prop["local_centroid"], prop["centroid"], prop["orientation"],
                                   prop["major_axis_length"], prop["coords"],
                                   object_matching.calculate_contour(prop["image"]))
                                  for prop in target_object_properties])

        # load forward vectors
        forward_velocity_x, forward_velocity_y = self.load_velocities(self.forward_velocity_filelist, frame_no)
        # load reverse vectors
        reverse_velocity_x, reverse_velocity_y = self.load_velocities(self.reverse_velocity_filelist, frame_no)

        remap_x, remap_y = interpolation.inverse_mapping(reverse_velocity_x, reverse_velocity_y, self.image_shape)
        remapped_target_image = cv2.remap(target_image, remap_x.astype(np.float32), remap_y.astype(np.float32),
                                          cv2.INTER_NEAREST)

        forward_pair_list = object_matching.get_pairs(initial_properties, remapped_target_image)
        forward_pair_list = forward_pair_list[~np.isnan(forward_pair_list)]
        forward_pair_list = forward_pair_list.astype(np.int)

        remap_x, remap_y = interpolation.inverse_mapping(forward_velocity_x, forward_velocity_y, self.image_shape)
        remapped_initial_image = cv2.remap(initial_image, remap_x.astype(np.float32), remap_y.astype(np.float32),
                                           cv2.INTER_NEAREST)

        reverse_pair_list = object_matching.get_pairs(target_properties, remapped_initial_image)
        reverse_pair_list = reverse_pair_list[~np.isnan(reverse_pair_list)]
        reverse_pair_list = reverse_pair_list.astype(np.int)

        forward_unique, forward_index, forward_bincount = np.unique(forward_pair_list, return_index=True,
                                                                    return_counts=True)
        reverse_unique, reverse_index, reverse_bincount = np.unique(reverse_pair_list, return_index=True,
                                                                    return_counts=True)

        diff_search = np.max(target_image) - len(target_properties)

        selected_initial_mask = np.ones(len(initial_properties), np.bool)
        selected_target_mask = np.ones(len(target_properties), np.bool)

        matched_flow_x, matched_flow_y, selected_initial_mask, selected_target_mask = object_matching.calculate_matched_velocities(
            initial_properties,
            target_properties,
            reverse_pair_list,
            forward_index,
            forward_unique,
            forward_bincount,
            reverse_unique,
            reverse_bincount,
            diff_search,
            matched_flow_x,
            matched_flow_y,
            selected_initial_mask,
            selected_target_mask,
        )

        counter += np.count_nonzero(~selected_initial_mask)

        initial_properties = object_matching.remove_items(initial_properties, selected_initial_mask)
        target_properties = object_matching.remove_items(target_properties, selected_target_mask)
        unselected_initial = np.array([x[2] for x in initial_properties])
        unselected_target = np.array([x[2] for x in target_properties])

        # Round 2
        forward_velocity_x_smooth = skimage.filters.gaussian(forward_velocity_x, 15, preserve_range=True)
        forward_velocity_y_smooth = skimage.filters.gaussian(forward_velocity_y, 15, preserve_range=True)

        reverse_velocity_x_smooth = skimage.filters.gaussian(reverse_velocity_x, 15, preserve_range=True)
        reverse_velocity_y_smooth = skimage.filters.gaussian(reverse_velocity_y, 15, preserve_range=True)

        selected_initial_mask = np.ones(len(unselected_initial), np.bool)
        selected_target_mask = np.ones(len(unselected_target), np.bool)

        # perform backward propagation of target centroids
        forward_propagated_centroids = tracer_functions.update_tracer(unselected_initial, forward_velocity_y_smooth,
                                                                      forward_velocity_x_smooth)

        # perform backward propagation of target centroids
        backward_propagated_centroids = tracer_functions.update_tracer(unselected_target, reverse_velocity_y_smooth,
                                                                       reverse_velocity_x_smooth)

        # perform nuclei matching by propagating the nuclei centroids with the flow vectors
        forward_difference = object_matching.fast_distance_function(unselected_target, forward_propagated_centroids)
        backward_difference = object_matching.fast_distance_function(unselected_initial,
                                                                     backward_propagated_centroids).T

        raw_difference = object_matching.fast_distance_function(unselected_target, unselected_initial)

        for initial_index in range(forward_difference.shape[0]):
            i = np.argsort(forward_difference[initial_index, :])[0]
            k = np.argsort(backward_difference[initial_index, :])[0]
            j = np.argsort(raw_difference[initial_index, :])[0]

            if i == j and forward_difference[initial_index, i] < pairwise_threshold_distance:
                target_index = j
                coords, output_velocity = object_matching.single_object_velocity(initial_properties[initial_index],
                                                                                 target_properties[target_index])

                if coords is not None:
                    coords = np.rint(coords).astype(np.int)
                    matched_flow_x[coords[:, 0], coords[:, 1]] = output_velocity[:, 1]
                    matched_flow_y[coords[:, 0], coords[:, 1]] = output_velocity[:, 0]

                    selected_initial_mask[initial_index] = 0
                    selected_target_mask[target_index] = 0
                    counter += 1

            elif k == j and backward_difference[initial_index, k] < pairwise_threshold_distance:
                target_index = j
                coords, output_velocity = object_matching.single_object_velocity(initial_properties[initial_index],
                                                                                 target_properties[target_index])

                if coords is not None:
                    coords = np.rint(coords).astype(np.int)
                    matched_flow_x[coords[:, 0], coords[:, 1]] = output_velocity[:, 1]
                    matched_flow_y[coords[:, 0], coords[:, 1]] = output_velocity[:, 0]

                    selected_initial_mask[initial_index] = 0
                    selected_target_mask[target_index] = 0
                    counter += 1

        unselected_initial2 = unselected_initial[selected_initial_mask]
        unselected_target2 = unselected_target[selected_target_mask]
        initial_properties = object_matching.remove_items(initial_properties, selected_initial_mask)
        target_properties = object_matching.remove_items(target_properties, selected_target_mask)

        # Round 3

        magnitude = np.sqrt(np.array(matched_flow_x) ** 2 + np.array(matched_flow_y) ** 2)
        mean_magnitude = np.nanmean(magnitude)
        std_magnitude = np.nanstd(magnitude)

        velocity_threshold_distance = mean_magnitude + 2 * std_magnitude

        while True:
            old_counter = counter
            final_difference = object_matching.fast_distance_function(unselected_target2, unselected_initial2)
            difference_mask = final_difference < velocity_threshold_distance

            pairs = np.sum(difference_mask, axis=0)
            indices = np.where(pairs == 1)[0]

            selected_initial_mask = np.ones(len(unselected_initial2), np.bool)
            selected_target_mask = np.ones(len(unselected_target2), np.bool)

            for target_index in indices:
                initial_index = np.where(difference_mask[:, target_index] == 1)[0][0]
                coords, output_velocity = object_matching.single_object_velocity(initial_properties[initial_index],
                                                                                 target_properties[target_index])

                if coords is not None:
                    coords = np.rint(coords).astype(np.int)
                    matched_flow_x[coords[:, 0], coords[:, 1]] = output_velocity[:, 1]
                    matched_flow_y[coords[:, 0], coords[:, 1]] = output_velocity[:, 0]

                    selected_initial_mask[initial_index] = 0
                    selected_target_mask[target_index] = 0
                    counter += 1

            unselected_initial2 = unselected_initial2[selected_initial_mask]
            unselected_target2 = unselected_target2[selected_target_mask]
            initial_properties = object_matching.remove_items(initial_properties, selected_initial_mask)
            target_properties = object_matching.remove_items(target_properties, selected_target_mask)
            # print(len(unselected_initial2), len(unselected_target2))

            final_difference = object_matching.fast_distance_function(unselected_target2, unselected_initial2)
            difference_mask = final_difference < velocity_threshold_distance

            pairs = np.sum(difference_mask, axis=1)
            indices = np.where(pairs == 1)[0]

            selected_initial_mask = np.ones(len(unselected_initial2), np.bool)
            selected_target_mask = np.ones(len(unselected_target2), np.bool)

            for initial_index in indices:
                target_index = np.where(difference_mask[initial_index, :] == 1)[0][0]
                coords, output_velocity = object_matching.single_object_velocity(initial_properties[initial_index],
                                                                                 target_properties[target_index])

                if coords is not None:
                    coords = np.rint(coords).astype(np.int)
                    matched_flow_x[coords[:, 0], coords[:, 1]] = output_velocity[:, 1]
                    matched_flow_y[coords[:, 0], coords[:, 1]] = output_velocity[:, 0]

                    selected_initial_mask[initial_index] = 0
                    selected_target_mask[target_index] = 0
                    counter += 1

            unselected_initial2 = unselected_initial2[selected_initial_mask]
            unselected_target2 = unselected_target2[selected_target_mask]
            initial_properties = object_matching.remove_items(initial_properties, selected_initial_mask)
            target_properties = object_matching.remove_items(target_properties, selected_target_mask)
            # print(len(unselected_initial2), len(unselected_target2))

            if old_counter == counter:
                break

        selected_centroid, counts = np.unique(np.vstack((np.array(centroid_list), unselected_initial2)), axis=0,
                                              return_counts=True)
        selected_centroid = selected_centroid[counts == 1]
        matched_y_pos, matched_x_pos = selected_centroid.T
        cen_round = np.rint(selected_centroid).astype(np.int32)
        flow_x_cen = matched_flow_x.ravel()[np.ravel_multi_index(cen_round.T, self.image_shape)]
        flow_y_cen = matched_flow_y.ravel()[np.ravel_multi_index(cen_round.T, self.image_shape)]

        data = np.c_[matched_y_pos.astype(np.float32).ravel(), matched_x_pos.astype(np.float32).ravel()]
        tree = KDTree(data, leafsize=16)

        nanpos = np.argwhere(np.isnan(matched_flow_x))
        y_pos = nanpos[:, 0]
        x_pos = nanpos[:, 1]

        pts = np.array(np.c_[y_pos.ravel(), x_pos.ravel()], dtype=np.float32)
        distances, indices = tree.query(pts, k=10, distance_upper_bound=64.0)

        values = np.c_[flow_y_cen, flow_x_cen]

        interpolated_flow_x, interpolated_flow_y = interpolation.inverse_distance_weighting(pts.astype(np.int),
                                                                                            distances, indices,
                                                                                            values,
                                                                                            matched_flow_x,
                                                                                            matched_flow_y)

        # x component
        utils.save_output(interpolated_flow_x,
                          os.path.join(flowx_output_directory, 'flowx_{:03d}_float16'.format(frame_no + 1)),
                          save_velocity_as_tif=save_velocity_as_tif, save_dtype=save_dtype)

        # y component
        utils.save_output(interpolated_flow_y,
                          os.path.join(flowy_output_directory, 'flowy_{:03d}_float16'.format(frame_no + 1)),
                          save_velocity_as_tif=save_velocity_as_tif, save_dtype=save_dtype)

        return total_number, counter

    def flowWarp_function(self,
                          output_folder="FlowWarp",
                          start_frame=0,
                          ):
        transformation_folder = os.path.join(self.forward_velocity_folder, output_folder)
        os.makedirs(transformation_folder, exist_ok=True)

        for frame_no in tqdm(range(start_frame, self.length - 1)):
            tracer_pos, _ = self.flowWarp_iteration(frame_no, transformation_folder)

    def flowWarp_iteration(self,
                           frame_no,
                           transformation_folder):
        flow_x, flow_y = self.load_velocities(self.forward_velocity_filelist, frame_no)
        img_frame = self.image[frame_no]

        map1_inverse, map2_inverse = interpolation.inverse_mapping(flow_x, flow_y, self.image_shape)
        remapped_image = cv2.remap(img_frame, map1_inverse.astype(np.float32),
                                   map2_inverse.astype(np.float32), cv2.INTER_CUBIC)

        output_image = np.dstack((self.image[frame_no + 1], remapped_image))
        output_image = np.moveaxis(output_image, -1, 0)

        skimage.io.imsave(os.path.join(transformation_folder, 'output_{:03d}.tif'.format(frame_no)), output_image,
                          check_contrast=False, metadata={'mode': 'composite'}, imagej=True)

        nrmse = skimage.metrics.normalized_root_mse(self.image[frame_no + 1], remapped_image)

        return nrmse, output_image

    def flowPath_function(self,
                          output_folder="FlowPath",
                          start_frame=0, frames=10,
                          alpha=0,
                          spacing=8,
                          max_tracers=None,
                          ):
        """
        Wrapper function that calls :func:`~flow_path_iteration` for each frames in the image stack.

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store the vector trace images
        start_frame : int
            Frame number with which to start vector trace visualization
        frames : int
            Length of trails in number of frames that will be drawn for each artificial tracer
        spacing : int
            Grid spacing used to initialize tracers
        max_tracers : int or None
            Maximum number of tracers to be used in the calculation [Currently unused]

        Returns
        -------
        None

        See Also
        --------
        initialize_flow_path : function used to initialize tracers
        flow_path_iteration : function used to perform vector trace visualization for a single frame
        """
        # create output folders
        flow_trace_folder = os.path.join(self.forward_velocity_folder, output_folder)
        os.makedirs(flow_trace_folder, exist_ok=True)

        tracer_pos, all_pos_index, x_array_shape = self.flowPath_initialization(frames=frames,
                                                                                spacing=spacing,
                                                                                max_tracers=max_tracers)

        for frame_no in tqdm(range(start_frame, self.length - 1)):
            img_frame = None
            if alpha != 0:
                img_frame = self.image[frame_no]
            tracer_pos, _ = self.flowPath_iteration(frame_no, tracer_pos, all_pos_index, x_array_shape,
                                                    flow_trace_folder,
                                                    alpha=alpha,
                                                    img_frame=img_frame,
                                                    frames=frames,
                                                    spacing=spacing,
                                                    )

    def flowPath_initialization(self,
                                frames=10,
                                spacing=8,
                                max_tracers=None,
                                ):
        """
        Initializes the tracers that will be used for vector trace visualization

        Parameters
        ----------
        frames : int
            Length of trails in number of frames that will be drawn for each artificial tracer
        spacing : int
            Grid spacing used to initialize tracers.
        max_tracers : int or None
            Maximum number of tracers to be used in the calculation [Currently unused]

        Returns
        -------
        tracer_pos : 3D array of shape (frames, tracer_no, 2)
            Array containing the positions of the tracers in the format [y,x]
        all_pos_index: iter
            Iterable that outputs the tracer number
        x_array_shape: (int, int)
            Tuple containing the shape of the grid used to generate tracers

        See Also
        --------
        initialize_flow_path : function used to initialize tracers
        flow_path_iteration: function used to perform vector trace visualization for a single frame
        """
        if max_tracers is None:
            max_tracers = self.image_shape[0] * self.image_shape[1]

        tracer_pos = np.full((frames, max_tracers, 2), fill_value=np.nan)

        x = np.arange(spacing // 2, self.image_shape[1], spacing, dtype=np.float32)
        y = np.arange(spacing // 2, self.image_shape[0], spacing, dtype=np.float32)
        x_array, y_array = np.meshgrid(x, y)
        x_array_shape = x_array.shape

        all_pos_index = np.arange(x_array_shape[0] * x_array_shape[1])

        tracer_pos[0, :x_array.flatten().shape[0], 1] = x_array.flatten()
        tracer_pos[0, :y_array.flatten().shape[0], 0] = y_array.flatten()

        return tracer_pos, all_pos_index, x_array_shape

    def flowPath_iteration(self,
                           frame_no, tracer_pos, all_pos_index, x_array_shape,
                           flow_trace_folder,
                           alpha=0,
                           img_frame=None,
                           frames=10,
                           spacing=8,
                           ):
        """
        Calculates and outputs vector traces for a single iteration

        Parameters
        ----------
        frame_no : int
            Frame number with which to perform vector trace visualization
        tracer_pos : 3D array of shape (frames, tracer_no, 2)
            Array containing the positions of the tracers in the format [y,x]
        all_pos_index: iter
            Iterable that outputs the tracer number
        x_array_shape: (int, int)
            Tuple containing the shape of the grid used to generate tracers
        flow_trace_folder : str
            Folder name that will be created in the main directory to store the vector trace images
        frames : int
            Length of trails in number of frames that will be drawn for each artificial tracer
        spacing : int
            Grid spacing used to initialize tracers

        Returns
        -------
        tracer_pos : 3D array of shape (frames, tracer_no, 2)
            Array containing the positions of the tracers in the format [y,x]
        output_image : 3D array of shape (m, n, 3)
            RGB image showing the tails of the tracers

        See Also
        --------
        initialize_flow_path : function used to initialize tracers
        plot_flow_path: wrapper function to perform vector trace visualization on all frames
        """
        # load velocity
        flow_x, flow_y = self.load_velocities(self.forward_velocity_filelist, frame_no)

        temp_tracer_pos = tracer_functions.update_tracer(tracer_pos[0, ...], flow_y, flow_x)

        tracer_pos = np.delete(tracer_pos, -1, axis=0)
        tracer_pos = np.insert(tracer_pos, 0, temp_tracer_pos, axis=0)

        # Identify valid tracers to draw
        draw_pos = np.any(~np.isnan(tracer_pos), axis=(0, 2))
        draw_tracer_pos = tracer_pos[:, draw_pos, :]
        draw_tracer_pos = np.rint(draw_tracer_pos)

        # Identify empty locations
        filled_pos = tracer_pos[:(frames // 2), ...][~np.all(np.isnan(tracer_pos[:(frames // 2), ...]), axis=2)]
        filled_pos = np.floor_divide(filled_pos, spacing)
        filled_index = np.ravel_multi_index(np.array(filled_pos, dtype=np.int).T, x_array_shape, mode='clip')
        diff_index = np.setdiff1d(all_pos_index, filled_index)

        # fill in additional tracers
        empty_pos = np.where(np.all(np.isnan(tracer_pos), axis=(0, 2)))[0]
        for i, index in enumerate(diff_index):
            y, x = np.unravel_index(index, x_array_shape)
            tracer_pos[0, empty_pos[i], :] = [y * spacing + spacing // 2, x * spacing + spacing // 2]

        # catch and ignore warning when the values are all nan
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            x_diff = np.nanmean(draw_tracer_pos[-2::-1, :, 1] - draw_tracer_pos[-1:0:-1, :, 1], axis=0)
            y_diff = np.nanmean(draw_tracer_pos[-2::-1, :, 0] - draw_tracer_pos[-1:0:-1, :, 0], axis=0)

        # obtain colors for drawing
        metric = np.arctan2(y_diff, -x_diff, where=~(np.isnan(x_diff) | np.isnan(y_diff))) * 180 / np.pi
        colors = colormap_functions.get_colors(metric, plt.cm.twilight, vmin=-180, vmax=180)

        if alpha != 0:
            output_image = skimage.color.gray2rgb(alpha * utils.imadjust(img_frame))
            output_image = output_image/np.max(output_image)
            output_image = skimage.util.img_as_ubyte(output_image)
        else:
            output_image = np.ones(self.image_shape + (3,), dtype=np.uint8) * 101

        for i in range(0, draw_tracer_pos.shape[1], 1):
            points = draw_tracer_pos[np.newaxis, :, i, ::-1]  # opencv takes (x,y)
            nan_pos = np.all(~np.isnan(points), axis=-1)
            points = np.array(points[np.newaxis, nan_pos, :], dtype=np.int)
            output_image = cv2.polylines(output_image, points, isClosed=False, color=colors[i, :3] * 255)

        skimage.io.imsave(os.path.join(flow_trace_folder, 'output_{:03d}.tif'.format(frame_no)), output_image,
                          check_contrast=False)

        return tracer_pos, output_image

    def flowTracer_function(self,
                            output_folder="FlowTracer",
                            save_initial_tracer_pos=True,
                            use_random_tracers=True,
                            tracer_no=10000,
                            spacing=16,
                            start_frame=0,
                            ):
        """
        Iterates and plots positions of artificial tracers based on provided motion estimation vectors

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store the artificial tracer images
        save_initial_tracer_pos : Bool
            Save initial tracer positions
        use_random_tracers : Bool
            If true, generate tracer positions based on a regular grid. If false, generate random position for tracers.
        tracer_no : int
            Maximum number of artificial tracers to use
        start_frame : int
            Frame number with which to start vector trace visualization
        spacing : int
            Grid spacing used to initialize tracers
        start_frame : int
            Frame number with which to start vector trace visualization

        Returns
        -------

        See Also
        --------

        """
        tracer_folder = os.path.join(self.forward_velocity_folder, output_folder)
        os.makedirs(tracer_folder, exist_ok=True)

        tracer_centroids, color = self.flowTracer_initialization(save_initial_tracer_pos=save_initial_tracer_pos,
                                                                 use_random_tracers=use_random_tracers,
                                                                 tracer_no=tracer_no,
                                                                 spacing=spacing,
                                                                 )

        # save first image
        self.flowTracer_first_frame(tracer_folder,
                                    start_frame, tracer_centroids, color,
                                    )

        for frame_no in tqdm(range(start_frame, self.length - 1)):
            tracer_centroids, output_image = self.flowTracer_iteration(tracer_folder,
                                                                       frame_no, tracer_centroids, color,
                                                                       )

    def flowTracer_initialization(self,
                                  save_initial_tracer_pos=True,
                                  use_random_tracers=True,
                                  tracer_no=10000,
                                  spacing=16,
                                  segmentation_filelist=None,
                                  ):
        """
        Initializes the tracers that will be used for vector trace visualization

        Parameters
        ----------
        save_initial_tracer_pos : bool
            Set to True to save initial positions
        use_random_tracers : bool
            Set to True to use tracers with randomly defined starting x,y positions
        spacing : int
            Grid spacing used to initialize tracers.
        tracer_no : int or None
            Maximum number of tracers to be used in the calculation [Currently unused]

        Returns
        -------
        tracer_pos : 2D array of shape (tracer_no, 2)
            Array containing the positions of the tracers in the format [y,x]
        all_pos_index: iter
            Iterable that outputs the tracer number
        x_array_shape: (int, int)
            Tuple containing the shape of the grid used to generate tracers

        See Also
        --------
        initialize_flow_path : function used to initialize tracers
        flow_path_iteration: function used to perform vector trace visualization for a single frame
        """
        if segmentation_filelist is not None:
            initial_image = skimage.io.imread(self.object_segmentation_filelist[0])
            if initial_image.shape != self.image_shape:
                print("Label image is not the same size as the input image. Resizing label image.")
                initial_image = cv2.resize(initial_image, (self.image_shape[1], self.image_shape[0]),
                                           interpolation=cv2.INTER_NEAREST)
            # initial_image = object_matching.remove_objects(initial_image, 100, 2000)
            initial_object_properties = skimage.measure.regionprops(initial_image)
            initial_object_centroids = np.array([np.array(x['Centroid']) for x in initial_object_properties])

            tracer_x = np.array(initial_object_centroids[:, 1], dtype=np.float32)
            tracer_y = np.array(initial_object_centroids[:, 0], dtype=np.float32)

        elif use_random_tracers:
            tracer_x = np.array(np.random.randint(1, self.image_shape[1], tracer_no), dtype=np.float32)
            tracer_y = np.array(np.random.randint(1, self.image_shape[0], tracer_no), dtype=np.float32)
        else:
            x = np.arange(spacing // 2, self.image_shape[1], spacing, dtype=np.float32)
            y = np.arange(spacing // 2, self.image_shape[0], spacing, dtype=np.float32)
            x_array, y_array = np.meshgrid(x, y)
            tracer_x = x_array.flatten()
            tracer_y = y_array.flatten()

        tracer_centroids = np.array((tracer_y, tracer_x)).T

        color = np.array([colormap_functions.create_color() for _ in range(tracer_centroids.shape[0])])

        if save_initial_tracer_pos:
            import pickle
            tracer_coord = {'tracer_x': tracer_x,
                            'tracer_y': tracer_y,
                            'color': color,
                            }

            with open(os.path.join(self.main_folder, 'tracer.pkl'), 'wb') as file:
                pickle.dump(tracer_coord, file)

        return tracer_centroids, color

    def flowTracer_first_frame(self,
                               tracer_folder,
                               frame_no, tracer_centroids, color,
                               ):
        first_image = skimage.color.gray2rgb(self.image[frame_no, ...]) / 255
        output_image = tracer_functions.draw_tracer(first_image, tracer_centroids, color)

        skimage.io.imsave(os.path.join(tracer_folder, 'output_{:03d}.tif'.format(frame_no)),
                          (output_image * 255).astype(np.uint8))

        return output_image

    def flowTracer_iteration(self,
                             tracer_folder,
                             frame_no, tracer_centroids, color,
                             ):
        """
        Calculates and outputs vector traces for a single iteration

        Parameters
        ----------
        frame_no : int
            Frame number with which to perform vector trace visualization
        tracer_centroids : 3D array of shape (frames, tracer_no, 2)
            Array containing the positions of the tracers in the format [y,x]
        color : 2D array
            Array containing the color information for each tracer
        tracer_folder : str
            Folder name that will be created in the main directory to store the artificial tracer images

        Returns
        -------
        tracer_centroids : 3D array of shape (frames, tracer_no, 2)
            Array containing the positions of the tracers in the format [y,x]
        output_image : 3D array of shape (m, n, 3)
            RGB image showing the tails of the tracers

        See Also
        --------
        initialize_flow_path : function used to initialize tracers
        plot_flow_path: wrapper function to perform vector trace visualization on all frames
        """
        flow_x, flow_y = self.load_velocities(self.forward_velocity_filelist, frame_no)

        tracer_centroids = tracer_functions.update_tracer(tracer_centroids, flow_y, flow_x)

        # Identify valid tracers to draw
        draw_pos = np.any(~np.isnan(tracer_centroids), axis=1)
        draw_tracer_pos = tracer_centroids[draw_pos, :]
        draw_colors = color[draw_pos]
        draw_tracer_pos = np.rint(draw_tracer_pos)

        output_image = tracer_functions.draw_tracer(skimage.color.gray2rgb(self.image[frame_no + 1, ...]) / 255,
                                                    draw_tracer_pos, draw_colors)

        skimage.io.imsave(os.path.join(tracer_folder, 'output_{:03d}.tif'.format(frame_no + 1)),
                          (output_image * 255).astype(np.uint8))

        return tracer_centroids, output_image

    def flowDerivative_iteration(self,
                                 output_folder, frame_no,
                                 stat_matrix=None,
                                 file_string=None,
                                 smoothing=None,
                                 colormap=None,
                                 colormap_min=-1.5, colormap_max=1.5,
                                 ):
        """
        Calculates gradients and output the various flow derivatives for a single iteration

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store flow derivative images
        frame_no : int
            Frame number with which to calculate flow derivatives
        stat_matrix : 2D array of shape (2, 2)
            Array containing formulation of
        file_string: str
            File name in the format '[name]_{:03d}.tif'
        colormap : str or None
            Colormap to plot
        smoothing : int
            Size of gaussian smoothing kernel
        colormap_min : float
            Minimum value that will be used for colormap normalization
        colormap_max : float
            Maximum value that will be used for colormap normalization

        Returns
        -------
        output_image : 2D array
            Output image containing the colorized flow derivative

        See Also
        --------
        plot_curl : wrapper function to plot curl for all frames
        plot_divergence : wrapper function to plot divergence for all frames
        plot_simple_shear : wrapper function to plot simple shear for all frames
        """
        _colormap = colormap_functions.parse_colormap(colormap)

        flow_x, flow_y = self.load_velocities(self.forward_velocity_filelist, frame_no)

        if smoothing is not None:
            from scipy.ndimage import gaussian_filter
            flow_x = gaussian_filter(flow_x, smoothing)
            flow_y = gaussian_filter(flow_y, smoothing)

        dflowx_dy, dflowx_dx = np.gradient(flow_x)
        dflowy_dy, dflowy_dx = np.gradient(flow_y)

        # negative sign needed due to the fact that the yaxis is inverted
        stat = -np.array([[dflowx_dy, dflowx_dx], [dflowy_dy, dflowy_dx]]) * stat_matrix[..., np.newaxis, np.newaxis]
        stat = np.sum(stat, axis=(0, 1))

        if _colormap is None:
            skimage.io.imsave(os.path.join(output_folder, file_string.format(frame_no)), stat,
                              check_contrast=False)
        else:
            output_image = colormap_functions.get_colors(stat, _colormap, vmin=colormap_min, vmax=colormap_max)
            output_image = output_image[..., :3]  # remove alpha layer
            output_image = skimage.util.img_as_ubyte(output_image)
            skimage.io.imsave(os.path.join(output_folder, file_string.format(frame_no)), output_image,
                              check_contrast=False)

        return stat

    def flowCurl_function(self,
                          output_folder="curl",
                          smoothing=None,
                          vmin=-1.5, vmax=1.5,
                          ):
        """
        Calculates gradients and output the curl values for an image stack

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store flow derivative images
        smoothing : int or Bool
            Sigma value for gaussian smoothing
        vmin : float
            Minimum value that will be used for colormap normalization
        vmax : float
            Maximum value that will be used for colormap normalization

        Returns
        -------

        See Also
        --------
        plot_stat_iter : base function to generate flow derivative images
        """
        curl_folder = os.path.join(self.forward_velocity_folder, output_folder)
        os.makedirs(curl_folder, exist_ok=True)
        curl_string = 'curl_{:03d}.tif'

        curl_stat_matrix = np.array([[-1, 0], [0, 1]])
        for img_no in tqdm(range(self.length - 1)):
            self.flowDerivative_iteration(curl_folder, img_no, curl_stat_matrix, curl_string,
                                          smoothing=smoothing,
                                          colormap=plt.cm.coolwarm,
                                          colormap_min=vmin, colormap_max=vmax,
                                          )

    def flowDivergence_function(self,
                                output_folder="divergence",
                                smoothing=None,
                                vmin=-1.5, vmax=1.5,
                                ):
        """
        Calculates gradients and output the divergence values for an image stack

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store flow derivative images
        smoothing : int or Bool
            Sigma value for gaussian smoothing
        vmin : float
            Minimum value that will be used for colormap normalization
        vmax : float
            Maximum value that will be used for colormap normalization

        Returns
        -------

        See Also
        --------
        plot_stat_iter : base function to generate flow derivative images
        """
        divergence_folder = os.path.join(self.forward_velocity_folder, output_folder)
        os.makedirs(divergence_folder, exist_ok=True)
        divergence_string = 'divergence_{:03d}.tif'

        divergence_stat_matrix = np.array([[0, 1], [1, 0]])
        for img_no in tqdm(range(self.length - 1)):
            self.flowDerivative_iteration(divergence_folder, img_no, divergence_stat_matrix, divergence_string,
                                          smoothing=smoothing,
                                          colormap=plt.cm.coolwarm,
                                          colormap_min=vmin, colormap_max=vmax,
                                          )

    def flowShear_function(self,
                           output_folder="shear",
                           smoothing=None,
                           vmin=-1.5, vmax=1.5,
                           ):
        """
        Calculates gradients and output the simple shear values for an image stack

        Parameters
        ----------
        output_folder : str
            Folder name that will be created in the main directory to store flow derivative images
        smoothing : int or Bool
            Sigma value for gaussian smoothing
        vmin : float
            Minimum value that will be used for colormap normalization
        vmax : float
            Maximum value that will be used for colormap normalization

        Returns
        -------

        See Also
        --------
        plot_stat_iter : base function to generate flow derivative images
        """
        shear_folder = os.path.join(self.forward_velocity_folder, output_folder)
        os.makedirs(shear_folder, exist_ok=True)
        shear_string = 'shear_{:03d}.tif'

        shear_stat_matrix = np.array([[1, 0], [0, 1]])
        for img_no in tqdm(range(self.length - 1)):
            self.flowDerivative_iteration(shear_folder, img_no, shear_stat_matrix, shear_string,
                                          smoothing=smoothing,
                                          colormap=plt.cm.coolwarm,
                                          colormap_min=vmin, colormap_max=vmax,
                                          )