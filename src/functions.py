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

DEBUG = False

def bresenham(x, y, x_dst, y_dst):
    """
    creation of a segment using bresenham algorithm
    x, y source point
    x_dst, y_dst destination point
    """
    segment = [] #contains all pixels in the segment
 
    #metematical simplifications
    error_x = abs(x_dst - x)
    error_y = abs(y_dst - y)

    delta_x = 2 * error_x
    delta_y = 2 * error_y

    #for the case we go backward in the direction
    if x <= x_dst:
        x_inc = 1
    else:
        x_inc = -1
    if y <= y_dst:
        y_inc = 1
    else:
        y_inc = -1
    
    index = 0

    if delta_x > delta_y:

        while index <= delta_x:
            segment.append([x, y])
            x += x_inc
            index+=2 #because delta = 2 * error
            error_x -= delta_y
            if error_x < 0:
                y += y_inc
                error_x += delta_x

    else : 
        while index <= delta_y:
            segment.append([x, y])
            index+=2 #because delta = 2 * error
            y += y_inc
            error_y -= delta_x
            if error_y < 0:
                x += x_inc
                error_y += delta_y

    return segment

#
# Applies the BRESENHAM algorithm from a starting point
# to a direction set by an angle (in degres)
# @param {*} x1 X position of the starting point
# @param {*} y1 Y position of the starting point
# @param {*} angle The direction of the ray
#
def bresenham_angle(degres, max_lenght):
    """
    Determinate starting point and destination point depending of the angle given as parameter
    starting point is always a corner of the image.
    """
    angle = degres * math.pi / 180
    
    x2 = round(math.sqrt(2) * max_lenght * math.cos(angle))
    y2 = round(math.sqrt(2) * max_lenght * math.sin(angle))
    #At this moment, 4 possibilities
    if x2 >= 0 and y2 >= 0:
        #starting top left
        x1 = 0
        y1 = 0
        x2 = min(max_lenght-1, x2)
        y2 = min(max_lenght-1, y2)
    elif x2 < 0 and y2 < 0:
        #starting bottom right
        x1 = min(max_lenght-1, -x2)
        y1 = min(max_lenght-1, -y2)
        x2 = 0
        y2 = 0
    elif x2 >= 0 and y2 < 0:
        #starting top right
        x1 = 0
        y1 = min(max_lenght-1, -y2)
        y2 = 0
        x2 = min(max_lenght-1, x2)
    else :
        #starting bottom left
        x1 = min(max_lenght-1, -x2)
        x2  = 0
        y1 = 0
        y2 = min(max_lenght-1, y2)
    return bresenham(x1, y1, x2, y2)


def scan_parrallel(segment, max_size):
    """
    This function get all the parrallels segments in an image from a single segment
    the segments returned 
    """
    x_src = segment[0][0]
    y_src = segment[0][1]
    x_dst = segment[-1][0]
    y_dst = segment[-1][1]

    if x_src - x_dst != 0:
        angle = abs((y_src - y_dst) / (x_src - x_dst))
    else:
        angle = 1

    segments = []
    # Adding all the segments below the first segment
    for actual_segment in range(1, max_size):
        segments.append([])
        for actual_point in range(max_size):
            if angle >= 1:
                if segment[actual_point][0]-actual_segment >= 0: # Check pixel exists
                    segments[-1].append([segment[actual_point][0] - actual_segment, segment[actual_point][1]])
            elif segment[actual_point][1]-actual_segment >= 0: # Check pixel exists
                    segments[-1].append([segment[actual_point][0],segment[actual_point][1]-actual_segment])

    segments.append(segment)

    # Adding all the segments above the first segment
    for actual_segment in range(1, max_size):
        segments.append([])
        for actual_point in range(max_size):
            if angle >= 1:
                if segment[actual_point][0]+actual_segment < max_size: # Check pixel exists
                    segments[-1].append([segment[actual_point][0]+actual_segment, segment[actual_point][1]])
            elif segment[actual_point][1]+actual_segment < max_size: # Check pixel exists
                    segments[-1].append([segment[actual_point][0], segment[actual_point][1]+actual_segment])

    return segments

def histogram(cardinal=16):
    """
    We want this function to produce a data structure representing a histogram
    of [what does it represent ?] depeding on the number of directions passed in arguments.
    """
    raise NotImplementedError('The histogram function is not implemented yet')

def print_segment(segment, max_size):
    print(segment, "\n")
    result = np.zeros((max_size, max_size))
