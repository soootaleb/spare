
from models.point import Point

import math, random, numpy as np

class Segment(list):
    '''
    The Segment class extends the python list in order
    to add applicatio specific functions.

    Note that segments are lists of points with restrictions
    - Added points must be following the last one
    - The segment has a sens (a beginning and an end)

    /!\ The X and Y axis are inverted (X is vertical and Y horizontal)
    '''

    color = None

    def __init__(self, points):
        '''
        The given points are passed to the list constructor.
        TODO: Verify that the points defined a segment (continuous and straight)
        '''
        if len(points) == 0: raise ValueError('[WARNING] Instanciated an empty segment')
        self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        super().__init__(points)

    @property
    def start(self) -> Point:
        '''
        The first point of the segment
        '''
        return self[0]

    @property
    def end(self) -> Point:
        '''
        The last point of the segment
        '''
        return self[-1]
        
    def __getitem__(self, key) -> Point:
        if isinstance(key, int):
            return super().__getitem__(key)
        elif isinstance(key, Point):
            return self[key.x, key.y]
        else:
            try:
                return [o for o in self if o.x == key[0] and o.y == key[1]][0]
            except Exception:
                return None
        

    def append(self, point):
        if point in self:
            raise ValueError('[ERROR] Segment already contains {}'.format(point))    
        elif len(self) > 0:
            if abs(point.x - self.end.x) > 1 or abs(point.y - self.end.y) > 1:
                raise ValueError('[ERROR] Cannot append {} because last point was {}'.format(point, self.end))
            else:
                super().append(point)


    @property
    def vertical(self) -> bool:
        return self.start.y == self.end.y

    @property
    def horizontal(self) -> bool:
        return self.start.x == self.end.x

    def angle(self, radians = False):
        '''
        Returns the direction of the segment.
        By default, the angle is expressed as degrees
        but specifying radians=True will return the result as radians.
        '''
        if self.vertical:
            angle = np.pi / 2
        elif self.horizontal:
            angle = 0
        else:
            BC = abs(self.start.x - self.end.x)
            AC = abs(self.start.y - self.end.y)
            angle = math.atan(BC / AC)

        return angle if radians else np.degrees(angle)