from models.point import Point
from models.segment import Segment

from functions import *

from math import sin, cos, tan, pi, sqrt

import os, cv2 as cv

'''
    Represents an image in our application. It's created with an OpenCV::imread image
    but it adds project oriented features
'''
class Image(object):

    IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'misc')

    fname = None

    base = None # We keep the original one to be able to reset
    image = None # Underlying OpenCV image that we can manipulate

    def __init__(self, fname):

        if isinstance(fname, str):
            self.fname = fname
            self.base = cv.imread(os.path.join(self.IMAGES_DIR, fname), cv.IMREAD_COLOR)
            self.image = self.base.copy()
        else:
            self.fname = 'IN_MEMORY_IMG'
            self.base = fname
            self.image = self.base.copy()

    @property
    def max_dimension(self):
        return max(self.width, self.height)

    @property
    def width(self):
        return self.image.shape[1]

    @property
    def height(self):
        return self.image.shape[0]

    def reset(self):
        '''
        Resets the OpenCV image to its original version (as passed in the constructor)
        '''
        self.image = self.base.copy()

        return self

    def __contains__(self, point) -> bool:
        '''
        We consider the points to be zero indexed
        '''
        return point.x < self.width and point.y < self.height

    def resize(self, factor):
        self.image = cv.resize(self.image, (round(factor * self.width), round(factor * self.height)))
        return self

    def merge(self, image):
        '''
            Uses OpenCV::add to merge the given image to the original instance.

            Returns a new instance of Image, and the original images are not affected
        '''
        return Image(cv.add(self.image, image.image))

    def ray(self, angle):
        """
        Determinate starting point and destination point depending of the angle given as parameter
        starting point is always a corner of the image.

        The starting point is a corner of the image, depending on the provided angle.

        TODO: Automate the destination point depending on the image shape (remove max_length)
        TODO: Add the possibility to start from a specific position
        """
        direction = angle * pi / 180

        max_lenght = self.max_dimension
        
        x2 = round(math.sqrt(2) * max_lenght * math.sin(direction))
        y2 = round(math.sqrt(2) * max_lenght * math.cos(direction))
        
        # At this moment, 4 possibilities
        if x2 >= 0 and y2 >= 0: # Starting top left
            x1 = 0
            y1 = 0
            x2 = min(max_lenght - 1, x2)
            y2 = min(max_lenght - 1, y2)
        elif x2 < 0 and y2 < 0: # Starting bottom right
            x1 = min(max_lenght - 1, -x2)
            y1 = min(max_lenght - 1, -y2)
            x2 = 0
            y2 = 0
        elif x2 >= 0 and y2 < 0: # Starting top right
            x1 = 0
            y1 = min(max_lenght - 1, -y2)
            y2 = 0
            x2 = min(max_lenght - 1, x2)
        else : # Starting bottom left
            x1 = min(max_lenght - 1, -x2)
            x2  = 0
            y1 = 0
            y2 = min(max_lenght - 1, y2)

        return Segment([point for point in bresenham(x1, y1, x2, y2) if point in self])

    def __getitem__(self, point):
        '''
            I removed the verification of "point in self" to gain around 10% performances.
            I consider the point to be in the image since the produced data structures
            for rays and parallels are existing points in our images
        '''
        return self.image[point.x, point.y]

    def parallels(self, angle):
        """
        This function get all the parrallels parallels in an image from a single segment
        the parallels returned
        """

        ray = self.ray(angle)

        max_length = self.max_dimension

        angle = 1 if ray.vertical else abs(ray.slope)

        def map_offset_to_parallels(offset):
            def duplicate_points(point):
                if angle >= 1 and 0 <= point.x + offset < max_length:
                    return Point(point.x + offset, point.y)
                elif angle < 1 and 0 <= point.y + offset < max_length:
                    return Point(point.x, point.y + offset)
            
            return Segment([o for o in map(duplicate_points, ray) if o is not None])

        return map(map_offset_to_parallels, range(-max_length, max_length))


    def draw(self, segment):
        '''
            Image::draw now raises and Exception if a point is already colored.
            It would mean there is a high probability the point has already been visited
            by one of our algorithms...
            
            Note that you could be very unfortunate and get an error without reason if
            - The image contains a certain color for a pixel
            - The segment has choosen a random color to be the same of the pixel (1 / 255*255*255 chance)
            - The segment contains the pixel with the same color...

            Juste restarting the algorithm should remove the exception.
        '''
        for point in segment:

            color = self.image[point.x, point.y]
            if color[0] == max(0, segment.color[0] - 2) \
                and color[1] == max(0, segment.color[1] - 2) \
                and color[2] == max(0, segment.color[2] - 2):
                
                raise Exception('The {} is already colored in image {} !!!'.format(point, self.fname))

            self.image[point.x, point.y] = [
                max(0, segment.color[0] - 2),
                max(0, segment.color[1] - 2),
                max(0, segment.color[2] - 2)
            ]
