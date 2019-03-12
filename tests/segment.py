import unittest, random

from models.point import Point
from models.segment import Segment

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

    def test_slope(self):
        slope_1 = Segment([Point(0, 0), Point(10, 10)]) # Slope is 1
        slope_2 = Segment([Point(0, 0), Point(10, 20)]) # Slope is 2
        slope_half = Segment([Point(0, 0), Point(20, 10)]) # Slope is 1/2
        slope_horizontal = Segment([Point(0, 0), Point(10, 0)]) # Slope is 0
        slope_vertical = Segment([Point(0, 0), Point(0, 10)]) # Slope is 0

        self.assertEqual(slope_1.slope, 1)
        self.assertEqual(slope_half.slope, 0.5)
        self.assertEqual(slope_horizontal.slope, 0)
        self.assertEqual(slope_vertical.slope, 1)