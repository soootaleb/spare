

class Point(object):

    x = None
    y = None

    tuple = tuple()

    def __init__(self, x, y):
        if x < 0: raise ValueError('Point::new - X must be positive instead of {}'.format(x))
        if y < 0: raise ValueError('Point::new - Y must be positive instead of {}'.format(y))
        
        self.x = x
        self.y = y

        self.tuple = (x, y)

    def __str__(self):
        return str([self.x, self.y])

    def __repr__(self):
        return str([self.x, self.y])

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x \
            and self.y == other.y