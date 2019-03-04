

class Point(object):

    x = None
    y = None

    def __init__(self, x, y):
        if x < 0: raise ValueError('Point::new - X must be positive instead of {}'.format(self.x))
        if y < 0: raise ValueError('Point::new - Y must be positive instead of {}'.format(self.y))
        
        self.x = x
        self.y = y

    def __str__(self):
        return str([self.x, self.y])