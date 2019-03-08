
from models.point import Point
from models.point import Point

import math, random

class Segment(list):

    color = None

    def __init__(self, points):
        # if len(points) == 0: raise ValueError('[WARNING] Instanciated an empty segment')
        self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        super().__init__(points)

    @property
    def start(self) -> Point:
        return self[0]

    @property
    def end(self) -> Point:
        return self[-1]
        
    def __getitem__(self, key) -> Point:
        return super().__getitem__(key)

    def append(self, point):

        if len(self) > 0:
            last_point = self.end

            if abs(point.x - last_point.x) > 1 or abs(point.y - last_point.y) > 1:
                
                raise ValueError('[ERROR] Cannot append {} because last point was {}'.format(point, last_point))

        super().append(point)

    @property
    def vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def horizontal(self) -> bool:
        return self.start.y == self.end.y

    @property
    def slope(self) -> float:

        if self.vertical:
            return 1 # TODO: Fix this ugly value (a vertical slope is not 1 of coef but Infinity instead)
        else:

            delta_y = self.start.y - self.end.y
            delta_x = self.start.x - self.end.x
        
            return delta_y / delta_x
