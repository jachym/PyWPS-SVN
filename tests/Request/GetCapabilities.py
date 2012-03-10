"""Unit test for WPS GetCapabilities request type
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


from pywps.Request.GetCapabilities import GetCapabilities

class TestGetCapabilitiesRequest(unittest.TestCase):


    def testIsGetCapabilities(self):
        """Test if given request is GetCapabilities request"""

        self.assertEquals(self.request.request,"getcapabilities")

    def testHasLang(self):
        """Test if given request is contains lang parameter"""

        self.assertTrue(self.request.language)
        self.assertEquals(self.request.language,"en")

    def testHasAcceptVersions(self):
        """Test if given request is contains AcceptVersions parameter"""

        self.assertTrue(self.request.acceptVersions)
        self.assertEquals(len(self.request.acceptVersions),1)
        self.assertEquals(self.request.acceptVersions, ["1.0.0"])

    def testHasService(self):
        """Test if given request is contains Service parameter"""

        self.assertTrue(self.request.service)
        self.assertEquals(self.request.service,"wps")

class TestGetCapabilitiesRequestPOST(TestGetCapabilitiesRequest):
    def setUp(self):

        request = open(os.path.join(REQUESTS,"getcapabilities-01.xml"),"r").read()
        self.request = GetCapabilities(request,"POST")

class TestGetCapabilitiesRequestGET(TestGetCapabilitiesRequest):
    def setUp(self):

        request = open(os.path.join(REQUESTS,"getcapabilities-01.txt"),"r").read()
        self.request = GetCapabilities(request,"GET")

def suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetCapabilitiesRequestPOST))
    suite.addTest(unittest.makeSuite(TestGetCapabilitiesRequestGET))
    return suite


if __name__ == "__main__":

    unittest.main()
