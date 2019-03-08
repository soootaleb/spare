from models.point import Point
from models.segment import Segment

from functions import *

from math import sin, cos, tan, pi, sqrt

'''
    Represents an image in our application. It's created with an OpenCV::imread image
    but it adds project oriented features

    Overloaded operators:
    - point in image

'''
class Image(object):

    base = None # We keep the original one to be able to reset
    image = None # Underlying OpenCV image that we can manipulate

    def __init__(self, cv_image):
        self.base = cv_image
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

    def __contains__(self, point) -> bool:
        '''
        We consider the points to be zero indexed
        '''
        return point.x < self.width and point.y < self.height

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
        
        x2 = round(math.sqrt(2) * max_lenght * math.cos(direction))
        y2 = round(math.sqrt(2) * max_lenght * math.sin(direction))
        
        #At this moment, 4 possibilities

        #TODO : Generate from angle 0 that goes left to right.
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
        return self.base[point.x, point.y] if self.__contains__(point) else -1

    def parallels(self, angle):
        """
        This function get all the parrallels parallels in an image from a single segment
        the parallels returned 
        """

        ray = self.ray(angle)

        max_length = self.max_dimension

        angle = 1 if ray.vertical else abs(ray.slope)

        parallels = []
        
        # Adding all the parallels below the first segment
        for actual_segment in range(1, max_length):
            parallels.append(Segment([]))
            parallels.append(Segment([]))
            for actual_point in range(max_length):
                if angle >= 1:
                    if x_exist(ray, actual_point, actual_segment): 
                        parallels[-1].append(Point(ray[actual_point][0] - actual_segment, ray[actual_point][1]))
                    if x_in_bound(ray, actual_point, actual_segment, max_length):
                        parallels[-2].append(Point(ray[actual_point][0]+actual_segment, ray[actual_point][1]))
                else:
                    if y_exist(ray, actual_point, actual_segment):
                        parallels[-1].append(Point(ray[actual_point][0],ray[actual_point][1]-actual_segment))   
                    if y_in_bound(ray, actual_point, actual_segment, max_length):
                        parallels[-2].append(Point(ray[actual_point][0], ray[actual_point][1]+actual_segment))

        parallels.append(ray)

        return parallels

    def draw(self, segment):
        for point in segment: # To check if pixel exists
            self.image[point.x, point.y] = [
                max(0, segment.color[0] - 2),
                max(0, segment.color[1] - 2),
                max(0, segment.color[2] - 2)
            ]
