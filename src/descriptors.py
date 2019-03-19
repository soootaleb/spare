from models.descriptor import Descriptor
from math import sin, cos, pi
from functools import reduce

class AngularPresenceDescriptor(Descriptor):

    relations = {
        #This order is for text generation, as "A is above and on the left of B"
        #and not "A is on the left of and above B"
        "90": "above ",
        "270": "under ",
        "0": "on the left of ",
        "180": "on the right of "
    } 

    combination = {
        # +-10%
        # < 5 -> not at all
        "0.20":"a bit ", #5 -> 25
        "0.40":"slightly ", #25 -> 45
        "0.60":"partially ", #45 -> 65
        "0.80":"strongly ", #65 -> 85
        "1.0":"totally " #85-> 100+
    }

    def compute_direction(self, parallels) -> float:

        angle = parallels[0].angle(radians = True) % pi / 2
        sin_cos = sin(angle) if angle > pi / 4 else cos(angle)

        def reduce_parallels_to_score(acc_total_score, curr_segment):
            def reduce_segment_scores(acc_segment_score, curr_point):
                
                if self.reference[curr_point].any() != 0 :
                    acc_segment_score[0] += 1
                if acc_segment_score[0] != 0 and self.relative[curr_point].any() != 0 :
                    acc_segment_score[1] +=1
                
                return acc_segment_score

            pixels_a, pixels_b = reduce(reduce_segment_scores, curr_segment, [0, 0])

            return acc_total_score + pixels_a * pixels_b
        return reduce(reduce_parallels_to_score, parallels, 0) / sin_cos

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
        Generate the pseudo-natural langage of the description in the descriptor
        TODO : have only ONE function that does this for ALL the descriptors we have
        and combine them (like : replace "is" by "touch" or "contains" depending of the descriptor)
        TODO : add the names of the object (like their path name or something) for better text generation
        '''
        interpretation = "A is "

        #for better language generation
        add_and = False

        #test all the directions
        for direction, value in self.description.items():
            temporary = ""

            #test all the quantities
            for key_comb, quantity in self.combination.items():
               
                #if it match
                if float(key_comb)-0.1 < value <= float(key_comb)+0.1:
                    temporary+= quantity + direction
                    if add_and:
                        interpretation += "and "
                    add_and = True
            #adding the textual information to the result
            interpretation += temporary
            
        interpretation +="B"

        return interpretation

