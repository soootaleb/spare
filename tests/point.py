import unittest, random

from models.point import Point

class TestPointMethods(unittest.TestCase):

    def test_new(self):
        with self.assertRaises(ValueError) as context:
            Point(-1, 0)

        with self.assertRaises(ValueError) as context:
            Point(0, -1)

    def test_eq(self):

        for i in range(5):
            x = random.randint(0, 100)
            y = random.randint(0, 100)

            self.assertEqual(Point(x, y), Point(x, y))

        self.assertNotEqual(Point(0, 0), Point(10, 0))
        self.assertNotEqual(Point(0, 0), Point(0, 10))
        self.assertNotEqual(Point(0, 0), Point(10, 20))
        self.assertNotEqual(Point(0, 0), Point(20, 10))
