from models.descriptor import Descriptor
from math import sin
from functools import reduce

class AngularPresenceDescriptor(Descriptor):

    relations = {
        #This order for text generation, as "A is above and on the left of B"
        #and not "A is on the left of and above B"
        "90": "above ",
        "270": "under ",
        "0": "on the left of ",
        "180": "on the right of "
    } 
    # +-10%
    combination = {
        # < 10 -> not at all
        "0.2":"a bit ", #10 -> 30
        "0.4":"partially ", #30 -> 50
        "0.6":"sort of ", #50 -> 70 
        "0.8":"strongly ", #70 -> 90
        "1.0":"totally " #90-> 100+
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

    def interpret(self):
        interpretation = "A is "
        add_and = False
        for direction, value in self.description.items():
            temporary = ""
            for key_comb, quantity in self.combination.items():
               
                if float(key_comb)-0.1 <= value < float(key_comb)+0.1:
                    temporary+= quantity + direction
                    if add_and:
                        interpretation += "and "
                    add_and = True

            interpretation += temporary
            
        interpretation +="B"
        print(interpretation)

        return interpretation

