'''
    This module contains only functions to compute a histogram
    of two full scanning (one for each image) and return an integer
    representing the value of the concerned relation for the given
    rays (parallels)

'''

from models import point
from functools import reduce

def angle(parallels, image_a, image_b) -> float:
    '''
        Latest measures are between 0.4 and 0.5 seconds of processing
    '''

    parallels = list(parallels) # Force the map to compute for optimization

    def reduce_parallels_to_score(acc_total_score, curr_segment):
        def reduce_segment_scores(acc_segment_score, curr_point):
            if image_a[curr_point].any() != 0 :
                acc_segment_score[0] += 1
            if image_b[curr_point].any() != 0 :
                acc_segment_score[1] +=1
            
            return acc_segment_score

        pixels_a, pixels_b = reduce(reduce_segment_scores, curr_segment, [0, 0])

        return acc_total_score + pixels_a * pixels_b

    return reduce(reduce_parallels_to_score, parallels, 0)
