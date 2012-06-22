
__all__ = ["GetCapabilities","DescribeProcess","Execute"]


import unittest
import GetCapabilities
import DescribeProcess

def suite():

    suite = unittest.TestSuite()
    suite.addTest(GetCapabilities.suite())
    suite.addTest(DescribeProcess.suite())

    return suite


if __name__ == "__main__":

    unittest.run()
