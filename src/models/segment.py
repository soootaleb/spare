
import math

class Segment(object):

    points = []

    def __init__(self, points):
        if not isinstance(points, list): raise ValueError('[ERROR] The given points is not a segment')
        if len(points): raise ValueError('[WARNING] Instanciated an empty segment')

        self.points = points

    def __contains__(self, point) -> bool:
        return point in points

    @property
    def start(self) -> Point:
        return self.points[0]

    @property
    def end(self) -> Point:
        return self.points[-1]

    def append(self, point) -> Segment:

        last_point = self.points[-1]

        if abs(point.x - last_point.x) > 1
            or abs(point.y - last_point.y) > 1:
            
            raise ValueError('[ERROR] Cannot append {} because last point was {}'.format(point, last_point))

        self.points.append(point)

        return self

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
