from models.point import Point
from models.segment import Segment

from functions import bresenham

from math import sin, cos, tan, pi, sqrt

'''
    Represents an image in our application. It's created with an OpenCV::imread image
    but it adds project oriented features

    Overloaded operators:
    - point in image

'''
class Image(object):

    width = None
    height = None

    base = None # We keep the original one to be able to reset
    image = None # Underlying OpenCV image that we can manipulate

    def __init__(self, cv_image):
        if not bool(cv_image): print('[WARNING] Instanciated an empty image')

        self.base = cv_image
        self.image = self.base.copy()
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]

    def reset(self):
        '''
        Resets the OpenCV image to its original version (as passed in the constructor)
        '''
        self.image = self.base.copy()

    def __contains__(self, point) -> bool:
        '''
        We consider the points to be zero indexed
        '''
        return point.x < self.width - 1
            and point.y < self.height - 1

    def ray(self, angle):
        """
        Determinate starting point and destination point depending of the angle given as parameter
        starting point is always a corner of the image.

        The starting point is a corner of the image, depending on the provided angle.

        TODO: Automate the destination point depending on the image shape (remove max_length)
        TODO: Add the possibility to start from a specific position
        """
        direction = degres * pi / 180

        max_lenght = sqrt(self.width ** 2 + self.height ** 2)
        
        x2 = round(max_lenght * cos(direction))
        y2 = round(max_lenght * sin(direction))
        
        #At this moment, 4 possibilities
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

        return bresenham(x1, y1, x2, y2)

    def parallels(self, angle) -> Segment[]:
        """
        This function get all the parrallels parallels in an image from a single segment
        the parallels returned 
        """

        ray = self.ray(angle)

        max_length = sqrt(self.width ** 2 + self.height ** 2)

        angle = ray.vertical ? 1 : abs(self.slope)

        parallels = []
        
        # Adding all the parallels below the first segment
        for actual_segment in range(1, max_length):
            parallels.append([])
            parallels.append([])
            for actual_point in range(max_length):
                if angle >= 1:
                    if x_exist(ray, actual_point, actual_segment): 
                        parallels[-1].append([ray[actual_point][0] - actual_segment, ray[actual_point][1]])
                    if x_in_bound(ray, actual_point, actual_segment, max_length):
                        parallels[-2].append([ray[actual_point][0]+actual_segment, ray[actual_point][1]])
                else:
                    if y_exist(ray, actual_point, actual_segment):
                        parallels[-1].append([ray[actual_point][0],ray[actual_point][1]-actual_segment])   
                    if y_in_bound(ray, actual_point, actual_segment, max_length):
                        parallels[-2].append([ray[actual_point][0], ray[actual_point][1]+actual_segment])

        parallels.append(segment)

        return parallels