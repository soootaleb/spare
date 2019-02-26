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

def get_segment(x1, y1, x2, y2):
    """
    Tracé de segment d'apres l'algorithme de bresenham
    (x1 y1) : le point de départ en haut a gauche, (x2 y2) point d'arrivé en bas a droite.
    retourne une liste contenant les double (x, y) de chacun des points.
    """

    segment = [] # Contient tout les pixels du segment.

    error = x2 - x1
    delta_x = error*2
    delta_y = (y2 - y1)*2

    while x1 < x2:
        segment.append([x1,y1])
        x1+=1
        error -= delta_y
        if error <= 0:
            y1 += 1
            error += delta_x
    return segment

def scan_parrallel(segment, height):
    """
    This function get all the parrallels segments in an image from a single segment
    """

    segments = []
    for actual_segment in range(height):
        segments.append([])
        for actual_point in range(height):
            if segment[actual_point][0]+actual_segment < height:
                segments[-1].append([segment[actual_point][0]+actual_segment, segment[actual_point][1]])
            else:
                break
    for actual_segment in range(1,height):
        segments.append([])
        for actual_point in range(height):
            if segment[actual_point][1]+actual_segment < height:
                segments[-1].append([segment[actual_point][0], segment[actual_point][1]+actual_segment])
            else: 
                break
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


