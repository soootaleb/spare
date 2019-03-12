
from models.point import Point
from models.image import Image
from models.histogram import Histogram

class Descriptor(object):

    relative = None
    reference = None

    scanning = None
    histogram = None

    relations = []

    def __init__(self, reference: Image, relative: Image, cardinal = 16):

        self.relative = relative
        self.reference = reference

        self.histogram = Histogram(reference, relative) \
            .set_cardinal(cardinal)

        self.scanning = {
            str(direction): self.reference.parallels(direction) \
                for direction in self.histogram.directions
        }

    def set_cardinal(self, cardinal):
        self.scanning = {
            str(direction): self.reference.parallels(direction) \
                for direction in self.histogram.set_cardinal(cardinal).directions
        }

        return self

    def compute_histogram(self):
        for (direction, parallels) in self.scanning.items():
            self.histogram[direction] = self.compute_direction(parallels)
        
        return self
        
    def compute_direction(self, parallels) -> float:
        '''
            This method is responsible for computing a value of description depending on
            a particular direction, which is represented by the scanning parallels

            The method must accept those scanning parallels and retur a float which
            describes "how much" the relative image is positioned in this direction
        '''
        raise NotImplementedError('You must override the Descriptor::compute_direction function')

    def describe(self):
        '''
            Returns the final maps of [relation, proportion]
        '''
        if len(self.relations) == 0:
            raise Warning('You did not aspecify any relation so describing won\'t give any result')
                
        return { label: self.mask(int(direction)) for (direction, label) in self.relations.items() }