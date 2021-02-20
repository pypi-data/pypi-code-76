import cv2
import numpy as np


# Between 0 and 1. closer to 0 will make more precise matches.
match_coefficient = 0.01

# Sift and Flann
sift = cv2.SIFT_create()
index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)


def getMatchPercentage(image1, image2, isDebug=False):
    if image1 is None or image2 is None:
        return 0
    # 1. Check if images are equal
    if image1.shape == image2.shape:
        difference = cv2.subtract(image1, image2)
        b, g, r = cv2.split(difference)
        # print(difference)
        if (
            cv2.countNonZero(b) == 0
            and cv2.countNonZero(g) == 0
            and cv2.countNonZero(r) == 0
        ):
            if isDebug:
                print("Similarity: 100% (equal size and channels)")
            return 100

    # 2. Check for similarities
    # kp_ -> stands for KEY POINT in the image
    # desc_ -> stands for DESCRIPTOR. Each descriptor describes a key point
    kp_1, desc_1 = sift.detectAndCompute(image1, None)
    kp_2, desc_2 = sift.detectAndCompute(image2, None)

    matches = flann.knnMatch(desc_1, desc_2, k=2)
    good_points = []
    for m, n in matches:
        if m.distance < match_coefficient * n.distance:
            good_points.append(m)

    number_keypoints = 0
    if len(kp_1) >= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    percentage_similarity = len(good_points) / number_keypoints * 100

    if isDebug:
        print("Similarity: " + str(int(percentage_similarity)))

        # result = cv2.drawMatchesKnn(image1,kp_1,  image2, kp_2, matches,None)
        result = cv2.drawMatches(image1, kp_1, image2, kp_2, good_points, None)

        cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return percentage_similarity
