"""
This module is a first & naive approach for the program structure.

Considering 

1 - The programm is small for now
2 - We don't have any idea of the program architecture

We prefer to use module level functions, easier to use & call.
We'll eventually refactor into potential classes later.
"""
import numpy as np
import sys

def get_segment(x1, y1, x2, y2, max_lenght = 10000):
    """
    Tracé de segment d'apres l'algorithme de bresenham
    (x1 y1) : le point de départ en haut a gauche, (x2 y2) point d'arrivé en bas a droite.
    retourne une liste contenant les double (x, y) de chacun des points.
    """

    segment = [] # Contient tout les pixels du segment.
 
    delta_x = x2 - x1
    delta_y = y2 - y1
    
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

    x = x1
    y = y1
   
    while x < max_lenght or y < max_lenght:
        
        if (err_x >= 0.5):
            x+=1
            err_x-=1
        if (err_y >= 0.5):
            y+=1
            err_y-=1

        if x < max_lenght and y < max_lenght:
            segment.append([x, y])
    
        err_x += err_x_inc
        err_y += err_y_inc
    return segment

def scan_parrallel(segment, height):
    """
    This function get all the parrallels segments in an image from a single segment
    the segments returned 
    """
    angle_cst = (segment[0][1] - segment[-1][1]) / (segment[0][0] - segment[-1][0])
    angle= angle_cst
    print(angle)
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


