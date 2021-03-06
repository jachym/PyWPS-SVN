import os
import sys

pywpsPath = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))
#sys.path.append(pywpsPath)
sys.path.insert(0, pywpsPath)

import pywps
import pywps.Process

import unittest
import os
import urllib
from xml.dom import minidom
import base64
import sys
import tempfile

class ExceptionTestCase(unittest.TestCase):
    tiffurl="http://rsg.pml.ac.uk/wps/testdata/srtm_NW_iberia.tif" #17megas
    #tiffurl="http://rsg.pml.ac.uk/wps/testdata/srtm_algarve.tif" #3.2 megas
    wfsurl = "http://rsg.pml.ac.uk/geoserver2/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=rsg:areas_pw&maxFeatures=1"
    owsns = "http://www.opengis.net/ows/1.1"
    
    xmldom= None

#NOTE: Depending on the code position where the exception is raised, the pywps.response maybe filled or not
#for proper Exception debug it should be better to use a try: exception. See: soap_testes.testSOAP11Fault
    
    def setUp(self):
        #Silence sterr otherwise the promopt is flooded with error message from exceptions
        sys.stderr = open('/dev/null',"w") 
    
    def testMaxFileProcess(self):
        """Text exception raise from MaxFileSize (process and cfg file)"""
        #Calling complexRaster process that has datainput with maxfilezie=2.0megas below 3mega of pywps.cfg
       
        self._setFromEnv()
        
        mypywps = pywps.Pywps(pywps.METHOD_GET)
        inputs = mypywps.parseRequest("service=wps&request=execute&version=1.0.0&identifier=complexRaster&datainputs=[indata=%s]" % self.tiffurl)
        
        mypywps.performRequest()
        xmldom = minidom.parseString(mypywps.response)
        #Check that is an exception
        exceptionDOM=xmldom.getElementsByTagNameNS(self.owsns,"Exception")
        self.assertTrue(len(exceptionDOM)>0)
        
        #Check that is FileSizeExceeded
        self.assertEqual(exceptionDOM[0].getAttribute("exceptionCode"),"FileSizeExceeded")
        
        #Check that is 2.0 MB
        self.assertTrue("2.0" in exceptionDOM[0].getAttribute("locator"))
        
        #Calling complexprocess that has no maxfilesize, checking that pywps.cfg limit is respected
        #its is enough one raster input to raise the error
        inputs = mypywps.parseRequest("service=wps&request=execute&version=1.0.0&identifier=complexprocess&datainputs=[rasterin=%s]" % (urllib.quote(self.tiffurl)) )
        mypywps.performRequest()
     
        xmldom = minidom.parseString(mypywps.response)
        exceptionDOM=xmldom.getElementsByTagNameNS(self.owsns,"Exception")
        
        self.assertTrue(len(exceptionDOM)>0)
        self.assertEqual(exceptionDOM[0].getAttribute("exceptionCode"),"FileSizeExceeded")
        #Maximum file size is 3.0 MB for input
        self.assertTrue("3.0" in exceptionDOM[0].getAttribute("locator"))
        

    def testQuoteChar(self):
        """Test escape in WSP ExceptionText"""
        from pywps.Process import WPSProcess
        import re
        name="proc_name"
        exception_message="<<to-be-escaped>>"
        wps = pywps.Pywps(pywps.METHOD_GET)
        wps.parseRequest('service=WPS&version=1.0.0&request=Execute&identifier=%s' % name)
    
        class Process(WPSProcess):
            def __init__(self):
                WPSProcess.__init__(self,
                                    identifier = name,
                                    title="Testing process")
            def execute(self):
                raise RuntimeError(exception_message)
      
        response=wps.performRequest(processes=[Process()])      
        
        pattern=re.compile('<ows:ExceptionText>(.*)</ows:ExceptionText>')
        if pattern.search(response):
            exception_text = pattern.search(response).group(1)
        else:
            assert False, "ExceptionText not found in response:\n%s" % response
            
        self.assertEquals('Failed to execute WPS process [proc_name]: &lt;&lt;to-be-escaped&gt;&gt;',exception_text)
        self.assertNotEquals('Failed to execute WPS process [proc_name]: <<to-be-escaped>>',exception_text)


    def _setFromEnv(self):
        os.putenv("PYWPS_PROCESSES", os.path.join(pywpsPath,"tests","processes"))
        os.environ["PYWPS_PROCESSES"] = os.path.join(pywpsPath,"tests","processes")
        os.putenv("PYWPS_CFG", os.path.join(pywpsPath,"pywps","default"))
        os.environ["PYWPS_CFG"] = os.path.join(pywpsPath,"pywps","default.cfg")


if __name__ == "__main__":
    #unittest.main()
   suite = unittest.TestLoader().loadTestsFromTestCase(ExceptionTestCase)
   unittest.TextTestRunner(verbosity=2).run(suite)