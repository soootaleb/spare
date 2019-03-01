"""
This module is a first & naive approach for the program structure.

Considering 

1 - The programm is small for now
2 - We don't have any idea of the program architecture

We prefer to use module level functions, easier to use & call.
We'll eventually refactor into potential classes later.
"""
import numpy as np
import sys, math

def get_segment(x1, y1, x2, y2, max_lenght = 10000):
    """
    Tracé de segment d'apres l'algorithme de bresenham
    (x1 y1) : le point de départ en haut a gauche, (x2 y2) point d'arrivé en bas a droite.
    retourne une liste contenant les double (x, y) de chacun des points.
    """
    segment = [] # Contient tout les pixels du segment.
 
    delta_x = x2 - x1
    delta_y = y2 - y1
    
    if delta_x >= 0:
        x_sign = 1
    else:
        x_sign = -1

    if delta_y >= 0:
        y_sign = 1
    else:
        y_sign = -1

    if delta_x == 0:
        err_x_inc = 0
    else:
        err_x_inc = delta_y / delta_x
    
    if delta_y == 0:
        err_y_inc = 0
    else:
        err_y_inc = delta_x / delta_y
    
    err_x = 0.0
    err_y = 0.0
    iteration = 0
    x = x1
    y = y1
   
    iter_max = math.sqrt(2) * max_lenght
    
    while ( (x <= max_lenght and x >= 0) or (y >= 0 and y <= max_lenght)) and iteration < iter_max:
        
        if (abs(err_x) >= 0.5):
            x += x_sign
            err_x-= x_sign
            
        if (abs(err_y) >= 0.5):
            y += y_sign
            err_y-= y_sign

        if x < max_lenght and y < max_lenght:
            segment.append([x, y])
    
        err_x += err_x_inc
        err_y += err_y_inc
        iteration+=1
    return segment

def scan_parrallel(segment, height):
    """
    This function get all the parrallels segments in an image from a single segment
    the segments returned 
    """

    if segment[0][0] - segment[-1][0] != 0:
        angle_cst = (segment[0][1] - segment[-1][1]) / (segment[0][0] - segment[-1][0])
    else:
        angle_cst = height

    angle= angle_cst
    segments = []
    #adding all the segments below the first segment
    for actual_segment in range(1, height):
        segments.append([])
        for actual_point in range(height):
            if angle >= 1:
                if segment[actual_point][0]-actual_segment >= 0:
                    segments[-1].append([segment[actual_point][0] - actual_segment, segment[actual_point][1]])
            elif segment[actual_point][1]-actual_segment >= 0:
                    segments[-1].append([segment[actual_point][0],segment[actual_point][1]-actual_segment])

    segments.append(segment)

    #adding all the segments above the first segment
    for actual_segment in range(1, height):
        segments.append([])
        for actual_point in range(height):
            if angle >= 1:
                if segment[actual_point][0]+actual_segment < height:
                    segments[-1].append([segment[actual_point][0]+actual_segment, segment[actual_point][1]])
            elif segment[actual_point][1]+actual_segment < height:
                    segments[-1].append([segment[actual_point][0], segment[actual_point][1]+actual_segment])

    return segments

def histogram(cardinal=16):
    """
    We want this function to produce a data structure representing a histogram
    of [what does it represent ?] depeding on the number of directions passed in arguments.
    """
    raise NotImplementedError('The histogram function is not implemented yet')

def print_segment(segment, height):
    print(segment, "\n")
    result = np.zeros((height, height))
    for point in segment:
        result[point[0], point[1]] +=1
    print("segment [\n", result)
    return result

def test_segments(segments, height, affiche=False):
    result = np.zeros((height, height))
    for segment in segments:
        for point in segment:
            result[point[0], point[1]] +=1
    if affiche :
        print(result)
    return np.array_equal(np.ones((height, height)), result)



def test_all_segments(height):
    max_lenght = height-1
    total = 0
    fails = 0
    passed_all = True
    not_working = []
    for x in range(height):
        total+=2
        #from (0, 0)
        seg_tmp = get_segment(0, 0, x, max_lenght, height)
        if len(seg_tmp) > 1 :
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
        else :
            not_working.append([0, 0, x, max_lenght])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp

        seg_tmp = get_segment(0, 0, max_lenght, x, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
        else :
            not_working.append([0, 0, max_lenght, x, height])
            print("pas de segment pour", not_working[-1])
            print(seg_temp)
            fails+=1
            tmp = False
        passed_all = passed_all and tmp
    for x in range(height):
        total+=2
        #from (max, 0)
        seg_tmp = get_segment(max_lenght, 0, 0, x, height)
        if len(seg_tmp) >= 1 :
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
        else :
            not_working.append([max_lenght, 0, 0, x])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp

        seg_tmp = get_segment(max_lenght, 0, x, 0, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                fails+=1
        else :
            not_working.append([max_lenght, 0, x, 0])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp

    for x in range(height):
        total+=2
        #from (max, max)
        seg_tmp = get_segment(max_lenght, max_lenght, x, 0, height)
        if len(seg_tmp) >= height-1 :
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                fails+=1
        else :
            not_working.append([max_lenght, max_lenght, x, 0])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp


        seg_tmp = get_segment(max_lenght, max_lenght, 0, x, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                fails+=1
        else :
            not_working.append([max_lenght, max_lenght, 0, x])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp


    for x in range(height):
        total+=2
        #from (0, max)
        seg_tmp = get_segment(0, max_lenght, x, 0, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                not_working.append([0, max_lenght, x, 0])
                print("erreur avec le segment",not_working[-1])
                fails+=1
        else :
            not_working.append([0, max_lenght, x, 0])
            fails+=1
            print("pas de segment pour", not_working[-1])
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp


        seg_tmp = get_segment(0, max_lenght, max_lenght, x, height)
        if len(seg_tmp) > 1:
            tmp = test_segments(scan_parrallel(seg_tmp, height), height)
            if not tmp:
                not_working.append([0, max_lenght, max_lenght, x])
                print("erreur avec le segment",not_working[-1])
                fails+=1
        else :
            not_working.append([0, max_lenght, 0, x])
            print("pas de segment pour", not_working[-1])
            fails+=1
            print(seg_tmp)
            tmp = False
        passed_all = passed_all and tmp
    print("nombre total : ", total, ", nombre raté :", fails)
    return passed_all


def merge_images(img1, img2):
    """
    Merges two images into one, and affect colors to each image (instead of binary)
    for visualisation purpose
    """
    raise NotImplementedError('this function is not implemented')
    