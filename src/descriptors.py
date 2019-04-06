from models.descriptor import Descriptor
from math import sin, cos, pi
from functools import reduce
import numpy as np
from decorators import timeit

class AngularPresenceDescriptor(Descriptor):
    annulative = True
    used_values = 0.0
    value_number = 0
    relations = {
        #This order is for text generation, as "A is above and on the left of B"
        #and not "A is on the left of and above B"
        "90": "above ",
        "270": "under ",
        "0": "on the left ", 
        "180": "on the right "
    } 

    combination = {
        # +-10%
        # < 5 -> not at all
        "0.30":"a bit ", #5 -> 25
        "0.50":"slightly ", #25 -> 45
        "0.70":"partially ", #45 -> 65
        "0.90":"strongly ", #65 -> 85
        "1.0":"totally " #85-> 100+
    }

    # NEW METHOD
    # 2.5ms to compute_direction for a 1/8 resize factor
    # 12ms to compute_direction for a 1/3 resize factor
    # 
    # OLD METHOD
    # 7ms for 1/8
    # 45ms for 1/3
    # 
    # Keeping the old code since the new one may be buggy (and relies on grayscale)
    def compute_direction(self, parallels) -> float:
        angle = abs(parallels[int(len(parallels)/2)].angle(radians = True)) % (pi / 2) # Why the fuck not use the Segment::angle ?
        sin_cos = sin(angle) if angle > pi / 4 else cos(angle)

        def reduce_parallels_to_score(acc_total_score, curr_segment):

            if False: # This way, the method seems
                reference = list(map(lambda o: self.reference.image[o.x][o.y], curr_segment))
                relative = list(map(lambda o: self.relative.image[o.x][o.y], curr_segment))
                return acc_total_score + np.sum(np.array(reference)) * np.sum(np.array(reference) & (relative))
            else: # This is the old way to do it
                def reduce_segment_scores(acc_segment_score, curr_point):
                    
                    if self.reference[curr_point] != 0 :
                        acc_segment_score[0] += 1
                    if acc_segment_score[0] != 0 and self.relative[curr_point] != 0 :
                        acc_segment_score[1] +=1
                    
                    return acc_segment_score

                pixels_a, pixels_b = reduce(reduce_segment_scores, curr_segment, [0, 0])
                return acc_total_score + pixels_a * pixels_b

        return reduce(reduce_parallels_to_score, parallels, 0) / sin_cos


    def interpret(self):
        '''
        Generate the pseudo-natural langage of the description in the descriptor
        TODO : have only ONE function that does this for ALL the descriptors we have
        and combine them (like : replace "is" by "touch" or "contains" depending of the descriptor)
        TODO : add the names of the object (like their path name or something) for better text generation
        '''
        #interpretation = "A is "
        interpretation = ""
        #for better language generation
        add_and = False
        self.used_values = 0.0
        self.value_number = 0
        #measure of total score
        #test all the directions
        for direction, value in self.description.items():
            temporary = ""
            #test all the quantities
            for key_comb, quantity in self.combination.items():

                #if it match
                if float(key_comb)-0.1 <= value < float(key_comb)+0.1:
                    self.used_values += value
                    self.value_number += 1
                    if add_and:
                        temporary += "and "
                    temporary+= quantity + direction
                    add_and = True
                #adding the textual information to the result
            interpretation += temporary
            
        #interpretation +="B"
        
        #Total score between 5.7 and 7.7

        return interpretation

    def safety(self):
        if self.estimated_bias == 0:
            return self.used_values
        elif self.value_number != 0:
            return self.used_values / self.value_number
        else :
            return 0
class OverlappingDescriptor(Descriptor):
    annulative = False
    relations = {
        #This order is for text generation, as "A is above and on the left of B"
        #and not "A is on the left of and above B"
        "90": "a",
        "270": "b",
        "0": "c", 
        "180": "d"
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
        angle = abs(parallels[int(len(parallels)/2)].angle(radians = True)) % (pi / 2)
        sin_cos = sin(angle) if angle > pi / 4 else cos(angle)

        def reduce_parallels_to_score(acc_total_score, curr_segment):
            def reduce_segment_scores(acc_segment_score, curr_point):
                
                if self.reference[curr_point].any() != 0 and self.relative[curr_point].any():
                    acc_segment_score += 1
                return acc_segment_score

            overlapping = reduce(reduce_segment_scores, curr_segment, 0)

            return acc_total_score + (overlapping * overlapping) / 2
        return reduce(reduce_parallels_to_score, parallels, 0) / sin_cos


    def interpret(self):
        '''
        Generate the pseudo-natural langage of the description in the descriptor
        TODO : have only ONE function that does this for ALL the descriptors we have
        and combine them (like : replace "is" by "touch" or "contains" depending of the descriptor)
        TODO : add the names of the object (like their path name or something) for better text generation
        '''
        interpretation = ""
        if self.estimated_bias >= 0.85:
            interpretation += "totally overlapping "
        elif self.estimated_bias > 0.75:
            interpretation += "strongly overlapping "
        elif self.estimated_bias > 0.45:
            interpretation += "partially overlapping "
        elif self.estimated_bias > 0.25:
            interpretation += "slightly overlapping " 
        elif self.estimated_bias > 0.10:
            interpretation += "a bit overlapping "
        
        #measure of total score
        #test all the directions
        return interpretation

    def safety(self):
        return self.estimated_bias