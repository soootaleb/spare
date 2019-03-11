'''
    This module contains only functions to compute a histogram
    of two full scanning (one for each image) and return an integer
    representing the value of the concerned relation for the given
    rays (parallels)

'''

from models import point

def angle(parallels, image_a, image_b) -> float:
    '''
        Latest measures are between 0.4 and 0.5 seconds of processing
    '''
    score = 0
    for segment in parallels:
        pixels_a = 0
        pixels_b = 0
        for point in segment:
            if image_a[point].any() != 0 :
                pixels_a += 1
            if image_b[point].any() != 0 :
                pixels_b +=1
        score+= pixels_a * pixels_b

    return score