from pywps.Request import Request
from pywps.Request import NSMAP
import re

class GetCapabilities(Request):
    """GetCapabilites request class

    .. attribute:: acceptedVersions
    .. attribute:: request
    """

    acceptVersions = None
    request = None
    schemaLocation=None

    def __init__(self,request,method):
        Request.__init__(self,request,method)

        self.request = "getcapabilities"

    def _parseRequestPOST(self,root):
        """Parse request via POST method
        
        :param root: root element
        """
        self.acceptVersions = root.xpath("//wps:AcceptVersions/ows:Version/text()", namespaces=NSMAP)
        self.language = root.xpath("//wps:GetCapabilities/@language",namespaces= NSMAP)[0].lower()
        self.service = root.xpath("//wps:GetCapabilities/@service",namespaces= NSMAP)[0].lower()
        self.request = re.sub("{.*}","",root.tag).lower()

    def _parseRequestGET(self,qs):
        """Parse request via GET method
        
        :param qs: dictionary
        """

        for i in qs.iterkeys():
            lowI = i.lower()
            if lowI == "language":
                self.language = qs[i][0].lower()
            elif lowI == "acceptversions":
                self.acceptVersions = qs[i]
            elif lowI == "service":
                self.service = qs[i][0].lower()
            elif lowI == "request":
                self.request = qs[i][0].lower()
        pass

    def _setSchemaLocation(self):
        self.schemaLocation = "http://schemas.opengis.net/wps/"+self.version+"/wpsGetCapabilities_request.xsd"
