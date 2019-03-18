from models.descriptor import Descriptor
from math import sin
from functools import reduce

class AngularPresenceDescriptor(Descriptor):

    relations = {
        "0": "on the left of",
        "90": "above",
        "180": "on the right of",
        "270": "under",
    } 

    def compute_direction(self, parallels) -> float:
        def reduce_parallels_to_score(acc_total_score, curr_segment):
            def reduce_segment_scores(acc_segment_score, curr_point):
                
                if self.reference[curr_point].any() != 0 :
                    acc_segment_score[0] += 1
                if acc_segment_score[0] != 0 and self.relative[curr_point].any() != 0 :
                    acc_segment_score[1] +=1
                
                return acc_segment_score

            pixels_a, pixels_b = reduce(reduce_segment_scores, curr_segment, [0, 0])

            #TODO : get a real normalisation
            return acc_total_score + (pixels_a * pixels_b / (10*(len(curr_segment)+ pixels_a + pixels_b)))

        return reduce(reduce_parallels_to_score, parallels, 0)

    def mask(self, direction):
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