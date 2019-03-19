import unittest, random

from models.point import Point
from models.segment import Segment

import numpy as np

class TestSegmentMethods(unittest.TestCase):

    def test_new(self):
        with self.assertRaises(ValueError) as context:
            Segment([])

    def test_extremums(self):
        a = Point(random.randint(0, 100), random.randint(0, 100))
        b = Point(random.randint(0, 100), random.randint(0, 100))
        c = Point(random.randint(0, 100), random.randint(0, 100))

        segment = Segment([a, b, c])

        self.assertEqual(segment.start, a)
        self.assertEqual(segment.end, c)

    def test_getitem(self):
        a = Point(10, 20)
        b = Point(20, 30)
        c = Point(30, 40)

        segment = Segment([a, b, c])

        self.assertEqual(segment[Point(10, 20)], a) # Access by point
        self.assertEqual(segment[20, 30], b) # Access by coordinates
        self.assertEqual(segment[2], c) # Access by index
        self.assertEqual(segment[100, 100], None) # Accessing a missing point

    def test_append(self):
        a = Point(10, 20)
        b = Point(20, 30)
        c = Point(30, 40)

        segment = Segment([a, b, c])

        segment.append(Point(31, 40))

        # Working case
        self.assertEqual(segment.end, Point(31, 40))
        
        # Point is too far
        with self.assertRaises(ValueError) as context:
            segment.append(Point(100, 100))
        
        # Point already exists
        with self.assertRaises(ValueError) as context:
            segment.append(Point(31, 40))

    def test_angle(self):
        angle_1 = Segment([Point(0, 0), Point(10, 10)]) # Angle is 45°
        angle_2 = Segment([Point(0, 0), Point(10, 20)]) # Angle is arctan(20/10)
        angle_half = Segment([Point(0, 0), Point(20, 10)]) # Angle is arctan(10/20)
        angle_vertical = Segment([Point(0, 0), Point(10, 0)]) # Angle is 0°
        angle_horizontal = Segment([Point(0, 0), Point(0, 10)]) # Angle is 90°

        self.assertAlmostEqual(angle_1.angle(radians = True), np.pi / 4)
        self.assertAlmostEqual(angle_half.angle(radians = True), np.arctan(2))
        self.assertAlmostEqual(angle_horizontal.angle(radians = True), 0)
        self.assertAlmostEqual(angle_vertical.angle(radians = True), np.pi / 2)

        self.assertAlmostEqual(angle_1.angle(radians = False), 45)
        self.assertAlmostEqual(angle_half.angle(radians = False), 63, places = 0)
        self.assertAlmostEqual(angle_horizontal.angle(radians = False), 0)
        self.assertAlmostEqual(angle_vertical.angle(radians = False), 90)