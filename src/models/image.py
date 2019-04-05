from models.point import Point
from models.segment import Segment

from functions import *

from math import sin, cos, tan, pi, sqrt

import os, cv2 as cv, numpy as np

'''
    Represents an image in our application. It's created with an OpenCV::imread image
    but it adds project oriented features
'''
class Image(object):

    IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'misc')

    fname = None

    base = None # We keep the original one to be able to reset
    image = None # Underlying OpenCV image that we can manipulate

    color = None

    _parallels = dict()

    def __init__(self, fname, color = False):

        if isinstance(fname, str):
            self.fname = fname
            if color :
                self.base = cv.imread(os.path.join(self.IMAGES_DIR, fname), cv.IMREAD_COLOR)  
                self.color = True              
            else :
                self.base = cv.imread(os.path.join(self.IMAGES_DIR, fname), cv.IMREAD_GRAYSCALE) #cv.COLOR_RGB2GRAY)
                self.base[self.base > 0] = 1 # Passing white value as ones for easy computing
                self.color = False
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

    @property
    def center(self) -> Point:
        return Point(round(self.width / 2), round(self.height / 2))

    def reset(self):
        '''
            Resets the OpenCV image to its original version (as passed in the constructor)
            /!\ Every change is reset so the use of Image::resize or Image::rotate
        '''
        self.image = self.base.copy()
        self._parallels = dict()

        return self

    def __contains__(self, point) -> bool:
        '''
            Verifies that the given point has positive coordinates
            and stays in the dimensions of the image.

            We consider the points to be zero indexed
        '''
        return point.x < self.width and point.y < self.height

    def resize(self, factor):
        '''
            Uses OpenCV::resize to resize the image by the given factor
        '''
        self.image = cv.resize(self.image, (round(factor * self.width), round(factor * self.height)))
        return self

    def rotate(self, angle):
        '''
            Uses OpenCV::getRotationMatrix2D to create a rotation and apply it to the
            underlying instance image
        '''
        mat = cv.getRotationMatrix2D((self.center.x, self.center.y), angle, 1.0)
        self.image = cv.warpAffine(self.image, mat, self.image.shape[1::-1], flags=cv.INTER_LINEAR)

        return self

    def translate_horizontal(self, dir_x):
        """
        function that recalculate the new position of the image depending of its precedent position
        """
        x_del = dir_x
        if dir_x >= 0:
            angle = 0
            x_incr = 1
        else :
            angle = 180
            x_incr = -1
        segments = parallels(angle)
        for segment in segments :
            seen = False
            for point in segment:
                if not seen and self.image[point] != 0:
                    seen = True
                    self.image[point] = 0
                    x_del -= x_incr
                if seen and self.image[point] !=0 and x_del != 0:
                    self.image[point] = 0
                    x_del -= x_incr
                if seen and self.image[point] == 0 and dir_x != 0:
                    dir_x -= x_incr
                    self.image[point] = 255


    def merge(self, image):
        '''
            Uses OpenCV::add to merge the given image to the original instance.

            Returns a new instance of Image, and the original images are not affected
        '''

        result = cv.merge( [self.image, image.image, np.zeros( (self.width, self.height, 1), dtype = "uint8") ] )
        return Image( result, color = True)

    def ray(self, angle):
        """
        Determinate starting point and destination point depending of the angle given as parameter
        starting point is always a corner of the image.

        The starting point is a corner of the image, depending on the provided angle.

        TODO: Automate the destination point depending on the image shape (remove max_length)
        TODO: Add the possibility to start from a specific position
        """

        #radians
        direction = np.radians(angle)

        #should be deleted and use pythagore to be able to use rectangular images
        max_lenght = self.max_dimension
        
        #should be calculated using pythagore theorem so rectangles can be used.
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

    def __getitem__(self, key):
        '''
            I removed the verification of "point in self" to gain around 10% performances.
            I consider the point to be in the image since the produced data structures
            for rays and parallels are existing points in our images
        '''
        if isinstance(key, Point):
            return self[key.x, key.y]
        else:
            return self.image[key[0], key[1]]

    def parallels(self, angle):

        """
        This function get all the parrallels  in an image from a single segment
        The original segment
        """

        if str(angle) not in self._parallels.keys():
            ray = self.ray(angle)
            max_length = self.max_dimension

            def map_offset_to_parallels(offset):
                def duplicate_points(point):
                    if offset == 0:
                        return point
                    else:
                        if ray.vertical and 0 <= point.y + offset < max_length:
                            return Point(point.x, point.y + offset)
                        elif ray.horizontal and 0 <= point.x + offset < max_length:
                            return Point(point.x + offset, point.y)
                        elif 0 < ray.angle() % 90 <= 45 and 0 <= point.x + offset < max_length:
                            return Point(point.x + offset, point.y)
                        elif 90 > ray.angle() % 90 > 45 and 0 <= point.y + offset < max_length:
                            return Point(point.x, point.y + offset)
                
                segment = [o for o in map(duplicate_points, ray) if o is not None]
                return Segment(segment) if len(segment) > 0 else None

            self._parallels[str(angle)] = [o for o in map(map_offset_to_parallels, range(-max_length, max_length)) if o is not None]

        return self._parallels[str(angle)]


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
            if color[0] == max(0, segment.color[0]) \
                and color[1] == max(0, segment.color[1]) \
                and color[2] == max(0, segment.color[2]):
                
                raise Exception('The {} is already colored in image {} !!!'.format(point, self.fname))

            self.image[point.x, point.y] = [
                max(0, segment.color[0]),
                max(0, segment.color[1]),
                max(0, segment.color[2])
            ]
