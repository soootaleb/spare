import unittest, random, cv2 as cv, numpy as np, math

from models.point import Point
from models.image import Image
from models.segment import Segment

from functools import reduce

class TestImageMethods(unittest.TestCase):

    WIDTH = 50
    HEIGHT = 50

    def test_new(self):
        image = Image(np.zeros((self.WIDTH, self.HEIGHT, 3), np.uint8))

        self.assertIsNotNone(image.base)
        self.assertIsNotNone(image.fname)
        self.assertIsNotNone(image.image)

    def test_dimensions(self):
        image = Image(np.zeros((self.WIDTH, self.HEIGHT, 3), np.uint8))

        self.assertEqual(image.width, self.WIDTH)
        self.assertEqual(image.height, self.HEIGHT)
        self.assertEqual(image.max_dimension, max(self.WIDTH, self.HEIGHT))
    
    def test_center(self):
        image = Image(np.zeros((self.WIDTH, self.HEIGHT, 3), np.uint8))

        self.assertEqual(image.center, Point(self.WIDTH / 2, self.HEIGHT / 2))

    def test_contains(self):
        image = Image(np.zeros((self.WIDTH, self.HEIGHT, 3), np.uint8))
        
        self.assertTrue(image.center in image)
        self.assertTrue(Point(0, 0) in image)
        self.assertTrue(Point(self.WIDTH - 1, self.HEIGHT - 1) in image)

        self.assertFalse(Point(self.WIDTH + 1, self.HEIGHT + 1) in image)

    # def test_resize(self):
    #     image = Image(np.zeros((self.WIDTH, self.HEIGHT, 3), np.uint8))

    #     factors = [2, 1, 1/2, 1/4, 1/8]

    #     for factor in factors:
    #         image.reset()
    #         image.resize(factor)
    #         self.assertEqual(image.width, round(self.WIDTH * factor))
    #         self.assertEqual(image.height, round(self.HEIGHT * factor))

    #     with self.assertRaises(Exception) as context:
    #         image.resize(0)

    def test_parallels_unicity(self):
        image = Image(np.zeros((self.WIDTH, self.HEIGHT, 3), np.uint8))

        angles = [0, 10, 45, 90, 100, 270, 320]

        def index(point):
            return str(point.x) + '-' + str(point.y)

        for direction in angles:
            visited = []
            for segment in image.parallels(direction):
                for point in segment:
                    if index(point) in visited:
                        self.fail('The point {} is already visited'.format(point))

    def test_parallels_coverage(self):
        image = Image(np.zeros((self.WIDTH, self.HEIGHT, 1), np.uint8))

        angles = [0, 10, 45, 90, 100, 270, 320]

        for direction in angles:
            parallels = image.parallels(direction)
            found = reduce(lambda acc, curr: acc + len(curr), parallels, 0)
            self.assertEqual(found, self.WIDTH * self.HEIGHT)
            