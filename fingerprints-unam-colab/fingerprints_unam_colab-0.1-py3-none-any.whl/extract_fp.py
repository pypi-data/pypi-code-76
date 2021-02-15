import os
import sys

from collections import OrderedDict

try:
    from regions import Region
except:
    from huellas.regions import Region

try:
    from auxiliar import *
except:
    from huellas.auxiliar import *

def main(input_img_path, output_folder_path):
   
    img = cv2.imread(input_img_path, 
                    cv2.IMREAD_GRAYSCALE)
    #mostrar_imagen(img, "Original")
    
    median = cv2.medianBlur(img, 13)
    #mostrar_imagen(median, "F. Mediana")

    umbral = cv2.adaptiveThreshold(median,
                                   255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY,
                                   11,
                                   2)
    #mostrar_imagen(umbral, "Umbral Local")
    not_umbral = 255 - umbral
    
    N8 = np.ones((3, 3))

    dilatacion = cv2.dilate(not_umbral, N8, iterations=10)
    #mostrar_imagen(dilatacion, "Dilatacion")
    
    erosion = cv2.erode(dilatacion, N8, iterations=5)
    #mostrar_imagen(erosion, "Erosion")

    qty, label_mask = cv2.connectedComponents(erosion)
    labels, counts = np.unique(label_mask, return_counts=True)
    label_counts = [*zip(labels, counts)]
    label_counts.sort(key=lambda x:x[1], reverse=True)

    # Segmentation
    regions = []
    for label, count in label_counts:
        if label == 0 :
            continue
        # TODO: Avoid arbitrary sizes (why 10000?)
        elif count < 10000:
            continue
        cut_mask = label_mask == label
        
        # Calculate contours
        contours, _  = cv2.findContours(cut_mask.astype("uint8"), 
                                        cv2.RETR_EXTERNAL, 
                                        cv2.CHAIN_APPROX_SIMPLE)
       
        # Don't process images with more than one contour
        if len(contours) > 0:
            # Fill entire region as marked by contour
            cut_mask = cut_mask.astype("float32") * 255
            cut_mask = cv2.fillPoly(cut_mask, contours, 255)
            cut_mask = cut_mask == 255
            # Process region
            r = Region(contours[0], cut_mask, img)
            regions.append(r)

            #cv2.circle(img, r.centroid, radius=1, color=(0,255,0), thickness=10)
            #cv2.drawContours(img, r.contour, -1, (0,255,75), 4)
            #cv2.drawContours(img, r.rect_corners, 0, (0,75,255), 2)

            #mostrar_imagen(img)
            # Get minimum bounding box
            # Save for classification
            #import ipdb;ipdb.set_trace()

        #guardar_imagen(segmentacion, "../outputs/%d.png" % label)
    
    #guardar_imagen(img, "../outputs/all_detections.png")
    
    # Classification starts
    regions.sort(reverse=True)
    
    # Two palms (may have incomplete fingers)
    hands = [regions.pop(0)]
    hands.append(regions.pop(0))

    # Fingerprints
    fprint_candidates = []
    partial_hand_candidates = []
    while len(regions) != 0:
        r = regions.pop(0)
        #cv2.circle(img, r.centroid, radius=1, color=(0,255,0), thickness=10)
        poly = r.approx_poly(0.1)
        #cv2.drawContours(img, [poly], 0, (0,75,255), 2)
        if len(poly) == 4:
            # TODO: Needs an additional check (e.g. size ratio)
            fprint_candidates.append(r)
        else:
            partial_hand_candidates.append(r)

    # Check if remaining regions are part of the hands
    for r in partial_hand_candidates:
        _, h1_max_dist = hands[0].farthest_point_from_centroid()
        _, h2_max_dist = hands[1].farthest_point_from_centroid()
   
        selected_hand = None
        candidate_h1_distance = hands[0].distance_from_region(r)
        candidate_h2_distance = hands[1].distance_from_region(r)
        if candidate_h1_distance < candidate_h2_distance:
            if candidate_h1_distance <= h1_max_dist:
                # we are in merging region
                hands[0] = hands[0].merge(r)
        elif candidate_h2_distance < candidate_h1_distance:
            if candidate_h2_distance <= h2_max_dist:
                # we are in merging region
                hands[1] = hands[1].merge(r)
    
    for i in range(len(fprint_candidates)):
        fprint_candidates[i].save_cropped(output_folder_path + "fprint%d.png" % i)
    
    for i in range(len(hands)):
        hands[i].save_cropped(output_folder_path + "hand%d.png" % i)

        #cv2.circle(img, hand.centroid, radius=1, color=(0,255,0), thickness=10)
        #cv2.drawContours(img, hand.contour, -1, (0,255,75), 4)
        #cv2.drawContours(img, hand.rect_corners, 0, (0,75,255), 2)
        #mostrar_imagen(img, "hand")
    
    #guardar_imagen(img, "../outputs/detected_hands.png")

    # Clustering the remaining regions
    # v_repr = np.array([r.v_repr for r in regions])

    #mask = (erosion == 255)
    #segmentacion = mask * img
    #mostrar_imagen(segmentacion, "Erosion")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Usage: %s INPUT_IMG OUTPUT_FOLDER" % sys.argv[0])

    input_img_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    if not os.path.exists(input_img_path):
        raise ValueError("%s doesn't exist" % input_img_path)
    if os.path.exists(output_folder_path):
        if not os.path.isdir(output_folder_path):
            raise ValueError("%s is not a folder" % output_folder_path)
    if not output_folder_path.endswith(os.sep):
        output_folder_path += os.sep
    image_name = os.path.basename(input_img_path).split(".")[0]
    output_folder_path += image_name + os.sep
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    main(input_img_path, output_folder_path)
