from pywps.Request import Request
from pywps.Request import NSMAP
import re

class DescribeProcess(Request):
    """GetCapabilites request class

    .. attribute:: acceptedVersions
    .. attribute:: request
    .. attribute:: identifiers
    """

    request = None
    schemaLocation=None
    identifiers=None
    version=None

    def __init__(self,request,method):
        Request.__init__(self,request,method)

        self.request = "describeprocess"

    def _parseRequestPOST(self,root):
        """Parse request via POST method
        
        :param root: root element
        """

        self.language = root.xpath("//wps:DescribeProcess/@language",namespaces= NSMAP)[0].lower()
        self.service = root.xpath("//wps:DescribeProcess/@service",namespaces= NSMAP)[0].lower()
        self.request = re.sub("{.*}","",root.tag).lower()
        self.version = root.xpath("//wps:DescribeProcess/@version",namespaces= NSMAP)[0].lower()

        self.identifiers = root.xpath("//wps:DescribeProcess/ows:Identifier/text()",namespaces= NSMAP)
        self.identifiers.sort()

    def _parseRequestGET(self,qs):
        """Parse request via GET method
        
        :param qs: dictionary
        """

        for i in qs.iterkeys():
            lowI = i.lower()
            if lowI == "language":
                self.language = qs[i][0].lower()
            elif lowI == "service":
                self.service = qs[i][0].lower()
            elif lowI == "request":
                self.request = qs[i][0].lower()
            elif lowI == "identifier":
                self.identifiers = qs[i][0].lower().split(",")
                self.identifiers.sort()
            elif lowI == "version":
                self.version = qs[i][0].lower()
        pass

    def _setSchemaLocation(self):
        self.schemaLocation = "http://schemas.opengis.net/wps/"+self.version+"/wpsGetCapabilities_request.xsd"
