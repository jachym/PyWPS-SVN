
__all__ = ["GetCapabilities","DescribeProcess","Execute"]


import unittest
import GetCapabilities

def suite():

    suite = unittest.TestSuite()
    suite.addTest(GetCapabilities.suite())

    return suite


if __name__ == "__main__":

    unittest.run()
