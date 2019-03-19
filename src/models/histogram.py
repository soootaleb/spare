from models.image import Image
from numpy import linspace

class Histogram(object):
    '''
        Represents a single histogram as a data structure.
        The data is stored in the "values" property which is like

        {
            "0": 12,
            "90": 24,
            "180": 0,
            ...
        }

        It's a python dictionary for which
            - the keys are the angle, computed depending on the cardinal with range(0, 360, 360 / self.cardinal)
            - the values are the computed value to display on the histogram, computed by the given relation
        
    '''

    cardinal = 16

    image_a = None
    image_b = None

    relation = None

    values = dict()

    def __getitem__(self, direction: int):
        return self.values[str(direction)]

    def __setitem__(self, direction: int, value: float):
        self.values[str(direction)] = value
        return self

    def __init__(self, image_a: Image, image_b: Image):
        if not isinstance(image_a, Image) \
            or not isinstance(image_b, Image):
            
            raise ValueError('Histogram works with two objects of type Image')

        self.image_a = image_a
        self.image_b = image_b

    def set_cardinal(self, cardinal: int):
        self.values = dict()
        self.cardinal = cardinal
        return self

    def normalize(self):
        score_max = max(self.values.values())
        self.values = { direction: val / score_max for (direction, val) in self.values.items() }
        return self

    @property
    def directions(self):
        return linspace(0, 360, self.cardinal, dtype=int)
