import numpy as np

def test_segments(segments, height, affiche = False):
    result = np.zeros((height, height))
    for segment in segments:
        for point in segment:
            result[point[0], point[1]] += 1
    if affiche:
        print(result)
    return np.array_equal(np.ones((height, height)), result)

