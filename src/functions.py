"""
This module is a first & naive approach for the program structure.

Considering 

1 - The programm is small for now
2 - We don't have any idea of the program architecture

We prefer to use module level functions, easier to use & call.
We'll eventually refactor into potential classes later.
"""

def get_segment(x1, y1, x2, y2):
    """
    Tracé de segment d'apres l'algorithme de bresenham
    (x1 y1) : le point de départ en haut a gauche, (x2 y2) point d'arrivé en bas a droite.
    retourne une liste contenant les double (x, y) de chacun des points.
    """

    #raise NotImplementedError('This function is not tested yet')

    segment = [] # Contient tout les pixels du segment.

    delta_x = x2 - x1
    delta_y = y2 - y1
    y = y1 #rangée de départ
    error = 0.0
    if(delta_x != 0):
        err_x = delta_y / delta_x
    else:
        err_x = 0

    err_y = -1

    for x in range(x1, x2):
        segment.append([x, y])
        error += err_x
        if (error >= 0.5):
            y += 1
            error += err_y
    return segment

def scan_parrallel(segment, height):
    """
    This function get all the parrallels segments in an image from a segment
    """
    x0 = segment[0][0]
    y0 = segment[0][1]
    segments = []
    for actual_segment in range(height):
        segments.append([])
        for actual_point in range(height):
            if segment[actual_point][0]+actual_segment < height:
                segments[actual_segment].append([segment[actual_point][0]+actual_segment, segment[actual_point][1]])

    for actual_segment in range(1,height):
        segments.append([])
        for actual_point in range(height):
            if segment[actual_point][1]+actual_segment < height:
                segments[actual_segment].append([segment[actual_point][0], segment[actual_point][1]+actual_segment])
        #for actual in range(height-1,-1, -1):
    #raise NotImplementedError('The segments function is not implemented yet')
    print(segments)
    return segments

def test_all_segments(height):
    for x in range(height):
        seg_temp = get_segment(0, 0, x, height)
        print("\n actual segment : ",seg_temp)

        for y in range(height):
            seg_temp = get_segment(0, 0, height, y)
            print("\n",seg_temp)


def histogram(cardinal=16):
    """
    We want this function to produce a data structure representing a histogram
    of [what does it represent ?] depeding on the number of directions passed in arguments.
    """
    raise NotImplementedError('The histogram function is not implemented yet')


