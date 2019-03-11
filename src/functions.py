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

from models.point import Point
from models.segment import Segment

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
            segment.append(Point(x, y))
            x += x_inc
            index+=2 #because delta = 2 * error
            error_x -= delta_y
            if error_x < 0:
                y += y_inc
                error_x += delta_x

    else : 
        while index <= delta_y:
            segment.append(Point(x, y))
            index+=2 #because delta = 2 * error
            y += y_inc
            error_y -= delta_x
            if error_y < 0:
                x += x_inc
                error_y += delta_y

    return Segment(segment)


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

def x_exist(segment, point, shift):
    return segment[point][0] - shift >= 0

def y_exist(segment, point, shift):
    return segment[point][1] - shift >= 0

def x_in_bound(segment, point, shift, max_size):
    return segment[point][0] + shift < max_size

def y_in_bound(segment, point, shift, max_size):
    return segment[point][1] + shift < max_size