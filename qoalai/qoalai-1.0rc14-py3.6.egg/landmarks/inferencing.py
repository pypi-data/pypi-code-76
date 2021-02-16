import cv2 
import numpy as np 

GRID = 19


def nms_phone(map, position, grid_size=1/GRID):
    """Methode for landmark NMS
    
    Arguments:
        map {numpy} -- the output map
        position {numpy} -- the output position 
    
    Keyword Arguments:
        grid_size {[type]} -- [description] (default: {1/GRID})
    
    Returns:
        [type] -- [description]
    """
    img = (map * 255).astype(np.uint8)
    ret, labels = cv2.connectedComponents(img)
    
    # ----------------------------- #
    # labelling the result          #
    # ----------------------------- #
    label_dict = {}
    for i in range(GRID):
        for j in range(GRID):
            tmp = labels[i, j]
            
            if tmp != 0:
                if tmp not in list(label_dict.keys()):
                    label_dict[tmp] = []

                label_dict[tmp].append([map[i, j], i, j])
    
    # ----------------------------- #
    # find the max value for each lbl
    # ignore the non maxima         #
    # ----------------------------- #
    max_val = {}
    for i in label_dict:
        if i not in max_val:
            max_val[i] = []
        
        biggest_val = 0
        for j in label_dict[i]:
            if biggest_val < j[0]:
                biggest_val = j[0]
                max_val[i] = j
    
    # ----------------------------- #
    # for each maximum point        #
    # find the x and y point        #
    # ----------------------------- #
    result = {}
    for i in max_val:
        ctr_x = (max_val[i][2] + position[max_val[i][1], max_val[i][2], 0]) * grid_size
        ctr_y = (max_val[i][1] + position[max_val[i][1], max_val[i][2], 1]) * grid_size

        ctr_x = max(ctr_x, 0)
        ctr_y = max(ctr_y, 0)
        ctr_x = min(ctr_x, 300)
        ctr_y = min(ctr_y, 300)
        result[i] = (max_val[i][0], ctr_x, ctr_y)
    
    # ----------------------------- #
    # if the number of points > 4   #
    # remove the         #
    # ----------------------------- #
    while(True):
        if len(result.keys()) > 4:
            worst = 1.
            worst_point = None
            for i in result:
                if worst > result[i][0]:
                    worst = result[i][0]
                    worst_point = i
                    
            del result[worst_point]
            
        else:
            break  
    
    # ----------------------------- #
    # sorting the point             #
    # ----------------------------- #
    sorted_result = {}
    
    if len(result.keys()) == 4:
        # ----------------------------- #
        # sorting the point             #
        # ----------------------------- #
        for i in result: 
            ctr_x = result[i][1]
            ctr_y = result[i][2]
            
            gradiens_x = []
            gradiens_y = []
            for j in result: 
                if j != i :
                    ctr_x_new = result[j][1]
                    ctr_y_new = result[j][2] 
                    gradien_y = (ctr_y_new - ctr_y)
                    gradien_x = (ctr_x_new - ctr_x)
                    gradiens_x.append(gradien_x)
                    gradiens_y.append(gradien_y)
            
            gradien_x = np.mean(np.array(gradiens_x))
            gradien_y = np.mean(np.array(gradiens_y))
            
            # ----------------------------- #
            # the top letf point            #
            # ----------------------------- #
            if gradien_x >= 0 and gradien_y >=0: 
                if 1 not in sorted_result: 
                    sorted_result[1] = (result[i][0], ctr_x, ctr_y, gradien_x)
                else: 
                    if gradien_x > sorted_result[1][3]: 
                        sorted_result[2] = sorted_result[1]
                        sorted_result[1] = (result[i][0], ctr_x, ctr_y, gradien_x)
                    else: 
                        sorted_result[2] = (result[i][0], ctr_x, ctr_y, gradien_x)

            # ----------------------------- #
            # the top right point           #
            # ----------------------------- # 
            elif gradien_x < 0 and gradien_y >=0: 
                if 2 not in sorted_result: 
                    sorted_result[2] = (result[i][0], ctr_x, ctr_y, gradien_x)
                else:
                    if gradien_x > sorted_result[2][3]: 
                        sorted_result[1] = (result[i][0], ctr_x, ctr_y, gradien_x)
                    else: 
                        sorted_result[1] = sorted_result[2]
                        sorted_result[2] = (result[i][0], ctr_x, ctr_y, gradien_x)

            # ----------------------------- #
            # the bottom right point        #
            # ----------------------------- #    
            elif gradien_x <= 0 and gradien_y < 0: 
                if 4 not in sorted_result: 
                    sorted_result[4] = (result[i][0], ctr_x, ctr_y, gradien_x)
                else: 
                    if gradien_x > sorted_result[4][3]: 
                        sorted_result[3] = (result[i][0], ctr_x, ctr_y, gradien_x)
                    else:
                        sorted_result[3] = sorted_result[4]
                        sorted_result[4] = (result[i][0], ctr_x, ctr_y, gradien_x)

            # ----------------------------- #
            # the bottom left point         #
            # ----------------------------- #
            else:
                if 3 not in sorted_result: 
                    sorted_result[3] = (result[i][0], ctr_x, ctr_y, gradien_x)
                else: 
                    if gradien_x > sorted_result[3][3]: 
                        sorted_result[4] = sorted_result[3]
                        sorted_result[3] = (result[i][0], ctr_x, ctr_y, gradien_x) 
                    else: 
                        sorted_result[4] = (result[i][0], ctr_x, ctr_y, gradien_x) 
                    
    return sorted_result


def draw_res(img, point_dict):
    h, w, c = img.shape
    
    success_status = False
    # ----------------------------- #
    # if the detected point == 4    #
    # get the actual center point   #
    # do perspective transform      #
    # ----------------------------- # 
    if len(list(point_dict.keys())) == 4:

        rect = []
        for idx, i in enumerate(point_dict):
            #ctr_x = int(point_dict[idx+1][1] * w )
            
            if i == 1 or i == 3: 
                ctr_x = max(int(point_dict[idx+1][1] * w) -5, 0)
            else: 
                ctr_x = min(int(point_dict[idx+1][1] * w) +5, w)

            if i == 1 or i == 2: 
                ctr_y = max(int(point_dict[idx+1][2] * h) -5, 0)
            else: 
                ctr_y = min(int(point_dict[idx+1][2] * h) +5, h)

            rect.append([ctr_x, ctr_y])
        
        dst = np.array([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]], dtype = "float32")
        rect = np.array(rect, dtype='float32')
        M = cv2.getPerspectiveTransform(rect, dst)
        img = cv2.warpPerspective(img, M, (w, h))
        success_status = True

    bg = np.zeros((340, 340, 3))
    bg[20:-20, 20:-20, :] = img
    img = bg
    
    return img, success_status