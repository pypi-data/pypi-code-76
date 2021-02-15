from scipy.spatial import distance
import numpy as np
import cv2
from functools import partial


class Region(object):

    def __init__(self, contour, mask, original):
        '''using rotated axis convention (i.e. height is X)'''
        
        self.mask = mask
        self.contour = contour
        self.original = original
        self.segmentation = mask * original
        
        self.total_height, self.total_width = mask.shape
        self.total_size = mask.size

        # Calculate moments
        self.moments = cv2.moments(contour)
        self.hu_invariants = cv2.HuMoments(self.moments).flatten()
        
        # Calculate centroid
        center_y = int(self.moments['m10'] / self.moments['m00'])
        center_x = int(self.moments['m01'] / self.moments['m00'])
        self.centroid = (center_y, center_x)

        # Get area
        self.area = mask[mask == 1].size

        # Get minimum bounding rect
        self.rect = cv2.minAreaRect(self.contour)
        self.rect_corners = [np.int0(cv2.boxPoints(self.rect))]

        # Vector representation
        self.v_repr = np.hstack([self.hu_invariants,
                                 center_y/self.total_width,
                                 center_x/self.total_height,
                                 self.area/self.total_size])

    def distance_from_region(self, region):
        assert isinstance(region, Region)
        return distance.euclidean(self.centroid, region.centroid)

    def farthest_point_from_centroid(self):
        max_distance = 0
        max_point = None
        for point in self.contour:
            point = point[0]
            new_distance = distance.euclidean(self.centroid,
                                              point)
            if max_distance <= new_distance:
                max_distance = new_distance
                max_point = point
        return max_point, max_distance

    def merge(self, region):
        new_mask = region.mask + self.mask
        new_segmentation = region.segmentation + self.segmentation
        image_from_mask = new_mask.astype("uint8") * 255
        new_contour = self.merge_contours([region.contour, self.contour])
        return Region(new_contour, new_mask, new_segmentation)

    def merge_contours(self, contours):
        all_points = []
        for contour in contours:
            all_points += [p[0] for p in contour]
        new_contour = np.array(all_points).reshape((-1,1,2)).astype(np.int32)
        new_contour = cv2.convexHull(new_contour)
        return new_contour

    def approx_poly(self, threshold):
        assert 0 <= threshold <= 1
        epsilon = threshold * cv2.arcLength(self.contour, True)
        poly = cv2.approxPolyDP(self.contour, epsilon, True)
        return poly

    def save_uncropped(self, output_path):
        if not output_path.endswith(".png"):
            output_path += "_.png"
        # TODO: Crop image
        cv2.imwrite(output_path, self.segmentation)

    def save_cropped(self, output_path):
        if not output_path.endswith(".png"):
            output_path += "_.png"
        # Rotate
        center, size, angle = self.rect
        center = (int(center[0]), int(center[1])) 
        size = (int(size[0]), int(size[1]))
        height, width = self.segmentation.shape
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        # TODO: Freeing memory (idk if necessary)
        rotated_segmentation = cv2.warpAffine(self.segmentation, 
                                              rotation_matrix, 
                                              (width, height))
        # Crop
        cropped = cv2.getRectSubPix(rotated_segmentation, size, center)
        # Convert zero values to alpha channel
        bgr_img = cv2.cvtColor(cropped, cv2.COLOR_GRAY2BGR)
        b, g, r = cv2.split(bgr_img)
        alpha_channel = (cropped != 0).astype("uint8") * 255
        bgra_img = cv2.merge([b, g, r, alpha_channel])
        cv2.imwrite(output_path, bgra_img)

    def __eq__(self, r2):
        assert isinstance(r2, Region)
        return self.area == r2.area

    def __gt__(self, r2):
        assert isinstance(r2, Region)
        return self.area > r2.area
    
    def __lt__(self, r2):
        assert isinstance(r2, Region)
        return self.area < r2.area

    def __len__(self):
        return self.area

    def __str__(self):
        return "Region {0} with area {1}".format(self.centroid, self.area)

    def __repr__(self):
        return str(self)
