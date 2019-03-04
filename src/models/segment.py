

class Segment(object):

    points = []

    def __init__(self, points):
        if not isinstance(points, list): raise ValueError('[ERROR] The given points is not a segment')
        if len(points): raise ValueError('[WARNING] Instanciated an empty segment')

        self.points = points

    def __contains__(self, point) -> bool:
        return point in points