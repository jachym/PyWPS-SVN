"""Unit test for WPS DescribeProcess request type
"""

import unittest


import sys,os
sys.path.insert(0,os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
        ),"..",".."))

REQUESTS = os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
                    ),"..","requests")
            )


from pywps.Request.DescribeProcess import DescribeProcess

class TestDescribeProcessRequest(unittest.TestCase):


    def testIsDescribeProcess(self):
        """Test if given request is DescribeProcess request"""

        self.assertEquals(self.request.request,"describeprocess")

    def testHasLang(self):
        """Test if given request is contains lang parameter"""

        self.assertTrue(self.request.language)
        self.assertEquals(self.request.language,"en")

    def testIdentifiers(self):
        """Test if given requets has propper identifiers"""
        identifiers = ["intersection","union"]
        identifiers.sort()
        self.assertListEqual(self.request.identifiers,identifiers)

    def testVersion(self):
        """Test if given requets has propper version"""
        self.assertEquals(self.request.version,"1.0.0")

class TestDescribeProcessRequestPOST(TestDescribeProcessRequest):
    def setUp(self):

        request = open(os.path.join(REQUESTS,"describeprocess-01.xml"),"r").read()
        self.request = DescribeProcess(request,"POST")

class TestDescribeProcessRequestGET(TestDescribeProcessRequest):
    def setUp(self):

        request = open(os.path.join(REQUESTS,"describeprocess-01.txt"),"r").read()
        self.request = DescribeProcess(request,"GET")

def suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDescribeProcessRequestPOST))
    suite.addTest(unittest.makeSuite(TestDescribeProcessRequestGET))
    return suite


if __name__ == "__main__":

    unittest.main()
