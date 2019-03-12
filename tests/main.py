import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from point import TestPointMethods
from image import TestImageMethods
from segment import TestSegmentMethods

if __name__ == '__main__':
    unittest.main()