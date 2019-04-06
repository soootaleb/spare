
from models.point import Point
from models.image import Image
from models.histogram import Histogram
from math import cos, sqrt, exp
import numpy as np
class Descriptor(object):

    relative = None
    reference = None

    variance = None

    description = None

    scanning = None
    histogram = None

    estimated_bias = None
    annulative = None

    relations = []

    def __init__(self, reference: Image, relative: Image, cardinal = 16, variance = 30):

        self.relative = relative
        self.reference = reference
        self.variance = variance

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
    def set_variance(self, variance):
        self.variance = variance
        return self

    def compute_histogram(self):

        for (direction, parallels) in self.scanning.items():
            test = self.compute_direction(parallels)
            self.histogram[direction] = test
        self.histogram.normalize()
        self.estimated_bias = self.histogram.substract_minimum(self.annulative)
        return self
        
    def compute_direction(self, parallels) -> float:
        '''
            This method is responsible for computing a value of description depending on
            a particular direction, which is represented by the scanning parallels

            The method must accept those scanning parallels and retur a float which
            describes "how much" the relative image is positioned in this direction
        '''
        raise NotImplementedError('You must override the Descriptor::compute_direction function')
    
    def gaussian_density_comparison(self,angles, angle_to_compare, normalisation = True):
        '''
            Gaussian density function tweaked up with our parameters
        '''
        variance = self.variance
        # divided by two and reversed to act like a modulo
        if angle_to_compare == 0:
            density = [(exp(- ( (( (int(angle)- angle_to_compare) / variance)**2) /2) ) / (variance * sqrt(2 * np.pi)) * variance) /2 for angle in angles]
            density = np.add(density, np.flip(density))
        else :
            density = [(exp(- ( (( (int(angle)- angle_to_compare) / variance)**2) /2) ) / (variance * sqrt(2 * np.pi)) * variance) for angle in angles]
        if normalisation : 
            maximum = max(density)
            density = [value / maximum for value in density]
        return density


    def describe(self):
        '''
            Returns the final maps of [relation, proportion]
            Actually, not yet a proportion
        '''
        if len(self.relations) == 0:
            raise Warning('You did not aspecify any relation so describing won\'t give any result')
        values = { label: self.mask(int(direction)) for (direction,label) in self.relations.items() }
        self.description = values
        return values

    def mask(self, direction):
        '''
        Use a gaussian like density function to compare with the computed score
        and get a match score between the description and the direction
        '''
        gaussian_at_angles = self.gaussian_density_comparison(self.histogram.directions, int(direction))
        gaussian_at_angles = [round(val,9) for val in gaussian_at_angles]
        values =  list(self.histogram.values.values())
        #we take the minimums of the calculated values and the associated values expected in the gaussian
        minimums = [ min(gaussian, histogram_value) for gaussian, histogram_value in zip(gaussian_at_angles, values) ]

        #We select the maximum
        maximum = max(minimums)

        #normalisation
        maximum = maximum / max(gaussian_at_angles)

        return maximum # Percentage of match between the mask and the description in the given direction

    def interpret(self):
        '''
            textual interpretation of the description given by the describe function
        '''
        #Actually should be a function used on ALL the descriptors using all the description.
        raise NotImplementedError('You must override the Descriptor::interpret function')
