from models.descriptor import Descriptor

from functools import reduce

class AngularPresenceDescriptor(Descriptor):

    relations = {
        "0": "on the right of",
        "90": "above",
        "180": "on the left of",
        "360": "under",
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

            return acc_total_score + pixels_a * pixels_b

        return reduce(reduce_parallels_to_score, parallels, 0)

    def mask(self, direction):
        return 0.6 # Percentage of match between the mask and the description in the given direction