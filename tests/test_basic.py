# -*- coding: utf-8 -*-

from .context import FracFocusPDFParser
from .context import Logger

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""


    def test_logger (self):
        l = Logger ()
        
        l.log ('info', 'test')
        assert (l.has_error() == False)
        l.error ('err')
        assert (l.has_error() == True)

if __name__ == '__main__':
    unittest.main()